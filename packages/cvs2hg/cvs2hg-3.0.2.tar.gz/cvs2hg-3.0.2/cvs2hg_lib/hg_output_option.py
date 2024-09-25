# -*- coding: utf-8 -*-
# (Be in -*- python -*- mode.)
#
# ====================================================================
# Copyright (c) 2009 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
# This software consists of voluntary contributions made by many
# individuals.  For exact contribution history, see the revision
# history and logs, available at http://cvs2svn.tigris.org/.
# ====================================================================

import os
import re
import bisect
import gc
import shutil
import inspect

import datetime
try:
    import pytz
except ImportError as err:
    pytz = None
    pytz_import_error = err

from cvs2hg_lib.common import FatalError
from cvs2hg_lib.common import InternalError
from cvs2hg_lib.context import Ctx
from cvs2hg_lib.log import logger
from cvs2hg_lib.artifact_manager import artifact_manager
from cvs2hg_lib.symbol import IncludedSymbol
from cvs2hg_lib.symbol import Trunk
from cvs2hg_lib.symbol import Branch
from cvs2hg_lib.cvs_item import CVSRevision
from cvs2hg_lib.cvs_item import CVSRevisionAdd
from cvs2hg_lib.cvs_item import CVSRevisionChange
from cvs2hg_lib.cvs_item import CVSRevisionDelete
from cvs2hg_lib.cvs_item import CVSRevisionNoop
from cvs2hg_lib.repository_mirror import RepositoryMirror
from cvs2hg_lib.repository_mirror import LODExistsError
from cvs2hg_lib.dvcs_common import DVCSOutputOption
from cvs2hg_lib.dvcs_common import MirrorUpdater

from mercurial import ui, hg, node as hgnode, context
from mercurial.error import RepoError  # 1.2 and later

###########################################################################
# Compatibility layer
###########################################################################

def _mercurial_version_tuple():
    import mercurial.util
    import re
    import sys
    try:
        return mercurial.util.versiontuple()
    except:
        # Simplified version of actual versiontuple (we don't care about minors…)
        ver = mercurial.util.version()
        m = re.match(br'(\d+(?:\.\d+){,2})[\+-]?(.*)', ver)
        if m:
            result = tuple([int(x) for x in m.group(1).split('.')])
            # Sanity check
            if result < (3, 2):
                sys.stderr.write("""ERROR: cvs2hg requires Mercurial 3.2 or later (found {0}).""".format(ver))
                sys.exit(1)
            return result
        else:
            return (0,)


mercurial_version = _mercurial_version_tuple()


def construct_memfilectx(repo, memctx, path, data, islink=False,
                         isexec=False, copied=None):
    """Constructs context.memfilectx in a way appropriate to mercurial
    being used (the signature unfortunately used to change)"""

    if mercurial_version >= (5, 0):
        return context.memfilectx(
            repo=repo, changectx=memctx, path=path, data=data,
            islink=islink, isexec=isexec, copysource=copied)
    elif 'changectx' in context.memfilectx.__init__.__code__.co_varnames:
        # Mercurial >= 4.5.x (after https://www.mercurial-scm.org/repo/hg-stable/rev/8a0cac20a1ad)
        return context.memfilectx(
            repo=repo, changectx=memctx, path=path, data=data,
            islink=islink, isexec=isexec, copied=copied)
    elif 'repo' in context.memfilectx.__init__.__code__.co_varnames:
        # Mercurial >= 3.1
        return context.memfilectx(
            repo=repo, path=path, data=data,
            islink=islink, isexec=isexec, copied=copied)
    else:
        # Mercurial <= 3.0.2
        return context.memfilectx(
            path, data, islink, isexec, copied)

def return_skipped_rev():
    """Tell mercurial to ignore given changeset.

    Old Mercurials raised IOError's (which were caught and interpreted
    as orders to skip), new Mercurials return None.

    The change happened at 650b5b6e75ed in hg-stable, last tag to use
    IOErrors is 3.1.
    """
    def legacy_way():
        raise IOError()

    def modern_way():
        return None

    # Unfortunately there is nothing obvious to test for this very change
    # but on the very next commit tidy_dirs method was removed from
    # hgext/convert/subversion. So let's use this. In case of any problems
    # handling modern mercurial is saner default.
    global _return_skipped_rev
    if not _return_skipped_rev:
        _return_skipped_rev = modern_way
        try:
            import mercurial.hgext.subversion
            if hasattr(mercurial.hgext.subversion, 'tidy_dirs'):
                _return_skipped_rev = legacy_way
        except:
            pass

    _return_skipped_rev()


_return_skipped_rev = None

###########################################################################

class HgOutputOption(DVCSOutputOption):
    """An OutputOption that creates a new Mercurial repository and adds changesets
    to it."""

    name = "Mercurial"

    # Three ways to create fixup changesets for tags and branches:
    #   - always: create a fixup changeset unconditionally, even if it's
    #     not necessary (i.e. the tag or branch is a simple copy of an
    #     existing changeset) (default for branches)
    #
    #   - optional: don't bother creating a fixup changeset if the tag or
    #     branch is a simple copy of an existing changeset, otherwise
    #     create one (default for tags)
    #
    #   - sloppy: like optional, but more relaxed: if the tag or branch only
    #     deletes files from an existing changeset, act like it is a
    #     simple copy of that changeset and do not create a fixup (this is
    #     to accomodate the CVS practice of tagging or branching only part
    #     of a source tree)
    VALID_FIXUP_MODES = ('always', 'optional', 'sloppy')

    def __init__(self, repo_dir, author_transforms=None, timezone=None,
                 tag_fixup_mode='optional', branch_fixup_mode='always'):
        """Constructor.

        REPO_DIR is the location of the Mercurial repository.  It will be
        created if it doesn't exist.

        AUTHOR_TRANSFORMS is the same as for GitOutputOption.
        (XXX its format is an artifact of fastimport format: neither git nor hg
        insist on \"Real Name <email@domain>\", as the author/committer/user is
        an arbitrary string.  For writing directly to an hg repo, we
        could allow any string.)

        TIMEZONE is the timezone to use for all Mercurial timestamps.  It
        can be an integer (seconds east of UTC), which is only meaningful
        for a timezone that has never used DST (such as UTC itself).  Or it
        can be an instance of datetime.tzinfo, in case you feel like
        programming your own timezone; see the Python Library Reference for
        details.  Finally, it can be a string, for a name from the Olsen
        timezone database such as \"Canada/Eastern\" or \"Europe/Berlin\".
        To use a timezone name, you must have the pytz library installed.
        If TIMEZONE is not supplied, all Mercurial timestamps will be in
        UTC, just as with CVS.

        TAG_FIXUP_MODE determines when fixup changesets will be created for
        tags; it can be 'always', 'optional', or 'sloppy' (default: 'optional').

        BRANCH_FIXUP_MODE is the same but for branches (default: 'always').
        """
        DVCSOutputOption.__init__(self)
        self.repo_dir = repo_dir
        self.author_transforms = self.normalize_author_transforms(author_transforms)
        self.set_timezone(timezone)
        self.set_tag_fixup_mode(tag_fixup_mode)
        self.set_branch_fixup_mode(branch_fixup_mode)

        # Object for keeping self._mirror in sync with the progress of the
        # conversion.  (Serves a similar purpose to GitOutputOption's
        # revision_writer, except it doesn't write revisions anywhere of
        # course.)
        self.mirror_updater = MirrorUpdater()

        # Record all the changesets on each CVS line-of-development as a map
        # {lod : [(revnum, node)]}, where revnum is a Subversion revision
        # number (from SVNCommit objects) and node is a Mercurial changeset ID.
        # Note that the first element of every list is either a fixup commit or
        # not part of the branch at all (in sloppy fixup mode).  That is, the
        # first "real" commit on each LOD is changesets[lod][1].
        self.changesets = {}

        # The current head of each branch as a map from CVS LineOfDevelopment
        # to Mercurial node.  (Note: if a branch is created without a fixup
        # commit, this map initially records a "head" node that is not actually
        # on that branch, so it's not technically the branch head.  That's
        # covered up pretty quickly by actual commits on the branch, though.)
        self.branch_head = {}

        # Each tag fixup results in an open head, which is undesirable.  So
        # we artificially "merge" them back into the appropriate branch at
        # the earliest opportunity.  This map tracks unmerged fixup heads by
        # mapping CVS LOD to tuple (tag, node).
        self.pending_fixup = {}

        # Map CVS branch names to LineOfDevelopment objects (including "trunk"
        # mapped to the Trunk instance used in this conversion).
        self.branch_lod = {}

        # Map tag name to node (tags are all written at the end)
        self.tags = {}

        self.ui = None                      # mercurial.ui.ui
        self.repo = None                    # mercurial.localrepo.localrepository
        self.start_node = None              # parent of the first converted rev

    def check(self):
        DVCSOutputOption.check(self)
        self.check_repo()

    def check_repo(self):
        # Mercurial is happy to create a repository in an existing directory,
        # so we have to check for .hg.
        if os.path.isdir(os.path.join(self.repo_dir, '.hg')):
            raise RuntimeError("directory '%s' already contains a Mercurial repository"
                             % self.repo_dir)

    def set_timezone(self, timezone):
        """Set the timezone for Mercurial timestamps.  See constuctor
        docstring for details."""
        if timezone is None:                # UTC by default
            self.timezone = 0
        elif isinstance(timezone, int):     # seconds east of UTC
            min = -12*3600
            max = 12*3600
            if not (min <= timezone <= max):
                raise ValueError(
                  "invalid timezone offset %d (must be between %d and %d)"
                  % (timezone, min, max))
            self.timezone = timezone
        elif isinstance(timezone, datetime.tzinfo):
            self.timezone = timezone
        elif isinstance(timezone, str):
            if pytz is None:
                raise FatalError(
                  "unable to handle timezone names: did you install pytz?\n"
                  "(original error: %s: %s)"
                  % (pytz_import_error.__class__.__name__, pytz_import_error))
            self.timezone = pytz.timezone(timezone)

    def set_tag_fixup_mode(self, mode):
        self._check_fixup_mode("tag", mode)
        self.tag_fixup_mode = mode

    def set_branch_fixup_mode(self, mode):
        self._check_fixup_mode("branch", mode)
        self.branch_fixup_mode = mode

    def _check_fixup_mode(self, what, mode):
        if mode not in self.VALID_FIXUP_MODES:
            raise ValueError("invalid %s fixup mode %r (must be one of %s)"
                             % (what, mode, ", ".join(self.VALID_FIXUP_MODES)))


    # -- Public methods required by OutputOption --

    def register_artifacts(self, which_pass):
        DVCSOutputOption.register_artifacts(self, which_pass)
        Ctx().revision_reader.register_artifacts(which_pass)
        self.mirror_updater.register_artifacts(which_pass)

    # hg tag/branch names definitely cannot contain newline, and almost
    # certainly should not contain colon.  apart from that, ... ?
    _symbol_name_re = re.compile(r':\n')

    def check_symbols(self, symbol_map):
        for symbol in symbol_map:
            # IncludedSymbol is the base class of Branch and Tag
            if (isinstance(symbol, IncludedSymbol) and
                self._symbol_name_re.search(symbol.name)):
                raise FatalError("invalid Mercurial tag/branch name: %r" % symbol.name)

    def setup(self, svn_rev_count):
        DVCSOutputOption.setup(self, svn_rev_count)

        self.ui = ui.ui()
        self.open_repo()
        assert self.repo.local()

        # Handle Mercurial API changes.
        # - 1.6: now repo.transaction() takes a 'desc' argument
        if 'desc' in inspect.getargspec(self.repo.transaction)[0]:
            self.repo_transaction = lambda: self.repo.transaction("cvs2hg")
        else:
            self.repo_transaction = self.repo.transaction

        Ctx().revision_reader.start()
        self.mirror_updater.start(self._mirror)

        # cvs2svn can live without cyclic garbage collection, but Mercurial
        # can't (or at least not 1.3: with 1.1 and 1.2, memory use is quite
        # tolerable, but it grows very fast with 1.3 and GC disabled)
        gc.enable()
        gc.collect()

        # Monkey-patch mercurial.encoding to assume the local encoding is UTF-8,
        # since CleanMetadataPass takes care of converting whatever is in CVS to
        # UTF-8.
        try:
            from mercurial import util        # Mercurial 1.1, 1.2
            util._encoding                    # trigger a AttributeError if not set
            util._encoding = "utf-8"
        except AttributeError:
            from mercurial import encoding    # Mercurial 1.3 and later
            encoding.encoding = "utf-8"

    def open_repo(self):
        # This blows up if the output repo already exists.  This should be
        # caught early by HgRunOptions, so don't bother to handle the error.
        # If someone creates the repo between the check by HgRunOptions and
        # now, well, too bad.
        self.repo = hg.repository(self.ui, self.repo_dir, create=True)
        self.start_node = hgnode.nullid

    def process_initial_project_commit(self, svn_commit):
        # Like git, Mercurial doesn't need an "initialize repo" commit.
        # N.B. this means that Mercurial revision 0 corresponds to
        # Subversion revision 2.
        logger.debug("ignoring initial project commit: %s" % svn_commit)

        assert len(svn_commit.projects) == 1
        trunk_lod = self.branch_lod["trunk"] = svn_commit.projects[0].get_trunk()
        self.branch_head[trunk_lod] = self.start_node

        self._mirror.start_commit(svn_commit.revnum)
        self._mirror.end_commit()

    def process_primary_commit(self, svn_commit):
        logger.debug("got primary commit: %s" % svn_commit)

        self._mirror.start_commit(svn_commit.revnum)
        (filenames, getfilectx) = self._analyze_cvs_revs(
          svn_commit.get_cvs_items())

        lod = self._get_unique_lod(
          [cvs_rev.lod for cvs_rev in svn_commit.get_cvs_items()],
          "commit affects %d LODs: %s")
        assert isinstance(self.branch_lod["trunk"], Trunk), \
               ("branch_lod['trunk'] is %r (expected a Trunk object)"
                % self.branch_lod.get("trunk"))

        parent1 = self._get_parent1(svn_commit, lod)

        parent2 = (self.detect_merge(svn_commit, lod, parent1) or
                   self._get_parent2(lod))
        node = self._commit_primary(
          svn_commit, [parent1, parent2], filenames, getfilectx, lod)

        for cvs_rev in svn_commit.get_cvs_items():
            self.mirror_updater.process_revision(cvs_rev, post_commit=False)

        self._mirror.end_commit()
        self.changesets.setdefault(lod, []).append((svn_commit.revnum, node))
        self.branch_head[lod] = node

        branch = self.repo[node].branch()
        logger.normal("added changeset %d:%s (branch: %s)"
                      % (len(self.repo)-1, hgnode.short(node), branch))

        if len(self.repo) % 1000 == 0:
            nobj = gc.collect()
            logger.debug("garbage collection found %d objects" % nobj)

    def process_post_commit(self, svn_commit):
        logger.debug("got post commit: %s" % svn_commit)
        self._mirror.start_commit(svn_commit.revnum)

        source_lod = self._get_unique_lod(
          # argh: cannot use svn_commit.get_cvs_items() here, because
          # SVNPostCommit deliberately returns an empty list -- need to
          # get around that somehow
          [cvs_rev.lod for cvs_rev in svn_commit.cvs_revs],
          "post-ntdb commit affects %d LODs: %s")
        motivating_rev = self.branch_head[source_lod]
        (filenames, getfilectx) = self._analyze_cvs_revs(
          svn_commit.cvs_revs, post_node=motivating_rev)

        # This is just for "%(revnum)s" in the commit message.
        svn_commit.motivating_revnum = hgnode.short(motivating_rev)

        lod = self.branch_lod["trunk"]
        try:
            parent1 = self.changesets[lod][-1][1]
            parent2 = motivating_rev
        except KeyError:
            # default branch doesn't exist yet
            parent1 = motivating_rev
            parent2 = self._get_parent2(lod)

        node = self._commit_post(
          svn_commit, [parent1, parent2], filenames, getfilectx, lod)

        for cvs_rev in svn_commit.cvs_revs:
            self.mirror_updater.process_revision(cvs_rev, post_commit=True)

        self._mirror.end_commit()
        self.changesets.setdefault(lod, []).append((svn_commit.revnum, node))
        self.branch_head[lod] = node

        logger.normal("added compensation changeset %d:%s"
                      % (len(self.repo)-1, hgnode.short(node)))

    def process_branch_commit(self, svn_commit):
        logger.debug("got branch commit: %s" % svn_commit)
        branch = svn_commit.symbol.name
        self._mirror.start_commit(svn_commit.revnum)
        source_groups = self._get_source_groups(svn_commit)

        lods = set()
        for (_, _, cvs_symbols) in source_groups:
            lods.update([cvs_symbol.symbol for cvs_symbol in cvs_symbols])
        lod = self._get_unique_lod(lods, "branch created with %d CVS LODs: %s")

        # This information isn't used anywhere in this class, but it could be handy
        # in subclasses (e.g. anyone overriding detect_merge()).
        self.branch_lod[lod.name] = lod

        # This has to come before adding the LOD to self._mirror.
        need_fixup = self._need_fixup(
          self.branch_fixup_mode, svn_commit, source_groups)

        first_creation = True               # most branches are only created once
        try:
            self._mirror.add_lod(lod)
            self.changesets[lod] = []
        except LODExistsError:
            # This just means the branch was created twice in CVS, and will
            # therefore be created twice in Mercurial (same thing as happens
            # in Subversion output).
            first_creation = False

        created = True                      # did we create a new changeset?
        if first_creation:
            if not need_fixup:
                # XXX copied from process_tag_commit() below
                (source_revnum, source_lod, cvs_symbols) = source_groups[0]
                node = self._get_cset(source_lod, source_revnum)
                created = False
                logger.verbose('branch %s is a simple copy of %s at r%d (%s)'
                               % (branch, source_lod, source_revnum, hgnode.short(node)))
            else:
                logger.verbose('branch %s requires a fixup changeset' % branch)
                node = self._create_first_fixup(
                  self.branch_fixup_mode, svn_commit, source_groups, lod)
        else:
            node = self._create_second_coming(svn_commit, source_groups, lod)

        # This is a bit weird: if we did not create a fixup, then node points
        # to the changeset *on a different branch* which is the root of the new
        # branch.  So adding it to changesets[lod] makes it look like that root
        # node is part of the new branch, which is patently false.  But it's 1)
        # consistent with branch_head (which temporarily claims that that root
        # node is part of the new branch), 2) it means that the first "real"
        # (non-fixup) commit on the new branch is always changesets[lod][1],
        # and 3) it's necessary if there's a tag that happens to point to the
        # root of this branch.
        self.changesets[lod].append((svn_commit.revnum, node))
        self.branch_head[lod] = node
        self._update_symbol(source_groups)
        self._mirror.end_commit()
        if created:
            logger.normal("added branch %r with fixup changeset %d:%s"
                          % (branch, len(self.repo)-1, hgnode.short(node)))
        else:
            logger.normal("added branch %r from changeset %s"
                          % (branch, hgnode.short(node)))

    def process_tag_commit(self, svn_commit):
        logger.debug("got tag commit: %s" % svn_commit)

        # XXX it ought to be possible for a CVS tag to have a split beginning, just
        # like a CVS branch can.  Should handle it the same we way handle split
        # branches.

        tag = svn_commit.symbol.name
        self._mirror.start_commit(svn_commit.revnum)

        source_groups = self._get_source_groups(svn_commit)
        need_fixup = self._need_fixup(
          self.tag_fixup_mode, svn_commit, source_groups)

        if not need_fixup:
            (source_revnum, source_lod, cvs_symbols) = source_groups[0]
            node = self._get_cset(source_lod, source_revnum)
            logger.verbose('tag %s is a simple copy of %s at r%d (%s)'
                           % (tag, source_lod, source_revnum, hgnode.short(node)))
        else:
            # Arbitrarily assign this tag to one of its source branches.  Most
            # of the time, there is only one source branch, so this is
            # perfectly correct.  For the oddball CVS tag with multiple source
            # branches, there's no good choice, but the fixup has to be on
            # *some* Mercurial branch.  (Either that or refuse to convert such
            # tags, which should perhaps be a configurable option.)
            lod = source_groups[0][1]

            logger.verbose('tag %s requires a fixup changeset' % tag)
            node = self._create_first_fixup(
              self.tag_fixup_mode, svn_commit, source_groups, lod)
            self.pending_fixup[lod] = (tag, node)

        self.tags[tag] = node
        logger.normal('tag %r: %d:%s' % (tag, len(self.repo)-1, hgnode.short(node)))
        self._update_symbol(source_groups)
        self._mirror.end_commit()

    def cleanup(self):
        self._close_pending_fixups()
        if self.tags:
            self._write_tags()

        # cvs2svn internally creates no cycles, so disables GC and prints warnings
        # if GC finds anything to collect.  But Mercurial's API makes no such
        # promise, so GC finds lots to collect.  So do a preemptive GC run to avoid
        # the warning from pass_manager.check_for_garbage().
        import gc
        nobj = gc.collect()
        logger.debug("Garbage collected %d objects" % nobj)

        DVCSOutputOption.cleanup(self)
        self.mirror_updater.finish()
        Ctx().revision_reader.finish()


    # -- Hooks for custom subclasses to override --

    def detect_merge(self, svn_commit, lod, parent1):
        """
        Determine if the CVS commit represented by SVN_COMMIT was a merge in CVS.
        If so, return the Mercurial changeset ID (in binary) of the changeset that
        should be its second parent; otherwise, return None.  The default
        implementation always returns None.

        SVN_COMMIT is a cvs2hg_lib.svn_commit.SVNPrimaryCommit object.

        LOD is an instance of either cvs2hg_lib.symbol.Trunk or
        cvs2hg_lib.symbol.Branch representing the CVS line of development where
        this commit happened.

        PARENT1 is the Mercurial changeset ID (binary) of the first parent.
        """
        return None


    # -- Private methods --

    def _analyze_cvs_revs(self, cvs_revs, post_node=None):
        cvs_rev_map = self._build_cvs_rev_map(cvs_revs)
        getfilectx = self._make_getfilectx(
          cvs_rev_map, Ctx().revision_reader, post_node)
        return (cvs_rev_map.keys(), getfilectx)

    def _build_cvs_rev_map(self, cvs_revs):
        cvs_rev_map = {}                  # map filename to CVSRevision
        for cvs_rev in cvs_revs:
            assert isinstance(cvs_rev, CVSRevision), \
                   "expected CVSRevision instance, not %r" % cvs_rev
            fn = cvs_rev.cvs_file.get_cvs_path()
            cvs_rev_map[fn] = cvs_rev
        return cvs_rev_map

    def _make_getfilectx(self, cvs_rev_map, revision_reader, post_node):
        def getfilectx(repo, memctx, path):
            cvs_rev = cvs_rev_map[path]
            if isinstance(cvs_rev, CVSRevisionDelete):
                return return_skipped_rev()
            elif isinstance(cvs_rev, CVSRevisionNoop):
                # This is a CVS "dead->dead" revision: do the same thing as svn
                # and git output do, i.e. keep the commit even though it changes
                # nothing (see CVSRevisionNoop docstring for rationale).
                return return_skipped_rev()
            elif isinstance(cvs_rev, (CVSRevisionChange, CVSRevisionAdd)):
                if post_node:
                    # The text has already been removed from cvs2svn's intermediary
                    # database.  Luckily it's in the output Mercurial repo!
                    data = repo[post_node][path].data()
                else:
                    data = self._get_revision_contents(revision_reader, cvs_rev)
            else:
                raise InternalError('Unexpected CVSRevision type: %r' % (cvs_rev,))

            return construct_memfilectx(
              repo, memctx, path, data,
              False,  # cvs doesn't do symlinks
              cvs_rev.cvs_file.executable,
              False)  # cvs doesn't do copies

        return getfilectx

    def _get_revision_contents(self, revision_reader, cvs_rev):
        """Return the complete contents of one revision of one file."""
        return revision_reader.get_content(cvs_rev)

    def _update_symbol(self, source_groups):
        for (source_revnum, source_lod, cvs_symbols) in source_groups:
            for cvs_symbol in cvs_symbols:
                self.mirror_updater.branch_file(cvs_symbol)

    def _get_unique_lod(self, lods, error_fmt):
        lods = set(lods)
        assert len(lods) == 1, error_fmt % (len(lods), ", ".join(map(str, lods)))
        return lods.pop()

    def _get_parent1(self, svn_commit, lod):
        try:
            return self.branch_head[lod]
        except KeyError:
            # This is rare: it should only happen in cases like empty CVS
            # trunk or non-trunk default branch (aka CVS vendor branch).
            return self.start_node

    def _get_parent2(self, lod, default=None):
        # If there is a tag fixup commit that has not been merged, make the
        # current changeset an artificial merge.  That way we don't have an
        # open head for every tag fixup.
        pending = self.pending_fixup.get(lod)
        if pending and default is None:
            (tag, node) = pending
            logger.debug("artificially merging fixup commit %s for tag %s"
                         % (hgnode.short(node), tag))
            del self.pending_fixup[lod]
            return node
        else:
            return default

    def _need_fixup(self, mode, svn_commit, source_groups):
        if mode == 'always':
            return True
        else:
            fixup_type = self._get_fixup_type(svn_commit, source_groups)
            if fixup_type == 'simple':
                return False
            elif fixup_type == 'complex':
                return True
            elif fixup_type == 'sloppy':
                # no fixup in sloppy mode, fixup in optional mode
                return (mode == 'optional')

    def _create_first_fixup(self, mode, svn_commit, source_groups, lod):

        source_cset = self._get_source_changesets(source_groups)

        # Figure out the files we have to delete in the fixup (i.e., those
        # that are present in some source revision but that don't have the
        # CVS tag).  (In sloppy fixup mode, we pretend the CVS tag covered
        # the whole tree, so we don't delete files in the fixup.)
        not_tagged = []
        if mode != 'sloppy':
            for (source_revnum, source_lod, cvs_symbols) in source_groups:
                node = self._get_cset(source_lod, source_revnum)
                cctx = self.repo[node]
                not_tagged += [fn for fn in cctx if fn not in source_cset]

        # If we have 1 source group, then this is obviously the right choice
        # for parent1.  If >1, pick an arbitrary one.
        parent1 = self._get_cset(source_groups[0][1], source_groups[0][0])
        parent2 = (self.detect_merge(svn_commit, lod, parent1) or
                   self._get_parent2(lod))

        # Don't ask Mercurial to commit all the files that are unchanged relative to
        # parent1 -- that would be a waste of time and I/O.
        for (filename, node) in source_cset.items():
            if node == parent1:
                del source_cset[filename]

        return self._create_fixup(svn_commit,
                                  (parent1, parent2),
                                  source_cset,
                                  source_cset.keys() + not_tagged,
                                  lod)

    def _create_second_coming(self, svn_commit, source_groups, lod):
        # If a branch was created on different files at different times, we
        # have a "split" branch.  We need a second (or third, etc.) fixup
        # commit for this second coming of the branch.  It's pretty similar
        # to the initial fixup commit except that it's descended from the
        # initial fixup.  And we don't have to worry about deleting files:
        # this fixup commit can only add files to the branch.
        source_cset = self._get_source_changesets(source_groups)

        # For the second creation of a branch, make the second fixup a child
        # of the previous branch head.  It looks prettier that way, and
        # Mercurial repos normally don't have a changeset on an existing
        # branch whose first parent is on another branch.
        parent1 = self.branch_head[lod]
        parent2 = self._get_parent2(lod)

        return self._create_fixup(svn_commit,
                                  (parent1, parent2),
                                  source_cset,
                                  source_cset.keys(),
                                  lod)

    def _get_source_changesets(self, source_groups):
        """Analyze the source_groups list and return a mapping from CVS filename to
        node id, telling us where to get the content of every tagged revision."""

        source_cset = {}

        for (source_revnum, source_lod, cvs_symbols) in source_groups:
            node = self._get_cset(source_lod, source_revnum)

            for cvs_symbol in cvs_symbols:
                filename = cvs_symbol.cvs_file.get_cvs_path()
                assert filename not in source_cset
                source_cset[filename] = node

        return source_cset

    def _create_fixup(self, svn_commit, parents, source_cset, files, lod):

        def getfilectx(repo, memctx, path):
            try:
                node = source_cset[path]
            except KeyError:
                # path does not have the tag: delete it in the fixup commit
                return return_skipped_rev()
            fctx = self.repo.filectx(path, changeid=node)
            flags = fctx.flags()
            return construct_memfilectx(
              repo, memctx, path, fctx.data(),
              False, # cvs doesn't do symlinks
              'x' in flags,
              False) # cvs doesn't do copies

        node = self._commit_fixup(svn_commit, parents, files, getfilectx, lod)
        logger.verbose("added fixup changeset %s (%d files) for symbol %r"
                       % (hgnode.short(node), len(files), svn_commit.symbol.name))

        # XXX should we add this changeset to self.changesets?
        # if so, on which LOD?

        return node

    def _get_cset(self, source_lod, revnum):
        # XXX very similar to GitOutputOption._get_source_mark()
        csets = self.changesets[source_lod]
        idx = bisect.bisect_left(csets, (revnum + 1,)) - 1
        return csets[idx][1]

    def _get_author(self, svn_commit):
        cvs_author = svn_commit.get_author()
        return self.author_transforms.get(cvs_author, cvs_author)

    def _get_hg_extra(self, lod):
        if isinstance(lod, Trunk):
            return None
        elif isinstance(lod, Branch):
            return {'branch': lod.name}
        else:
            raise AssertionError("invalid LOD for Mercurial branch: must be "
                                 "trunk or branch, not %r" % lod)

    def _get_hg_date(self, svn_commit):
        tz = self.timezone
        if isinstance(tz, datetime.tzinfo):
            timestamp = datetime.datetime.fromtimestamp(svn_commit.date)
            tzdelta = tz.localize(timestamp).utcoffset()
            # WTF: is this *really* the only way to get total seconds from tzdelta?
            tzoffset = tzdelta.days*3600*24 + tzdelta.seconds
        elif isinstance(tz, int):           # second east of UTC
            tzoffset = tz

        # N.B. Mercurial uses seconds *west* of UTC, hence -tzoffset.
        return "%d %d" % (svn_commit.date, -tzoffset)

    # The multitude of _commit() methods looks a bit silly, but it allows
    # subclasses to override each type of commit as required.

    def _commit_primary(self, svn_commit, parents, filenames, getfilectx, lod):
        return self._commit(svn_commit, parents, filenames, getfilectx, lod)

    def _commit_post(self, svn_commit, parents, filenames, getfilectx, lod):
        return self._commit(svn_commit, parents, filenames, getfilectx, lod)

    def _commit_fixup(self, svn_commit, parents, filenames, getfilectx, lod):
        return self._commit(svn_commit, parents, filenames, getfilectx, lod)

    def _commit(self, svn_commit, parents, filenames, getfilectx, lod):
        mctx = context.memctx(
          self.repo,
          parents,
          svn_commit.get_log_msg(),
          filenames,
          getfilectx,
          user=self._get_author(svn_commit),
          date=self._get_hg_date(svn_commit),
          extra=self._get_hg_extra(lod))
        return self._commit_memctx(mctx)

    def _commit_memctx(self, mctx):
        # XXX should I be wrapping my txn in weakref.proxy()?
        txn = self.repo_transaction()
        try:
            node = self.repo.commitctx(mctx)
            txn.close()
        finally:
            del txn
        return node

    def _close_pending_fixups(self):
        for (lod, pending) in self.pending_fixup.items():
            (tag, parent2) = pending
            parent1 = self.branch_head[lod]
            message = ("artificial changeset: close fixup head %s for tag %s"
                       % (hgnode.short(parent2), tag))
            mctx = context.memctx(self.repo,
                                  (parent1, parent2),
                                  message,
                                  [],
                                  None,
                                  user=Ctx().username,
                                  extra=self._get_hg_extra(lod))
            node = self._commit_memctx(mctx)
            self.changesets[lod].append((None, node))
            self.branch_head[lod] = node
            logger.verbose("closed fixup head for tag %s with changeset %s"
                           % (tag, hgnode.short(node)))

    def _write_tags(self):
        # XXX there is a somewhat smarter implementation of this in
        # hgext.convert.hg.puttags() (e.g. this code clobbers any existing
        # tags, so is not friendly to appending changesets to an existing
        # hg repo)
        data = "\n".join(["%s %s" % (hgnode.hex(node), tag)
                          for (tag, node) in self.tags.iteritems()])
        data += "\n"
        def getfilectx(repo, memctx, path):
            return construct_memfilectx(repo, memctx, path, data, False, False, None)

        try:
            parent1 = self.repo.lookup("default")
            extra = {}
        except RepoError:
            # Empty trunk in CVS.  Assume this is deliberate and do not create
            # Mercurial default branch; just add .hgtags after tip and keep it
            # on the same branch.
            parent1 = self.repo.lookup("tip")
            extra = {'branch': self.repo[parent1].branch()}

        parents = (parent1, self._get_parent2(None))
        mctx = context.memctx(self.repo,
                              parents,
                              "convert CVS tags",
                              [".hgtags"],
                              getfilectx,
                              user=Ctx().username,
                              extra=extra)
        self._commit_memctx(mctx)
        logger.normal("converted tags with changeset %s" % hgnode.short(node))


class ClobberHgOutputOption(HgOutputOption):
    """An OutputOption that creates a new Mercurial repository,
    unconditionally deleting any existing directory or file of the
    same name."""

    def check_repo(self):
        pass

    def open_repo(self):
        if os.path.exists(self.repo_dir):
            logger.verbose("Removing target '%s'" % self.repo_dir)
            shutil.rmtree(self.repo_dir)
        HgOutputOption.open_repo(self)

class ExistingHgOutputOption(HgOutputOption):
    """An OutputOption that appends changesets to an existing Mercurial
    repository.  The output repository must already exist."""

    def check_repo(self):
        if not os.path.isdir(os.path.join(self.repo_dir, '.hg')):
            raise FatalError("directory '%s' does not contain a Mercurial repository"
                             % self.repo_dir)

    def open_repo(self):
        try:
            self.repo = hg.repository(self.ui, self.repo_dir, create=False)
        except RepoError as err:
            raise FatalError(str(err))

        # Hmmm: this mirrors logic from _write_tags().
        try:
            self.start_node = self.repo.lookup('default')
        except RepoError:
            self.start_node = self.repo.lookup('tip')
