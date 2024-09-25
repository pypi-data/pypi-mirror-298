#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run_tests.py:  test suite for cvs2hg
#
#  Run:
#      run_tests.py -h
#  for list of options.
#
# ====================================================================
# Copyright (c) 2000-2009 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
######################################################################

# pylint: disable=line-too-long,fixme,unused-variable,too-many-locals,broad-except,import-outside-toplevel,too-many-arguments,missing-function-docstring,wrong-import-position

from __future__ import print_function
# General modules
import sys
import shutil
import stat
import re
import os
import time
import datetime
import os.path
import locale
import textwrap
import calendar
import types
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from difflib import Differ
try:
    import cvs2hg_test
    from cvs2hg_test import Failure
    from cvs2hg_test.main import safe_rmtree
    from cvs2hg_test.testcase import TestCase
    from cvs2hg_test.testcase import XFail, Wimp
finally:
    # This script needs to run in the correct directory.  Make sure we're there.
    if not (os.path.exists('cvs2hg') and os.path.exists('test-data')):
        sys.stderr.write("error: I need to be run in the directory containing "
                         "'cvs2hg' and 'test-data'.\n")
        sys.exit(1)

from mercurial import context, __version__ as hgversion, scmutil
context.memctx
have_hg = True

cvs2hg = os.path.abspath('cvs2hg')

test_data_dir = 'test-data'
tmp_dir = 'test-temporary-tmp-dir'


# -------------------------------------------------------------------------
# Compatibility
# -------------------------------------------------------------------------

def _mercurial_version_tuple():
    import mercurial.util
    import re
    try:
        return mercurial.util.versiontuple()
    except:
        # Simplified version of actual versiontuple (we don't care about minors…)
        ver = mercurial.util.version()
        m = re.match(br'(\d+(?:\.\d+){,2})[\+-]?(.*)', ver)
        if m:
            return tuple([int(x) for x in m.group(1).split('.')])
        else:
            return (0,)


mercurial_version = _mercurial_version_tuple()


if sys.version_info < (3, 0):
    def bytes_to_native(txt):
        return txt
else:
    def bytes_to_native(txt):
        return txt.decode()


# ----------------------------------------------------------------------
# Helpers.
# ----------------------------------------------------------------------


# The value to expect for svn:keywords if it is set:
KEYWORDS = 'Author Date Id Revision'


class RunProgramException(Failure):
    pass


class MissingErrorException(Failure):
    def __init__(self, error_re):
        Failure.__init__(
            self, "Test failed because no error matched '%s'" % (error_re,)
        )


def run_program(program, error_re, *varargs):
    """Run PROGRAM with VARARGS, return stdout as a list of lines.

    If there is any stderr and ERROR_RE is None, raise
    RunProgramException, and print the stderr lines if
    cvs2hg_test.main.options.verbose is true.

    If ERROR_RE is not None, it is a string regular expression that must
    match some line of stderr.  If it fails to match, raise
    MissingErrorExpection.
    """
    # FIXME: exit_code is currently ignored.
    exit_code, out, err = cvs2hg_test.main.run_command(program, 1, 0, *varargs)

    if error_re:
        # Specified error expected on stderr.
        if not err:
            raise MissingErrorException(error_re)
        else:
            for line in err:
                if re.match(error_re, line):
                    return out
            raise MissingErrorException(error_re)
    else:
        # No stderr allowed.
        if err:
            if cvs2hg_test.main.options.verbose:
                print('\n%s said:\n' % program)
                for line in err:
                    print(b'   ' + line, end=b'')
                print()
            raise RunProgramException(
                "Program execution failed. Executed program: {0} {1}\nStderr:\n    {2}".format(
                    program,
                    " ".join(varargs),
                    bytes_to_native(b"\n    ".join(x.rstrip(b"\n") for x in err))))

    return out


def run_script(script, error_re, *varargs):
    """Run Python script SCRIPT with VARARGS, returning stdout as a list
    of lines.

    If there is any stderr and ERROR_RE is None, raise
    RunProgramException, and print the stderr lines if
    cvs2hg_test.main.options.verbose is true.

    If ERROR_RE is not None, it is a string regular expression that must
    match some line of stderr.  If it fails to match, raise
    MissingErrorException.
    """
    # Use the same python that is running this script
    return run_program(sys.executable, error_re, script, *varargs)
    # On Windows, for an unknown reason, the cmd.exe process invoked by
    # os.system('sort ...') in cvs2svn receives invalid stdio handles, if
    # cvs2svn is started as "cvs2svn ...".  "python cvs2svn ..." avoids
    # this.  Therefore, the redirection of the output to the .s-revs file fails.
    # We no longer use the problematic invocation on any system, but this
    # comment remains to warn about this problem.


def run_hg(*varargs):
    """Run svn with VARARGS; return stdout as a list of lines.
    If there is any stderr, raise RunProgramException, and print the
    stderr lines if cvs2hg_test.main.options.verbose is true.
    """
    return run_program(cvs2hg_test.main.hg_binary, None, *varargs)


def repos_to_url(path_to_svn_repos):
    """Generate repository url."""
    rpath = os.path.abspath(path_to_svn_repos)
    if rpath[0] != '/':
        rpath = '/' + rpath
    return 'file://%s' % rpath.replace(os.sep, '/')


def svn_strptime(timestr):
    return time.strptime(timestr, '%Y-%m-%d %H:%M:%S')


class Log:
    def __init__(self, chg, symbols):
        """chg - mercurial changectx"""
        self.revision = chg.rev()
        self.author = chg.user()

        # Mercurial gives sth like (740382368.0, 0). Below we want
        # seconds from UTC.
        self.date = chg.date()[0]

        # The following symbols are used for string interpolation when
        # checking paths:
        self.symbols = symbols

        # Keys here are paths such as 'foo/bar', values are letter
        # codes such as 'M', 'A', and 'D'.
        self.changed_paths = {}

        # chg.status(par) works strangely, reversing information at many times
        # (confusion with status against workdir). Less official _buildstatus works nicely
        # and calculates proper delta
        status = scmutil.status([], [], [], [], [], [], [])
        mtch = None
        if mercurial_version < (4, 2):
            from mercurial import match as matchmod
            mtch = matchmod.match(root=None, cwd=None, patterns=[])
        status = chg._buildstatus(chg.parents()[0], status,
                                  mtch,
                                  False, False, False)

        if mercurial_version < (3, 3):
            # Here we have no nice object, but
            # [modified, added, removed, deleted, unknown, ignored, clean]
            # Let's emulate it
            class EmulatedStatus(object): pass
            st = EmulatedStatus()
            st.modified, st.added, st.removed, st.deleted, st.unknown, st.ignored, st.clean = status
            status = st

        for f in status.removed + status.deleted:
            self.changed_paths[f] = 'D'
        for f in status.added:
            self.changed_paths[f] = 'A'
        for f in status.modified:
            self.changed_paths[f] = 'M'
        self.status = status

        self.parents = [c.rev() for c in chg.parents()]
        self.branch = chg.branch()
        self.tags = list(chg.tags())

        self.msg = chg.description()

    def __str__(self):
        """Brief stringified information."""
        return "Log({rev},\n    added={added},\n    removed={removed},\n    modified={modified}, msg={descr})".format(
            rev=self.revision,
            # status=self.status,
            added=" ".join(self.status.added),
            modified=" ".join(self.status.modified),
            removed=" ".join(self.status.removed),
            descr=self.msg[:self.msg.find('\n')][:30])

    __repr__ = __str__

    def __cmp__(self, other):
        """Compare crucial attributes."""
        return cmp(self.revision, other.revision) or \
            cmp(self.author, other.author) or cmp(self.date, other.date) or \
            cmp(self.changed_paths, other.changed_paths) or \
            cmp(self.msg, other.msg)

    def get_path_op(self, path):
        """Return the operator for the change involving PATH.

        PATH is allowed to include string interpolation directives (e.g.,
        '%(trunk)s'), which are interpolated against self.symbols.  Return
        None if there is no record for PATH.
        """
        return self.changed_paths.get(path % self.symbols)

    def check_msg(self, msg):
        """Verify that this Log's message starts with the specified MSG."""
        if self.msg.find(msg) != 0:
            raise Failure(
                "Revision {rev} log message was:\n{msg}\n\n"
                "It should have begun with:\n{exp}\n\n".format(
                    rev=self.revision, msg=self.msg, exp=msg))

    def check_branch(self, branch):
        if branch != self.branch:
            raise Failure("Branch mismatch at {rev}: expected {exp}, actual {act}".format(
                exp=branch, rev=self.revision, act=self.branch))

    def check_tag(self, tag):
        if tag is not None and tag != 'None':
            if tag not in self.tags:
                raise Failure("Tag mismatch at {rev}: expected {exp}, actual {act}".format(
                    exp=tag, rev=self.revision, act=self.tags))
        else:
            if self.tags:
                raise Failure("Unexpected tag(s) at {rev}: {tags}".format(
                    rev=self.revision, tags=self.tags))

    def check_change(self, path, op):
        """Verify that this Log includes a change for PATH with operator OP.

        PATH is allowed to include string interpolation directives (e.g.,
        '%(trunk)s'), which are interpolated against self.symbols.
        """
        path = path % self.symbols
        found_op = self.changed_paths.get(path, None)
        if found_op is None:
            raise Failure(
                "Revision %d does not include change for path %s "
                "(it should have been %s).\n"
                % (self.revision, path, op,)
            )
        if found_op != op:
            raise Failure(
                "Revision %d path %s had op %s (it should have been %s)\n"
                % (self.revision, path, found_op, op,)
            )

    def check_changes(self, changed_paths):
        """Verify that this Log has precisely the CHANGED_PATHS specified.

        CHANGED_PATHS is a sequence of tuples (path, op), where the paths
        strings are allowed to include string interpolation directives
        (e.g., '%(trunk)s'), which are interpolated against self.symbols.
        """
        cp = {}
        for (path, op) in changed_paths:
            cp[path % self.symbols] = op

        if self.changed_paths != cp:
            raise Failure(
                "Revision %d changed paths list was:\n%s\n\n"
                "It should have been:\n%s\n\n"
                % (self.revision, self.changed_paths, cp,)
            )

    def check(self, msg, changed_paths):
        """Verify that this Log has the MSG and CHANGED_PATHS specified.

        Convenience function to check two things at once.  MSG is passed
        to check_msg(); CHANGED_PATHS is passed to check_changes()."""

        self.check_msg(msg)
        self.check_changes(changed_paths)


class Logs(object):
    """Group of log entries keyed by revision."""
    def __init__(self):
        self._items = {}

    def add(self, chg, symbols):
        self._items[chg.rev()] = Log(chg, symbols)

    def count(self):
        return len(self._items)

    def revs(self):
        return list(self._items.keys())

    def parent_of(self, rev_no):
        lg = self._items[rev_no]
        parents = lg.parents
        if len(parents) != 1:
            raise ValueError("Revision {rev} has non-unique parents {par}".format(rev=rev_no, par=parents))
        return parents[0]

    def find_tag_log(self, tagname):
        """Search LOGS for a log message containing 'TAGNAME' and return the
        log in which it was found."""
        for i in xrange(len(self._items) - 1, -1, -1):
            if self._items[i].msg.find("'" + tagname + "'") != -1:
                return self._items[i]
        raise ValueError("Tag %s not found in logs" % tagname)

    def check_msg(self, revno, msg):
        try:
            self._items[revno].check_msg(msg)
        except Failure as fail:
            self._annotate_failure_with_msg(fail, revno)
            raise

    def check_change(self, revno, path, op):
        try:
            self._items[revno].check_change(path, op)
        except Failure as fail:
            self._annotate_failure_with_changes(fail, revno)
            raise

    def check_changes(self, revno, changed_paths):
        try:
            self._items[revno].check_changes(changed_paths)
        except Failure as fail:
            self._annotate_failure_with_changes(fail, revno)
            raise

    def _annotate_failure_with_msg(self, failure, revno):
        msg = "Note: nearby revisions messages:\n"
        for x in range(revno - 5, revno + 5):
            rv = self._items.get(x)
            if rv:
                msg += "  [{0}] {1}\n".format(x, rv.msg.replace("\n", "\\n"))
        failure.args = (failure.args[0] + msg,)

    def _annotate_failure_with_changes(self, failure, revno):
        msg = "Note: nearby revisions changes:\n"
        for x in range(revno - 5, revno + 5):
            rv = self._items.get(x)
            if rv:
                msg += "  [{0}]\n".format(x)
                if rv.status.added:
                    msg += "      A: " + " ".join(rv.status.added) + "\n"
                if rv.status.modified:
                    msg += "      M: " + " ".join(rv.status.modified) + "\n"
                if rv.status.removed or rv.status.deleted:
                    msg += "      D: " + " ".join(rv.status.removed + rv.status.deleted) + "\n"
        failure.args = (failure.args[0] + msg,)

    def check(self, revno, msg, changed_paths, branch='default', tag='None'):
        self.check_msg(revno, msg)
        self.check_changes(revno, changed_paths)
        self.check_branch(revno, branch)
        self.check_tag(revno, tag)
        # Not so, above we get better error messages
        # self._items[revno].check(msg, changed_paths)

    def check_branch(self, revno, branch):
        self._items[revno].check_branch(branch)

    def check_tag(self, revno, tag):
        self._items[revno].check_tag(tag)

    def check_logs_count(self, count):
        act_count = self.count()
        if act_count != count:
            fail = Failure("Unexpected logs count: {0} (expected {1})\n".format(act_count, count))
            self._annotate_failure_with_changes(fail, 4)
            raise fail

    def __getitem__(self, revno):
        return self._items[revno]

    def __str__(self):
        for no in sorted(self._items.keys()):
            print(self._items[no])
            print()


def parse_log(hg_repos, restrict_to_path, symbols, skip_fixup_commits=False):
    """Return Logs object (mostly a dictionary of Log objects, keyed on revision number,
    with some extras).

    Initialize created Log objects with SYMBOLS."""

    logs = Logs()

    from mercurial import ui, hg   # commands
    u = ui.ui()
    repo = hg.repository(u, hg_repos)
    for rev_no in repo:
        chg = repo[rev_no]
        if restrict_to_path:
            touched = any(x == restrict_to_path or x.startswith(restrict_to_path + '/')
                          for x in chg.files())
            if not touched:
                continue
            if skip_fixup_commits:
                if chg.description().startswith('fixup commit'):
                    continue
        this_log = Log(chg, symbols)
        assert this_log
        logs.add(chg, symbols)
    return logs

    # u.pushbuffer()
    # commands.log(u, repo)
    # output = u.popbuffer()


def erase(path):
    """Unconditionally remove PATH and its subtree, if any.  PATH may be
    non-existent, a file or symlink, or a directory."""
    if os.path.isdir(path):
        safe_rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


log_msg_text_wrapper = textwrap.TextWrapper(width=76, break_long_words=False)


def sym_log_msg(symbolic_name, is_tag=None):
    """Return the expected log message for a cvs2svn-synthesized revision
    creating branch or tag SYMBOLIC_NAME.
    """
    # This reproduces the logic in SVNSymbolCommit.get_log_msg().
    if is_tag:
        type = 'tag'
    else:
        type = 'branch'

    return log_msg_text_wrapper.fill(
        "fixup commit for {type} '{name}'".format(type=type, name=symbolic_name))


def make_conversion_id(
        name, args, passbypass, options_file=None, symbol_hints_file=None
):
    """Create an identifying tag for a conversion.

    The return value can also be used as part of a filesystem path.

    NAME is the name of the CVS repository.

    ARGS are the extra arguments to be passed to cvs2svn.

    PASSBYPASS is a boolean indicating whether the conversion is to be
    run one pass at a time.

    If OPTIONS_FILE is specified, it is an options file that will be
    used for the conversion.

    If SYMBOL_HINTS_FILE is specified, it is a symbol hints file that
    will be used for the conversion.

    The 1-to-1 mapping between cvs2svn command parameters and
    conversion_ids allows us to avoid running the same conversion more
    than once, when multiple tests use exactly the same conversion."""

    conv_id = name

    args = args[:]

    if passbypass:
        args.append('--passbypass')

    if symbol_hints_file is not None:
        args.append('--symbol-hints=%s' % (symbol_hints_file,))

    # There are some characters that are forbidden in filenames, and
    # there is a limit on the total length of a path to a file.  So use
    # a hash of the parameters rather than concatenating the parameters
    # into a string.
    if args:
        conv_id += "-" + md5('\0'.join(args)).hexdigest()

    # Some options-file based tests rely on knowing the paths to which
    # the repository should be written, so we handle that option as a
    # predictable string:
    if options_file is not None:
        conv_id += '--options=%s' % (options_file,)

    return conv_id


class Conversion:
    """A record of a cvs2hg conversion.

    Fields:

      conv_id -- the conversion id for this Conversion.

      name -- a one-word name indicating the involved repositories.

      dumpfile -- the name of the hg bundle created by the conversion
          (if the DUMPFILE constructor argument was used); otherwise,
          None.

      repos -- the path to the hg repository.  Unset if DUMPFILE was
          specified.

      logs -- Logs object (dictionary of Log instances, as returned by parse_log()).
          Unset if DUMPFILE was specified.

      symbols -- a dictionary of symbols used for string interpolation
          in path names.

      stdout -- a list of lines written by cvs2hg to stdout

      _wc -- the basename of the working copy (within tmp_dir).
          Unset if DUMPFILE was specified.

      _wc_path -- the path to the working copy, if it has already
          been created; otherwise, None.  (The working copy is created
          lazily when get_wc() is called.)  Unset if DUMPFILE was
          specified.

      _wc_tree -- the tree built from the working copy, if it has
          already been created; otherwise, None.  The tree is created
          lazily when get_wc_tree() is called.)  Unset if DUMPFILE was
          specified.
    """

    # The number of the last cvs2svn pass (determined lazily by
    # get_last_pass()).
    last_pass = None

    @classmethod
    def get_last_pass(cls):
        """Return the number of cvs2svn's last pass."""
        if cls.last_pass is None:
            out = run_script(cvs2hg, None, '--help-passes')
            cls.last_pass = int(out[-1].split()[0])
        return cls.last_pass

    def __init__(
            self, conv_id, name, error_re, passbypass, symbols, args,
            options_file=None, symbol_hints_file=None, dumpfile=None,
    ):
        self.conv_id = conv_id
        self.name = name
        self.symbols = symbols
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        cvsrepos = os.path.join(test_data_dir, '%s-cvsrepos' % self.name)

        if dumpfile:
            self.dumpfile = os.path.join(tmp_dir, dumpfile)
            # Clean up from any previous invocations of this script.
            erase(self.dumpfile)
        else:
            self.dumpfile = None
            self.repos = os.path.join(tmp_dir, '%s-hg' % self.conv_id)

            # Clean up from any previous invocations of this script.
            erase(self.repos)

        args = list(args)
        if options_file:
            self.options_file = os.path.join(cvsrepos, options_file)
            args.extend([
                '--options=%s' % self.options_file,
            ])
            assert not symbol_hints_file
        else:
            self.options_file = None
            if tmp_dir != 'test-temporary-tmp-dir':
                # Only include this argument if it differs from cvs2svn's default:
                args.extend([
                    '--tmpdir=%s' % tmp_dir,
                ])

            if symbol_hints_file:
                self.symbol_hints_file = os.path.join(cvsrepos, symbol_hints_file)
                args.extend([
                    '--symbol-hints=%s' % self.symbol_hints_file,
                ])

            if self.dumpfile:
                args.extend(['--dumpfile=%s' % (self.dumpfile,)])
            else:
                args.extend(['--hgrepos', self.repos])
            args.extend([cvsrepos])

        if passbypass:
            self.stdout = []
            for p in range(1, self.get_last_pass() + 1):
                self.stdout += run_script(cvs2hg, error_re, '-p', str(p), *args)
        else:
            self.stdout = run_script(cvs2hg, error_re, *args)

        if self.dumpfile:
            if not os.path.isfile(self.dumpfile):
                raise Failure(
                    "Dumpfile not created: '%s'"
                    % os.path.join(os.getcwd(), self.dumpfile)
                )
        else:
            if os.path.isdir(self.repos):
                self.logs = parse_log(self.repos, None, self.symbols)
            elif error_re is None:
                raise Failure(
                    "Repository not created: '%s'"
                    % os.path.join(os.getcwd(), self.repos)
                )

    def output_found(self, pattern):
        """Return True if PATTERN matches any line in self.stdout.

        PATTERN is a regular expression pattern as a string.
        """
        pattern_re = re.compile(pattern)

        for line in self.stdout:
            if pattern_re.match(line):
                # We found the pattern that we were looking for.
                return 1
        else:
            return 0

    def get_wc(self, *args):
        """Return the path to the svn working copy, or a path within the WC.

        If a working copy has not been created yet, create it now.

        If ARGS are specified, then they should be strings that form
        fragments of a path within the WC.  They are joined using
        os.path.join() and appended to the WC path.
        """
        run_hg("update", "--cwd", self.repos)
        return os.path.join(self.repos, *args)

    def get_wc_tree(self):
        if self._wc_tree is None:
            self._wc_tree = cvs2hg_test.tree.build_tree_from_wc(self.get_wc(), 1)
        return self._wc_tree

    def path_exists(self, *args):
        """Return True if the specified path exists within the repository.

        (The strings in ARGS are first joined into a path using
        os.path.join().)
        """
        return os.path.exists(self.get_wc(*args))


class DVCSConversion:
    """A record of a cvs2{git,hg} conversion.

    Fields:

      name -- a one-word name indicating the CVS repository to be converted.

      stdout -- a list of lines written by cvs2svn to stdout."""

    def __init__(self, name, script, error_re, args, options_file=None):
        self.name = name
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        cvsrepos = os.path.join(test_data_dir, '%s-cvsrepos' % self.name)

        args = list(args)
        if options_file:
            self.options_file = os.path.join(cvsrepos, options_file)
            args.extend([
                '--options=%s' % self.options_file,
            ])
        else:
            self.options_file = None

        self.stdout = run_script(script, error_re, *args)


# Cache of conversions that have already been done.  Keys are conv_id;
# values are Conversion instances.
already_converted = {}


def ensure_conversion(
        name, error_re=None, passbypass=None,
        args=None, options_file=None, symbol_hints_file=None, dumpfile=None,
):
    """Convert CVS repository NAME to HG, but only if it has not
    been converted before by this invocation of this script.  If it has
    been converted before, return the Conversion object from the
    previous invocation.

    If no error, return a Conversion instance.

    If ERROR_RE is a string, it is a regular expression expected to
    match some line of stderr printed by the conversion.  If there is an
    error and ERROR_RE is not set, then raise Failure.

    If PASSBYPASS is set, then cvs2svn is run multiple times, each time
    with a -p option starting at 1 and increasing to a (hardcoded) maximum.

    NAME is just one word.  For example, 'main' would mean to convert
    './test-data/main-cvsrepos', and after the conversion, the resulting
    Mercurial repository would be in './test-temporary-tmp-dir/main-hg'.

    Any other options to pass to cvs2svn should be in ARGS, each element
    being one option, e.g., '--trunk-only'.  If the option takes an
    argument, include it directly, e.g., '--mime-types=PATH'.  Arguments
    are passed to cvs2svn in the order that they appear in ARGS.

    If OPTIONS_FILE is specified, then it should be the name of a file
    within the main directory of the cvs repository associated with this
    test.  It is passed to cvs2svn using the --options option (which
    suppresses some other options that are incompatible with --options).

    If SYMBOL_HINTS_FILE is specified, then it should be the name of a
    file within the main directory of the cvs repository associated with
    this test.  It is passed to cvs2svn using the --symbol-hints option.

    If DUMPFILE is specified, then it is the name of a dumpfile within
    the temporary directory to which the conversion output should be
    written."""

    if args is None:
        args = []
    else:
        args = list(args)

    conv_id = make_conversion_id(
        name, args, passbypass, options_file, symbol_hints_file
    )

    if conv_id not in already_converted:
        try:
            # Run the conversion and store the result for the rest of this
            # session:
            already_converted[conv_id] = Conversion(
                conv_id, name, error_re, passbypass,
                {},
                args, options_file, symbol_hints_file, dumpfile,
            )
        except Failure:
            # Remember the failure so that a future attempt to run this conversion
            # does not bother to retry, but fails immediately.
            already_converted[conv_id] = None
            raise

    conv = already_converted[conv_id]
    if conv is None:
        raise Failure()
    return conv


class Cvs2HgTestFunction(TestCase):
    """A TestCase based on a naked Python function object.

    FUNC should be a function that returns None on success and throws an
    cvs2hg_test.Failure exception on failure.  It should have a brief
    docstring describing what it does (and fulfilling certain
    conditions).  FUNC must take no arguments.

    This class is almost identical to cvs2hg_test.testcase.FunctionTestCase,
    except that the test function does not require a sandbox and does
    not accept any parameter (not even sandbox=None).

    This class can be used as an annotation on a Python function.

    """

    def __init__(self, func):
        # it better be a function that accepts no parameters and has a
        # docstring on it.
        assert isinstance(func, types.FunctionType)

        name = func.__name__

        assert func.__code__.co_argcount == 0, \
            '%s must not take any arguments' % name

        doc = func.__doc__.strip()
        assert doc, '%s must have a docstring' % name

        # enforce stylistic guidelines for the function docstrings:
        # - no longer than 50 characters
        # - should not end in a period
        # - should not be capitalized
        assert len(doc) <= 50, \
            "%s's docstring must be 50 characters or less" % name
        assert doc[-1] != '.', \
            "%s's docstring should not end in a period" % name
        assert doc[0].lower() == doc[0], \
            "%s's docstring should not be capitalized" % name

        TestCase.__init__(self, doc="[" + name + "] " + doc)
        self.func = func

    def get_function_name(self):
        return self.func.__name__

    def get_sandbox_name(self):
        return None

    def run(self, sandbox):
        return self.func()


class Cvs2HgTestFunction(Cvs2HgTestFunction):
    """Same as Cvs2HgTestFunction, but for test cases that should be
    skipped if Mercurial is not available.
    """
    def run(self, sandbox):
        if not have_hg:
            raise cvs2hg_test.Skip()
        else:
            return self.func()


class Cvs2HgTestCase(TestCase):
    def __init__(
            self, name, doc=None, variant=None,
            error_re=None, passbypass=None,
            args=None,
            options_file=None, symbol_hints_file=None, dumpfile=None,
    ):
        self.name = name

        if doc is None:
            # By default, use the first line of the class docstring as the
            # doc:
            doc = self.__doc__.splitlines()[0]

        if variant is not None:
            # Modify doc to show the variant.  Trim doc first if necessary
            # to stay within the 50-character limit.
            suffix = '...variant %s' % (variant,)
            doc = doc[:50 - len(suffix)] + suffix

        TestCase.__init__(self, doc="[" + type(self).__name__ + "] " + doc)

        self.error_re = error_re
        self.passbypass = passbypass
        self.args = args
        self.options_file = options_file
        self.symbol_hints_file = symbol_hints_file
        self.dumpfile = dumpfile

    def ensure_conversion(self):
        return ensure_conversion(
            self.name,
            error_re=self.error_re, passbypass=self.passbypass,
            args=self.args,
            options_file=self.options_file,
            symbol_hints_file=self.symbol_hints_file,
            dumpfile=self.dumpfile,
        )

    def get_sandbox_name(self):
        return None


# ----------------------------------------------------------------------
# Tests.
# ----------------------------------------------------------------------


@Cvs2HgTestFunction
def show_usage():
    "cvs2hg with no arguments shows usage"
    out = run_script(cvs2hg, None)
    if (len(out) > 2 and out[0].find('ERROR:') == 0 and out[1].find('DBM module')):
        print('cvs2hg cannot execute due to lack of proper DBM module.')
        print('Exiting without running any further tests.')
        sys.exit(1)
    if out[0].find('Usage:') < 0:
        raise Failure('Basic cvs2hg invocation failed.')


@Cvs2HgTestFunction
def cvs2hg_manpage():
    "generate a manpage for cvs2hg"
    out = run_script(cvs2hg, None, '--man')
    assert any('.TH CVS2HG' in line for line in out) 


@Cvs2HgTestFunction
def show_help_passes():
    "cvs2svn --help-passes shows pass information"
    out = run_script(cvs2svn, None, '--help-passes')
    if out[0].find('PASSES') < 0:
        raise Failure('cvs2svn --help-passes failed.')


@Cvs2HgTestFunction
def attr_exec():
    "detection of the executable flag"
    if sys.platform == 'win32':
        raise cvs2hg_test.Skip()
    conv = ensure_conversion('main')
    st = os.stat(conv.get_wc('single-files', 'attr-exec'))
    if not st.st_mode & stat.S_IXUSR:
        raise Failure()


@Cvs2HgTestFunction
def space_fname():
    "conversion of filename with a space"
    conv = ensure_conversion('main')
    if not conv.path_exists('single-files', 'space fname'):
        raise Failure()


@Cvs2HgTestFunction
def two_quick():
    "two commits in quick succession"
    conv = ensure_conversion('main')
    logs = parse_log(conv.repos, os.path.join('single-files', 'twoquick'), {}, skip_fixup_commits=True)
    if logs.count() != 2:
        raise Failure("Expected 2 logs, got {0} ({1})".format(len(logs), logs))


class PruneWithCare(Cvs2HgTestCase):
    "prune, but never too much"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'main', **kw)

    def run(self, sbox):
        # Robert Pluim encountered this lovely one while converting the
        # directory src/gnu/usr.bin/cvs/contrib/pcl-cvs/ in FreeBSD's CVS
        # repository (see issue #1302).  Step 4 is the doozy:
        #
        #   revision 1:  adds trunk/blah/, adds trunk/blah/cookie
        #   revision 2:  adds trunk/blah/NEWS
        #   revision 3:  deletes trunk/blah/cookie
        #   revision 4:  deletes blah [re-deleting trunk/blah/cookie pruned blah!]
        #   revision 5:  does nothing
        #
        # After fixing cvs2svn, the sequence (correctly) looks like this:
        #
        #   revision 1:  adds trunk/blah/, adds trunk/blah/cookie
        #   revision 2:  adds trunk/blah/NEWS
        #   revision 3:  deletes trunk/blah/cookie
        #   revision 4:  does nothing [because trunk/blah/cookie already deleted]
        #   revision 5:  deletes blah
        #
        # The difference is in 4 and 5.  In revision 4, it's not correct to
        # prune blah/, because NEWS is still in there, so revision 4 does
        # nothing now.  But when we delete NEWS in 5, that should bubble up
        # and prune blah/ instead.
        #
        # ### Note that empty revisions like 4 are probably going to become
        # ### at least optional, if not banished entirely from cvs2svn's
        # ### output.  Hmmm, or they may stick around, with an extra
        # ### revision property explaining what happened.  Need to think
        # ### about that.  In some sense, it's a bug in Subversion itself,
        # ### that such revisions don't show up in 'svn log' output.
        #
        # In the test below, 'trunk/full-prune/first' represents
        # cookie, and 'trunk/full-prune/second' represents NEWS.

        conv = self.ensure_conversion()

        # Confirm that revision 4 removes '/trunk/full-prune/first',
        # and that revision 6 removes '/trunk/full-prune'.
        #
        # Also confirm similar things about '/full-prune-reappear/...',
        # which is similar, except that later on it reappears, restored
        # from pruneland, because a file gets added to it.
        #
        # And finally, a similar thing for '/partial-prune/...', except that
        # in its case, a permanent file on the top level prevents the
        # pruning from going farther than the subdirectory containing first
        # and second.

        conv.logs.check_changes(3, (
            ('full-prune/first', 'D'),
            ('full-prune-reappear/sub/first', 'D'),
            ('partial-prune/sub/first', 'D'),
        ))

        conv.logs.check_changes(5, (
            ('full-prune/second', 'A'),
            ('full-prune-reappear/sub/second', 'A'),
            ('partial-prune/sub/first', 'A'),
        ))

        conv.logs.check_changes(29, (
            ('full-prune-reappear/appears-later', 'A'),
        ))


@Cvs2HgTestFunction
def interleaved_commits():
    "two interleaved trunk commits, different log msgs"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    # The initial import.
    rev = 26
    conv.logs.check(rev, 'Initial import.', (
        ('interleaved', 'A'),
        ('interleaved/1', 'A'),
        ('interleaved/2', 'A'),
        ('interleaved/3', 'A'),
        ('interleaved/4', 'A'),
        ('interleaved/5', 'A'),
        ('interleaved/a', 'A'),
        ('interleaved/b', 'A'),
        ('interleaved/c', 'A'),
        ('interleaved/d', 'A'),
        ('interleaved/e', 'A'),
    ), branch='default')

    def check_letters(rev):
        """Check if REV is the rev where only letters were committed."""

        conv.logs.check(rev, 'Committing letters only.', (
            ('interleaved/a', 'M'),
            ('interleaved/b', 'M'),
            ('interleaved/c', 'M'),
            ('interleaved/d', 'M'),
            ('interleaved/e', 'M'),
        ))

    def check_numbers(rev):
        """Check if REV is the rev where only numbers were committed."""

        conv.logs.check(rev, 'Committing numbers only.', (
            ('interleaved/1', 'M'),
            ('interleaved/2', 'M'),
            ('interleaved/3', 'M'),
            ('interleaved/4', 'M'),
            ('interleaved/5', 'M'),
        ))

    # One of the commits was letters only, the other was numbers only.
    # But they happened "simultaneously", so we don't assume anything
    # about which commit appeared first, so we just try both ways.
    rev += 1
    try:
        check_letters(rev)
        check_numbers(rev + 1)
    except Failure:
        check_numbers(rev)
        check_letters(rev + 1)


@Cvs2HgTestFunction
def simple_commits():
    "simple trunk commits"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    # The initial import.
    conv.logs.check(11, 'Initial import.', (    # W svn 13
        ('proj', 'A'),
        ('proj/default', 'A'),
        ('proj/sub1', 'A'),
        ('proj/sub1/default', 'A'),
        ('proj/sub1/subsubA', 'A'),
        ('proj/sub1/subsubA/default', 'A'),
        ('proj/sub1/subsubB', 'A'),
        ('proj/sub1/subsubB/default', 'A'),
        ('proj/sub2', 'A'),
        ('proj/sub2/default', 'A'),
        ('proj/sub2/subsubA', 'A'),
        ('proj/sub2/subsubA/default', 'A'),
        ('proj/sub3', 'A'),
        ('proj/sub3/default', 'A'),
    ))

    # The first commit.
    conv.logs.check(15, 'First commit to proj, affecting two files.', (  # svn 18
        ('proj/sub1/subsubA/default', 'M'),
        ('proj/sub3/default', 'M'),
    ))

    # The second commit.
    conv.logs.check(16, 'Second commit to proj, affecting all 7 files.', (  # svn 19
        ('proj/default', 'M'),
        ('proj/sub1/default', 'M'),
        ('proj/sub1/subsubA/default', 'M'),
        ('proj/sub1/subsubB/default', 'M'),
        ('proj/sub2/default', 'M'),
        ('proj/sub2/subsubA/default', 'M'),
        ('proj/sub3/default', 'M')
    ))


class SimpleTags(Cvs2HgTestCase):
    "simple tags and branches, no commits"

    def __init__(self, **kw):
        # See test-data/main-cvsrepos/proj/README.
        Cvs2HgTestCase.__init__(self, 'main', **kw)

    def run(self, sbox):
        conv = self.ensure_conversion()

        # Verify the copy source for the tags we are about to check
        # No need to verify the copyfrom revision, as simple_commits did that
        conv.logs.check(11, 'Initial import.', (
            ('proj/default', 'A'),
            ('proj/sub1/default', 'A'),
            ('proj/sub1/subsubA/default', 'A'),
            ('proj/sub1/subsubB/default', 'A'),
            ('proj/sub2/default', 'A'),
            ('proj/sub2/subsubA/default', 'A'),
            ('proj/sub3/default', 'A'),
        ))

        # Tag on rev 1.1.1.1 of all files in proj
        conv.logs.check(12, sym_log_msg('B_FROM_INITIALS'), (
            ('single-files', 'D'),
            ('partial-prune', 'D'),
        ), branch='B_FROM_INITIALS')

        # The same, as a tag
        log = conv.logs.find_tag_log('T_ALL_INITIAL_FILES')
        log.check(sym_log_msg('T_ALL_INITIAL_FILES', 1), (
            ('/(tags)s/T_ALL_INITIAL_FILES' + fromstr, 'A'),
        ), tag='T_ALL_INITIAL_FILES', branch='B_FROM_INITIALS')

        # Tag on rev 1.1.1.1 of all files in proj, except one
        log = conv.logs.find_tag_log('T_ALL_INITIAL_FILES_BUT_ONE')
        log.check(sym_log_msg('T_ALL_INITIAL_FILES_BUT_ONE', 1), (
            ('/(tags)s/T_ALL_INITIAL_FILES_BUT_ONE', 'A'),
            ('/(tags)s/T_ALL_INITIAL_FILES_BUT_ONE/proj/sub1/subsubB', 'D'),
        ), tag='T_ALL_INITIAL_FILES_BUT_ONE', branch='B_FROM_INITIALS')

        # The same, as a branch
        conv.logs.check(17, sym_log_msg('B_FROM_INITIALS_BUT_ONE'), (
            ('proj/sub1/subsubB', 'D'),
        ), branch='B_FROM_INITIALS_BUT_ONE')


@Cvs2HgTestFunction
def simple_branch_commits():
    "simple branch commits"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    conv.logs.check(19, 'Modify three files, on branch B_MIXED.', (
        ('proj/default', 'M'),
        ('proj/sub1/default', 'M'),
        ('proj/sub2/subsubA/default', 'M'),
    ), branch='B_MIXED')


@Cvs2HgTestFunction
def mixed_time_tag():
    "mixed-time tag"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    log = conv.logs.find_tag_log('T_MIXED')
    log.check_changes((
        ('/(tags)s/T_MIXED (from /(branches)s/B_MIXED:20)', 'A'),
    ), branch='B_MIXED', tag='T_MIXED')


@Cvs2HgTestFunction
def mixed_time_branch_with_added_file():
    "mixed-time branch, and a file added to the branch"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    # A branch from the same place as T_MIXED in the previous test,
    # plus a file added directly to the branch
    conv.logs.check(20, sym_log_msg('B_MIXED'), (
        ('partial-prune', 'D'),
        ('single-files', 'D'),
    ), branch='B_MIXED')

    conv.logs.check(22, 'Add a file on branch B_MIXED.', (
        ('proj/sub2/branch_B_MIXED_only', 'A'),
    ), branch='B_MIXED')


@Cvs2HgTestFunction
def mixed_commit():
    "a commit affecting both trunk and a branch"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    conv.logs.check(24,
                    'A single commit affecting one file on branch B_MIXED '
                    'and one on trunk.', (
                        ('proj/sub2/default', 'M'),
                        ('proj/sub2/branch_B_MIXED_only', 'M'),
                    ), branch='B_MIXED')


@Cvs2HgTestFunction
def split_time_branch():
    "branch some trunk files, and later branch the rest"
    # See test-data/main-cvsrepos/proj/README.
    conv = ensure_conversion('main')

    # First change on the branch, creating it
    conv.logs.check(25, sym_log_msg('B_SPLIT'), (
        ('partial-prune', 'D'),
        ('single-files', 'D'),
        ('proj/sub1/subsubB', 'D'),
    ), branch='B_SPLIT')

    conv.logs.check(29, 'First change on branch B_SPLIT.', (
        ('proj/default', 'M'),
        ('proj/sub1/default', 'M'),
        ('proj/sub1/subsubA/default', 'M'),
        ('proj/sub2/default', 'M'),
        ('proj/sub2/subsubA/default', 'M'),
    ), branch='B_SPLIT')

    # A trunk commit for the file which was not branched
    conv.logs.check(30, 'A trunk change to sub1/subsubB/default.  '
                    'This was committed about an', (
                        ('proj/sub1/subsubB/default', 'M'),
                    ))

    # Add the file not already branched to the branch, with modification:w
    conv.logs.check(31, sym_log_msg('B_SPLIT'), (
        ('proj/sub1/subsubB '
         '(from proj/sub1/subsubB:30)', 'A'),
    ), branch='B_SPLIT')

    conv.logs.check(32, 'This change affects sub3/default and sub1/subsubB/default, on branch', (
        ('proj/sub1/subsubB/default', 'M'),
        ('proj/sub3/default', 'M'),
    ), branch='B_SPLIT')


@Cvs2HgTestFunction
def multiple_tags():
    "multiple tags referring to same revision"
    conv = ensure_conversion('main')
    if not conv.path_exists('tags', 'T_ALL_INITIAL_FILES', 'proj', 'default'):
        raise Failure()
    if not conv.path_exists(
            'tags', 'T_ALL_INITIAL_FILES_BUT_ONE', 'proj', 'default'):
        raise Failure()


@Cvs2HgTestFunction
def multiply_defined_symbols():
    "multiple definitions of symbol names"

    # We can only check one line of the error output at a time, so test
    # twice.  (The conversion only have to be done once because the
    # results are cached.)
    conv = ensure_conversion(
        'multiply-defined-symbols',
        error_re=(
            r"ERROR\: Multiple definitions of the symbol \'BRANCH\' .*\: "
            r"1\.2\.4 1\.2\.2"
        ),
    )
    conv = ensure_conversion(
        'multiply-defined-symbols',
        error_re=(
            r"ERROR\: Multiple definitions of the symbol \'TAG\' .*\: "
            r"1\.2 1\.1"
        ),
    )
    assert conv


@Cvs2HgTestFunction
def multiply_defined_symbols_renamed():
    "rename multiply defined symbols"

    conv = ensure_conversion(
        'multiply-defined-symbols',
        options_file='cvs2svn-rename.options',
    )
    assert conv


@Cvs2HgTestFunction
def multiply_defined_symbols_ignored():
    "ignore multiply defined symbols"

    conv = ensure_conversion(
        'multiply-defined-symbols',
        options_file='cvs2svn-ignore.options',
    )
    assert conv


@Cvs2HgTestFunction
def repeatedly_defined_symbols():
    "multiple identical definitions of symbol names"

    # If a symbol is defined multiple times but has the same value each
    # time, that should not be an error.

    conv = ensure_conversion('repeatedly-defined-symbols')
    assert conv


@Cvs2HgTestFunction
def bogus_tag():
    "conversion of invalid symbolic names"
    conv = ensure_conversion('bogus-tag')
    assert conv


@Cvs2HgTestFunction
def overlapping_branch():
    "ignore a file with a branch with two names"
    conv = ensure_conversion('overlapping-branch')

    if not conv.output_found('.*cannot also have name \'vendorB\''):
        raise Failure()

    conv.logs.check(2, 'imported', (
        ('nonoverlapping-branch', 'A'),
        ('overlapping-branch', 'A'),
    ))

    if len(conv.logs) != 2:
        raise Failure()


class PhoenixBranch(Cvs2HgTestCase):
    "convert a branch file rooted in a 'dead' revision"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'phoenix', **kw)

    def run(self, sbox):
        conv = self.ensure_conversion()
        conv.logs.check(8, 'This file was supplied by Jack Moffitt', (
            ('/%(branches)s/volsung_20010721', 'A'),
            ('/%(branches)s/volsung_20010721/phoenix', 'A'),
        ))
        conv.logs.check(9, 'This file was supplied by Jack Moffitt', (
            ('/%(branches)s/volsung_20010721/phoenix', 'M'),
        ))


# TODO: We check for 4 changed paths here to accomodate creating tags
# and branches in rev 1, but that will change, so this will
# eventually change back.
@Cvs2HgTestFunction
def ctrl_char_in_log():
    "handle a control char in a log message"
    # This was issue #1106.
    rev = 2
    conv = ensure_conversion('ctrl-char-in-log')
    conv.logs.check_changes(rev, (
        ('ctrl-char-in-log', 'A'),
    ))
    if conv.logs[rev].msg.find('\x04') < 0:
        raise Failure(
            "Log message of 'ctrl-char-in-log,v' (rev 2) is wrong.")


@Cvs2HgTestFunction
def overdead():
    "handle tags rooted in a redeleted revision"
    conv = ensure_conversion('overdead')
    assert conv


class NoTrunkPrune(Cvs2HgTestCase):
    "ensure that trunk doesn't get pruned"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'overdead', **kw)

    def run(self, sbox):
        conv = self.ensure_conversion()
        for rev in conv.logs.revs():
            rev_logs = conv.logs[rev]
            if rev_logs.get_path_op('/%(trunk)s') == 'D':
                raise Failure()


@Cvs2HgTestFunction
def double_delete():
    "file deleted twice, in the root of the repository"
    # This really tests several things: how we handle a file that's
    # removed (state 'dead') in two successive revisions; how we
    # handle a file in the root of the repository (there were some
    # bugs in cvs2svn's svn path construction for top-level files); and
    # the --no-prune option.
    conv = ensure_conversion(
        'double-delete', args=[
            '--trunk-only',
            # '--no-prune',  # no such option for hg
        ])

    path = 'twice-removed'
    rev = 2
    conv.logs.check(rev, 'Updated CVS', (
        (path, 'A'),
    ))
    conv.logs.check(rev + 1, 'Remove this file for the first time.', (
        (path, 'D'),
    ))
    conv.logs.check(rev + 2, 'Remove this file for the second time,', (
    ))


@Cvs2HgTestFunction
def split_branch():
    "branch created from both trunk and another branch"
    # See test-data/split-branch-cvsrepos/README.
    #
    # The conversion will fail if the bug is present, and
    # ensure_conversion will raise Failure.
    conv = ensure_conversion('split-branch')
    assert conv


@Cvs2HgTestFunction
def resync_misgroups():
    "resyncing should not misorder commit groups"
    # See test-data/resync-misgroups-cvsrepos/README.
    #
    # The conversion will fail if the bug is present, and
    # ensure_conversion will raise Failure.
    conv = ensure_conversion('resync-misgroups')
    assert conv


class TaggedBranchAndTrunk(Cvs2HgTestCase):
    "allow tags with mixed trunk and branch sources"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'tagged-branch-n-trunk', **kw)

    def run(self, sbox):
        conv = self.ensure_conversion()

        tags = conv.symbols.get('tags', 'tags')

        a_path = conv.get_wc(tags, 'some-tag', 'a.txt')
        b_path = conv.get_wc(tags, 'some-tag', 'b.txt')
        if not (os.path.exists(a_path) and os.path.exists(b_path)):
            raise Failure()
        if (open(a_path, 'r').read().find('1.24') == -1) \
           or (open(b_path, 'r').read().find('1.5') == -1):
            raise Failure()


@Cvs2HgTestFunction
def enroot_race():
    """never use the rev-in-progress as a copy source"""

    # See issue #1427 and r8544.
    conv = ensure_conversion('enroot-race')
    rev = 6
    conv.logs.check_changes(rev, (
        ('/%(branches)s/mybranch (from /%(trunk)s:5)', 'A'),
        ('/%(branches)s/mybranch/proj/a.txt', 'D'),
        ('/%(branches)s/mybranch/proj/b.txt', 'D'),
    ))
    conv.logs[rev + 1].check_changes((
        ('/%(branches)s/mybranch/proj/c.txt', 'M'),
        ('proj/a.txt', 'M'),
        ('proj/b.txt', 'M'),
    ))


@Cvs2HgTestFunction
def enroot_race_obo():
    """do use the last completed rev as a copy source"""
    conv = ensure_conversion('enroot-race-obo')
    conv.logs.check_change(3, '/%(branches)s/BRANCH (from /%(trunk)s:2)', 'A')
    if not len(conv.logs) == 3:
        raise Failure()


class BranchDeleteFirst(Cvs2HgTestCase):
    "correctly handle deletion as initial branch action"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'branch-delete-first', **kw)

    def run(self, sbox):
        # See test-data/branch-delete-first-cvsrepos/README.
        #
        # The conversion will fail if the bug is present, and
        # ensure_conversion would raise Failure.
        conv = self.ensure_conversion()

        branches = conv.symbols.get('branches', 'branches')

        # 'file' was deleted from branch-1 and branch-2, but not branch-3
        if conv.path_exists(branches, 'branch-1', 'file'):
            raise Failure()
        if conv.path_exists(branches, 'branch-2', 'file'):
            raise Failure()
        if not conv.path_exists(branches, 'branch-3', 'file'):
            raise Failure()


@Cvs2HgTestFunction
def nonascii_filenames():
    """non ascii files converted incorrectly"""
    # see issue #1255

    # on a en_US.iso-8859-1 machine this test fails with
    # svn: Can't recode ...
    #
    # as described in the issue

    # on a en_US.UTF-8 machine this test fails with
    # svn: Malformed XML ...
    #
    # which means at least it fails. Unfortunately it won't fail
    # with the same error...

    # mangle current locale settings so we know we're not running
    # a UTF-8 locale (which does not exhibit this problem)
    current_locale = locale.getlocale()
    new_locale = 'en_US.ISO8859-1'
    locale_changed = None

    # From http://docs.python.org/lib/module-sys.html
    #
    # getfilesystemencoding():
    #
    # Return the name of the encoding used to convert Unicode filenames
    # into system file names, or None if the system default encoding is
    # used. The result value depends on the operating system:
    #
    # - On Windows 9x, the encoding is ``mbcs''.
    # - On Mac OS X, the encoding is ``utf-8''.
    # - On Unix, the encoding is the user's preference according to the
    #   result of nl_langinfo(CODESET), or None if the
    #   nl_langinfo(CODESET) failed.
    # - On Windows NT+, file names are Unicode natively, so no conversion is
    #   performed.

    # So we're going to skip this test on Mac OS X for now.
    if sys.platform == "darwin":
        raise cvs2hg_test.Skip()

    try:
        # change locale to non-UTF-8 locale to generate latin1 names
        locale.setlocale(locale.LC_ALL,  # this might be too broad?
                         new_locale)
        locale_changed = 1
    except locale.Error:
        raise cvs2hg_test.Skip()

    try:
        srcrepos_path = os.path.join(test_data_dir, 'main-cvsrepos')
        dstrepos_path = os.path.join(test_data_dir, 'non-ascii-cvsrepos')
        if not os.path.exists(dstrepos_path):
            # create repos from existing main repos
            shutil.copytree(srcrepos_path, dstrepos_path)
            base_path = os.path.join(dstrepos_path, 'single-files')
            shutil.copyfile(os.path.join(base_path, 'twoquick,v'),
                            os.path.join(base_path, 'two\366uick,v'))
            new_path = os.path.join(dstrepos_path, 'single\366files')
            os.rename(base_path, new_path)

        conv = ensure_conversion('non-ascii', args=['--encoding=latin1'])
        assert conv
    finally:
        if locale_changed:
            locale.setlocale(locale.LC_ALL, current_locale)
        safe_rmtree(dstrepos_path)


class UnicodeTest(Cvs2HgTestCase):
    "metadata contains Unicode"

    warning_pattern = r'ERROR\: There were warnings converting .* messages'

    def __init__(self, name, warning_expected, **kw):
        if warning_expected:
            error_re = self.warning_pattern
        else:
            error_re = None

        Cvs2HgTestCase.__init__(self, name, error_re=error_re, **kw)
        self.warning_expected = warning_expected

    def run(self, sbox):
        try:
            # ensure the availability of the "utf_8" encoding:
            u'a'.encode('utf_8').decode('utf_8')
        except LookupError:
            raise cvs2hg_test.Skip()

        self.ensure_conversion()


class UnicodeAuthor(UnicodeTest):
    "author name contains Unicode"

    def __init__(self, warning_expected, **kw):
        UnicodeTest.__init__(self, 'unicode-author', warning_expected, **kw)


class UnicodeLog(UnicodeTest):
    "log message contains Unicode"

    def __init__(self, warning_expected, **kw):
        UnicodeTest.__init__(self, 'unicode-log', warning_expected, **kw)


@Cvs2HgTestFunction
def vendor_branch_sameness():
    "avoid spurious changes for initial revs"
    conv = ensure_conversion(
        'vendor-branch-sameness', args=['--keep-trivial-imports']
    )

    # The following files are in this repository:
    #
    #    a.txt: Imported in the traditional way; 1.1 and 1.1.1.1 have
    #           the same contents, the file's default branch is 1.1.1,
    #           and both revisions are in state 'Exp'.
    #
    #    b.txt: Like a.txt, except that 1.1.1.1 has a real change from
    #           1.1 (the addition of a line of text).
    #
    #    c.txt: Like a.txt, except that 1.1.1.1 is in state 'dead'.
    #
    #    d.txt: This file was created by 'cvs add' instead of import, so
    #           it has only 1.1 -- no 1.1.1.1, and no default branch.
    #           The timestamp on the add is exactly the same as for the
    #           imports of the other files.
    #
    #    e.txt: Like a.txt, except that the log message for revision 1.1
    #           is not the standard import log message.
    #
    # (Aside from e.txt, the log messages for the same revisions are the
    # same in all files.)
    #
    # We expect that only a.txt is recognized as an import whose 1.1
    # revision can be omitted.  The other files should be added on trunk
    # then filled to vbranchA, whereas a.txt should be added to vbranchA
    # then copied to trunk.  In the copy of 1.1.1.1 back to trunk, a.txt
    # and e.txt should be copied untouched; b.txt should be 'M'odified,
    # and c.txt should be 'D'eleted.

    rev = 2
    conv.logs.check(rev, 'Initial revision', (
        ('proj', 'A'),
        ('proj/b.txt', 'A'),
        ('proj/c.txt', 'A'),
        ('proj/d.txt', 'A'),
    ))

    conv.logs.check(rev + 1, sym_log_msg('vbranchA'), (
        ('/%(branches)s/vbranchA (from /%(trunk)s:2)', 'A'),
        ('/%(branches)s/vbranchA/proj/d.txt', 'D'),
    ))

    conv.logs.check(rev + 2, 'First vendor branch revision.', (
        ('/%(branches)s/vbranchA/proj/a.txt', 'A'),
        ('/%(branches)s/vbranchA/proj/b.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/c.txt', 'D'),
    ))

    conv.logs.check(rev + 3, 'This commit was generated by cvs2svn to compensate for changes in r4,', (
        ('proj/a.txt (from /%(branches)s/vbranchA/proj/a.txt:4)', 'A'),
        ('proj/b.txt (from /%(branches)s/vbranchA/proj/b.txt:4)', 'R'),
        ('proj/c.txt', 'D'),
    ))

    rev = 7
    conv.logs.check(rev, 'This log message is not the standard', (
        ('proj/e.txt', 'A'),
    ))

    conv.logs.check(rev + 2, 'First vendor branch revision', (
        ('/%(branches)s/vbranchB/proj/e.txt', 'M'),
    ))

    conv.logs.check(rev + 3, 'This commit was generated by cvs2svn to compensate for changes in r9,', (
        ('proj/e.txt (from /%(branches)s/vbranchB/proj/e.txt:9)', 'R'),
    ))


@Cvs2HgTestFunction
def vendor_branch_trunk_only():
    "handle vendor branches with --trunk-only"
    conv = ensure_conversion('vendor-branch-sameness', args=['--trunk-only'])

    rev = 2
    conv.logs.check(rev, 'Initial revision', (
        ('proj', 'A'),
        ('proj/b.txt', 'A'),
        ('proj/c.txt', 'A'),
        ('proj/d.txt', 'A'),
    ))

    conv.logs.check(rev + 1, 'First vendor branch revision', (
        ('proj/a.txt', 'A'),
        ('proj/b.txt', 'M'),
        ('proj/c.txt', 'D'),
    ))

    conv.logs.check(rev + 2, 'This log message is not the standard', (
        ('proj/e.txt', 'A'),
    ))

    conv.logs.check(rev + 3, 'First vendor branch revision', (
        ('proj/e.txt', 'M'),
    ))


@Cvs2HgTestFunction
def default_branches():
    "handle default branches correctly"
    conv = ensure_conversion('default-branches')

    # There are seven files in the repository:
    #
    #    a.txt:
    #       Imported in the traditional way, so 1.1 and 1.1.1.1 are the
    #       same.  Then 1.1.1.2 and 1.1.1.3 were imported, then 1.2
    #       committed (thus losing the default branch "1.1.1"), then
    #       1.1.1.4 was imported.  All vendor import release tags are
    #       still present.
    #
    #    b.txt:
    #       Like a.txt, but without rev 1.2.
    #
    #    c.txt:
    #       Exactly like b.txt, just s/b.txt/c.txt/ in content.
    #
    #    d.txt:
    #       Same as the previous two, but 1.1.1 branch is unlabeled.
    #
    #    e.txt:
    #       Same, but missing 1.1.1 label and all tags but 1.1.1.3.
    #
    #    deleted-on-vendor-branch.txt,v:
    #       Like b.txt and c.txt, except that 1.1.1.3 is state 'dead'.
    #
    #    added-then-imported.txt,v:
    #       Added with 'cvs add' to create 1.1, then imported with
    #       completely different contents to create 1.1.1.1, therefore
    #       never had a default branch.
    #

    conv.logs.check(2, "Import (vbranchA, vtag-1).", (
        ('/%(branches)s/unlabeled-1.1.1', 'A'),
        ('/%(branches)s/unlabeled-1.1.1/proj', 'A'),
        ('/%(branches)s/unlabeled-1.1.1/proj/d.txt', 'A'),
        ('/%(branches)s/unlabeled-1.1.1/proj/e.txt', 'A'),
        ('/%(branches)s/vbranchA', 'A'),
        ('/%(branches)s/vbranchA/proj', 'A'),
        ('/%(branches)s/vbranchA/proj/a.txt', 'A'),
        ('/%(branches)s/vbranchA/proj/b.txt', 'A'),
        ('/%(branches)s/vbranchA/proj/c.txt', 'A'),
        ('/%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt', 'A'),
    ))

    conv.logs.check(3, "This commit was generated by cvs2svn to compensate for changes in r2,", (
        ('proj', 'A'),
        ('proj/a.txt (from /%(branches)s/vbranchA/proj/a.txt:2)', 'A'),
        ('proj/b.txt (from /%(branches)s/vbranchA/proj/b.txt:2)', 'A'),
        ('proj/c.txt (from /%(branches)s/vbranchA/proj/c.txt:2)', 'A'),
        ('proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:2)', 'A'),
        ('proj/deleted-on-vendor-branch.txt '
         '(from /%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt:2)', 'A'),
        ('proj/e.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/e.txt:2)', 'A'),
    ))

    conv.logs.check(4, sym_log_msg('vtag-1', 1), (
        ('/%(tags)s/vtag-1 (from /%(branches)s/vbranchA:2)', 'A'),
        ('/%(tags)s/vtag-1/proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:2)', 'A'),
    ))

    conv.logs.check(5, "Import (vbranchA, vtag-2).", (
        ('/%(branches)s/unlabeled-1.1.1/proj/d.txt', 'M'),
        ('/%(branches)s/unlabeled-1.1.1/proj/e.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/a.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/b.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/c.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt', 'M'),
    ))

    conv.logs.check(6, "This commit was generated by cvs2svn to compensate for changes in r5,", (
        ('proj/a.txt '
         '(from /%(branches)s/vbranchA/proj/a.txt:5)', 'R'),
        ('proj/b.txt '
         '(from /%(branches)s/vbranchA/proj/b.txt:5)', 'R'),
        ('proj/c.txt '
         '(from /%(branches)s/vbranchA/proj/c.txt:5)', 'R'),
        ('proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:5)', 'R'),
        ('proj/deleted-on-vendor-branch.txt '
         '(from /%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt:5)',
         'R'),
        ('proj/e.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/e.txt:5)', 'R'),
    ))

    conv.logs.check(7, sym_log_msg('vtag-2', 1), (
        ('/%(tags)s/vtag-2 (from /%(branches)s/vbranchA:5)', 'A'),
        ('/%(tags)s/vtag-2/proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:5)', 'A'),
    ))

    conv.logs.check(8, "Import (vbranchA, vtag-3).", (
        ('/%(branches)s/unlabeled-1.1.1/proj/d.txt', 'M'),
        ('/%(branches)s/unlabeled-1.1.1/proj/e.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/a.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/b.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/c.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt', 'D'),
    ))

    conv.logs.check(9, "This commit was generated by cvs2svn to compensate for changes in r8,", (
        ('proj/a.txt '
         '(from /%(branches)s/vbranchA/proj/a.txt:8)', 'R'),
        ('proj/b.txt '
         '(from /%(branches)s/vbranchA/proj/b.txt:8)', 'R'),
        ('proj/c.txt '
         '(from /%(branches)s/vbranchA/proj/c.txt:8)', 'R'),
        ('proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:8)', 'R'),
        ('proj/deleted-on-vendor-branch.txt', 'D'),
        ('proj/e.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/e.txt:8)', 'R'),
    ))

    conv.logs.check(10, sym_log_msg('vtag-3', 1), (
        ('/%(tags)s/vtag-3 (from /%(branches)s/vbranchA:8)', 'A'),
        ('/%(tags)s/vtag-3/proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:8)', 'A'),
        ('/%(tags)s/vtag-3/proj/e.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/e.txt:8)', 'A'),
    ))

    conv.logs.check(11, "First regular commit, to a.txt, on vtag-3.", (
        ('proj/a.txt', 'M'),
    ))

    conv.logs.check(12, "Add a file to the working copy.", (
        ('proj/added-then-imported.txt', 'A'),
    ))

    conv.logs.check(13, sym_log_msg('vbranchA'), (
        ('/%(branches)s/vbranchA/proj/added-then-imported.txt '
         '(from proj/added-then-imported.txt:12)', 'A'),
    ))

    conv.logs.check(14, "Import (vbranchA, vtag-4).", (
        ('/%(branches)s/unlabeled-1.1.1/proj/d.txt', 'M'),
        ('/%(branches)s/unlabeled-1.1.1/proj/e.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/a.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/added-then-imported.txt', 'M'),  # CHECK!!!
        ('/%(branches)s/vbranchA/proj/b.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/c.txt', 'M'),
        ('/%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt', 'A'),
    ))

    conv.logs.check(15, "This commit was generated by cvs2svn to compensate for changes in r14,", (
        ('proj/b.txt '
         '(from /%(branches)s/vbranchA/proj/b.txt:14)', 'R'),
        ('proj/c.txt '
         '(from /%(branches)s/vbranchA/proj/c.txt:14)', 'R'),
        ('proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:14)', 'R'),
        ('proj/deleted-on-vendor-branch.txt '
         '(from /%(branches)s/vbranchA/proj/deleted-on-vendor-branch.txt:14)',
         'A'),
        ('proj/e.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/e.txt:14)', 'R'),
    ))

    conv.logs.check(16, sym_log_msg('vtag-4', 1), (
        ('/%(tags)s/vtag-4 (from /%(branches)s/vbranchA:14)', 'A'),
        ('/%(tags)s/vtag-4/proj/d.txt '
         '(from /%(branches)s/unlabeled-1.1.1/proj/d.txt:14)', 'A'),
    ))


@Cvs2HgTestFunction
def default_branches_trunk_only():
    "handle default branches with --trunk-only"

    conv = ensure_conversion('default-branches', args=['--trunk-only'])

    conv.logs.check(2, "Import (vbranchA, vtag-1).", (
        ('proj', 'A'),
        ('proj/a.txt', 'A'),
        ('proj/b.txt', 'A'),
        ('proj/c.txt', 'A'),
        ('proj/d.txt', 'A'),
        ('proj/e.txt', 'A'),
        ('proj/deleted-on-vendor-branch.txt', 'A'),
    ))

    conv.logs.check(3, "Import (vbranchA, vtag-2).", (
        ('proj/a.txt', 'M'),
        ('proj/b.txt', 'M'),
        ('proj/c.txt', 'M'),
        ('proj/d.txt', 'M'),
        ('proj/e.txt', 'M'),
        ('proj/deleted-on-vendor-branch.txt', 'M'),
    ))

    conv.logs.check(4, "Import (vbranchA, vtag-3).", (
        ('proj/a.txt', 'M'),
        ('proj/b.txt', 'M'),
        ('proj/c.txt', 'M'),
        ('proj/d.txt', 'M'),
        ('proj/e.txt', 'M'),
        ('proj/deleted-on-vendor-branch.txt', 'D'),
    ))

    conv.logs.check(5, "First regular commit, to a.txt, on vtag-3.", (
        ('proj/a.txt', 'M'),
    ))

    conv.logs.check(6, "Add a file to the working copy.", (
        ('proj/added-then-imported.txt', 'A'),
    ))

    conv.logs.check(7, "Import (vbranchA, vtag-4).", (
        ('proj/b.txt', 'M'),
        ('proj/c.txt', 'M'),
        ('proj/d.txt', 'M'),
        ('proj/e.txt', 'M'),
        ('proj/deleted-on-vendor-branch.txt', 'A'),
    ))


@Cvs2HgTestFunction
def default_branch_and_1_2():
    "do not allow 1.2 revision with default branch"

    conv = ensure_conversion(
        'default-branch-and-1-2',
        error_re=(
            r'.*File \'.*\' has default branch=1\.1\.1 but also a revision 1\.2'
        ),
    )
    assert conv


@Cvs2HgTestFunction
def compose_tag_three_sources():
    "compose a tag from three sources"
    conv = ensure_conversion('compose-tag-three-sources')

    conv.logs.check(2, "Add on trunk", (
        ('tagged-on-trunk-1.1', 'A'),
        ('tagged-on-trunk-1.2-a', 'A'),
        ('tagged-on-trunk-1.2-b', 'A'),
        ('tagged-on-b1', 'A'),
        ('tagged-on-b2', 'A'),
    ))
    conv.logs.check_branch(2, 'default')

    conv.logs.check(3, sym_log_msg('b1'), (
        ('/%(branches)s/b1 (from /%(trunk)s:2)', 'A'),
    ), branch='b1')

    conv.logs.check(4, sym_log_msg('b2'), (
        ('/%(branches)s/b2 (from /%(trunk)s:2)', 'A'),
    ), branch='b2')

    conv.logs.check(5, "Commit on branch b1", (
        ('tagged-on-trunk-1.1', 'M'),
        ('tagged-on-trunk-1.2-a', 'M'),
        ('tagged-on-trunk-1.2-b', 'M'),
        ('tagged-on-b1', 'M'),
        ('tagged-on-b2', 'M'),
    ), branch='b1')

    conv.logs.check(6, "Commit on branch b2", (
        ('tagged-on-trunk-1.1', 'M'),
        ('tagged-on-trunk-1.2-a', 'M'),
        ('tagged-on-trunk-1.2-b', 'M'),
        ('tagged-on-b1', 'M'),
        ('tagged-on-b2', 'M'),
    ), branch='b2')

    conv.logs.check(7, "Commit again on trunk", (
        ('tagged-on-trunk-1.2-a', 'M'),
        ('tagged-on-trunk-1.2-b', 'M'),
        ('tagged-on-trunk-1.1', 'M'),
        ('tagged-on-b1', 'M'),
        ('tagged-on-b2', 'M'),
    ), branch='default')

    conv.logs.check(8, sym_log_msg('T', 1), (
        ('/%(tags)s/T (from /%(trunk)s:7)', 'A'),
        ('/%(tags)s/T/tagged-on-trunk-1.1 '
         '(from tagged-on-trunk-1.1:2)', 'R'),
        ('/%(tags)s/T/tagged-on-b1 (from /%(branches)s/b1/tagged-on-b1:5)', 'R'),
        ('/%(tags)s/T/tagged-on-b2 (from /%(branches)s/b2/tagged-on-b2:6)', 'R'),
    ))


@Cvs2HgTestFunction
def pass5_when_to_fill():
    "reserve a svn revnum for a fill only when required"
    # The conversion will fail if the bug is present, and
    # ensure_conversion would raise Failure.
    conv = ensure_conversion('pass5-when-to-fill')
    assert conv


class EmptyTrunk(Cvs2HgTestCase):
    "don't break when the trunk is empty"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'empty-trunk', **kw)

    def run(self, sbox):
        # The conversion will fail if the bug is present, and
        # ensure_conversion would raise Failure.
        conv = self.ensure_conversion()
        assert conv


@Cvs2HgTestFunction
def no_spurious_svn_commits():
    "ensure that we don't create any spurious commits"
    conv = ensure_conversion('phoenix')

    # Check spurious commit that could be created in
    # SVNCommitCreator._pre_commit()
    #
    #   (When you add a file on a branch, CVS creates a trunk revision
    #   in state 'dead'.  If the log message of that commit is equal to
    #   the one that CVS generates, we do not ever create a 'fill'
    #   SVNCommit for it.)
    #
    # and spurious commit that could be created in
    # SVNCommitCreator._commit()
    #
    #   (When you add a file on a branch, CVS creates a trunk revision
    #   in state 'dead'.  If the log message of that commit is equal to
    #   the one that CVS generates, we do not create a primary SVNCommit
    #   for it.)
    conv.logs.check(17, 'File added on branch xiphophorus', (
        ('/%(branches)s/xiphophorus/added-on-branch.txt', 'A'),
    ))

    # Check to make sure that a commit *is* generated:
    #   (When you add a file on a branch, CVS creates a trunk revision
    #   in state 'dead'.  If the log message of that commit is NOT equal
    #   to the one that CVS generates, we create a primary SVNCommit to
    #   serve as a home for the log message in question.
    conv.logs.check(18, 'file added-on-branch2.txt was initially added on '
                    + 'branch xiphophorus,\nand this log message was tweaked', ())

    # Check spurious commit that could be created in
    # SVNCommitCreator._commit_symbols().
    conv.logs.check(19, 'This file was also added on branch xiphophorus,', (
        ('/%(branches)s/xiphophorus/added-on-branch2.txt', 'A'),
    ))


class PeerPathPruning(Cvs2HgTestCase):
    "make sure that filling prunes paths correctly"

    def __init__(self, **kw):
        Cvs2HgTestCase.__init__(self, 'peer-path-pruning', **kw)

    def run(self, sbox):
        conv = self.ensure_conversion()
        conv.logs.check(6, sym_log_msg('BRANCH'), (
            ('/%(branches)s/BRANCH (from /%(trunk)s:4)', 'A'),
            ('/%(branches)s/BRANCH/bar', 'D'),
            ('/%(branches)s/BRANCH/foo (from foo:5)', 'R'),
        ))


@Cvs2HgTestFunction
def invalid_closings_on_trunk():
    "verify correct revs are copied to default branches"
    # The conversion will fail if the bug is present, and
    # ensure_conversion would raise Failure.
    conv = ensure_conversion('invalid-closings-on-trunk')
    assert conv


@Cvs2HgTestFunction
def individual_passes():
    "run each pass individually"
    conv = ensure_conversion('main')
    conv2 = ensure_conversion('main', passbypass=1)

    if conv.logs != conv2.logs:
        raise Failure()


@Cvs2HgTestFunction
def resync_bug():
    "reveal a big bug in our resync algorithm"
    # This will fail if the bug is present
    conv = ensure_conversion('resync-bug')
    assert conv


@Cvs2HgTestFunction
def branch_from_default_branch():
    "reveal a bug in our default branch detection code"
    conv = ensure_conversion('branch-from-default-branch')

    # This revision will be a default branch synchronization only
    # if cvs2svn is correctly determining default branch revisions.
    #
    # The bug was that cvs2svn was treating revisions on branches off of
    # default branches as default branch revisions, resulting in
    # incorrectly regarding the branch off of the default branch as a
    # non-trunk default branch.  Crystal clear?  I thought so.  See
    # issue #42 for more incoherent blathering.
    conv.logs.check(5, "This commit was generated by cvs2svn", (
        ('proj/file.txt '
         '(from /%(branches)s/upstream/proj/file.txt:4)', 'R'),
    ))


@Cvs2HgTestFunction
def file_in_attic_too():
    "die if a file exists in and out of the attic"
    ensure_conversion(
        'file-in-attic-too',
        error_re=(
            r'.*A CVS repository cannot contain both '
            r'(.*)' + re.escape(os.sep) + r'(.*) '
            + r'and '
            r'\1' + re.escape(os.sep) + r'Attic' + re.escape(os.sep) + r'\2'
        )
    )


@Cvs2HgTestFunction
def retain_file_in_attic_too():
    "test --retain-conflicting-attic-files option"
    conv = ensure_conversion(
        'file-in-attic-too', args=['--retain-conflicting-attic-files'])
    if not conv.path_exists('trunk', 'file.txt'):
        raise Failure()
    if not conv.path_exists('trunk', 'Attic', 'file.txt'):
        raise Failure()


@Cvs2HgTestFunction
def symbolic_name_filling_guide():
    "reveal a big bug in our SymbolFillingGuide"
    # This will fail if the bug is present
    conv = ensure_conversion('symbolic-name-overfill')
    assert conv


# Helpers for tests involving file contents and properties.

class NodeTreeWalkException:
    "Exception class for node tree traversals."
    pass


def node_for_path(node, path):
    "In the tree rooted under SVNTree NODE, return the node at PATH."
    if node.name != '__SVN_ROOT_NODE':
        raise NodeTreeWalkException()
    path = path.strip('/')
    components = path.split('/')
    for component in components:
        node = cvs2hg_test.tree.get_child(node, component)
    return node


# Helper for tests involving properties.
def props_for_path(node, path):
    "In the tree rooted under SVNTree NODE, return the prop dict for PATH."
    return node_for_path(node, path).props


# We do four conversions.  Each time, we pass --mime-types=FILE with
# the same FILE, but vary --default-eol and --eol-from-mime-type.
# Thus there's one conversion with neither flag, one with just the
# former, one with just the latter, and one with both.


@Cvs2HgTestFunction
def ignore():
    "test setting of svn:ignore property"
    conv = ensure_conversion('cvsignore')
    wc_tree = conv.get_wc_tree()
    topdir_props = props_for_path(wc_tree, 'trunk/proj')
    subdir_props = props_for_path(wc_tree, '/trunk/proj/subdir')

    if topdir_props['svn:ignore'] != \
       '*.idx\n*.aux\n*.dvi\n*.log\nfoo\nbar\nbaz\nqux\n':
        raise Failure()

    if subdir_props['svn:ignore'] != \
       '*.idx\n*.aux\n*.dvi\n*.log\nfoo\nbar\nbaz\nqux\n':
        raise Failure()


@Cvs2HgTestFunction
def requires_cvs():
    "test that CVS can still do what RCS can't"
    # See issues 4, 11, 29 for the bugs whose regression we're testing for.
    conv = ensure_conversion('requires-cvs', args=["--use-cvs"])

    atsign_contents = file(conv.get_wc("trunk", "atsign-add")).read()
    cl_contents = file(conv.get_wc("trunk", "client_lock.idl")).read()

    if atsign_contents[-1:] == "@":
        raise Failure()
    if cl_contents.find("gregh\n//\n//Integration for locks") < 0:
        raise Failure()

    if not (conv.logs[21].author == "William Lyon Phelps III" and
            conv.logs[20].author == "j random"):
        raise Failure()


@Cvs2HgTestFunction
def questionable_branch_names():
    "test that we can handle weird branch names"
    conv = ensure_conversion('questionable-symbols')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual branch paths, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def questionable_tag_names():
    "test that we can handle weird tag names"
    conv = ensure_conversion('questionable-symbols')
    conv.logs.find_tag_log('Tag_A').check(sym_log_msg('Tag_A', 1), (
        ('/%(tags)s/Tag_A (from /trunk:8)', 'A'),
    ))
    conv.logs.find_tag_log('TagWith/Backslash_E').check(
        sym_log_msg('TagWith/Backslash_E', 1),
        (
            ('/%(tags)s/TagWith', 'A'),
            ('/%(tags)s/TagWith/Backslash_E (from /trunk:8)', 'A'),
        )
    )
    conv.logs.find_tag_log('TagWith/Slash_Z').check(
        sym_log_msg('TagWith/Slash_Z', 1),
        (
            ('/%(tags)s/TagWith/Slash_Z (from /trunk:8)', 'A'),
        )
    )


@Cvs2HgTestFunction
def revision_reorder_bug():
    "reveal a bug that reorders file revisions"
    conv = ensure_conversion('revision-reorder-bug')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def exclude():
    "test that exclude really excludes everything"
    conv = ensure_conversion('main', args=['--exclude=.*'])
    for log in conv.logs.values():
        for item in log.changed_paths.keys():
            if item.startswith('/branches/') or item.startswith('/tags/'):
                raise Failure()


@Cvs2HgTestFunction
def vendor_branch_delete_add():
    "add trunk file that was deleted on vendor branch"
    # This will error if the bug is present
    conv = ensure_conversion('vendor-branch-delete-add')
    assert conv


@Cvs2HgTestFunction
def resync_pass2_pull_forward():
    "ensure pass2 doesn't pull rev too far forward"
    conv = ensure_conversion('resync-pass2-pull-forward')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


# @Cvs2HgTestFunction
# def native_eol():
#   "only LFs for svn:eol-style=native files"
#   conv = ensure_conversion('native-eol', args=['--default-eol=native'])
#   lines = run_program(cvs2hg_test.main.svnadmin_binary, None, 'dump', '-q',
#                       conv.repos)
#   # Verify that all files in the dump have LF EOLs.  We're actually
#   # testing the whole dump file, but the dump file itself only uses
#   # LF EOLs, so we're safe.
#   for line in lines:
#     if line[-1] != '\n' or line[:-1].find('\r') != -1:
#       raise Failure()


@Cvs2HgTestFunction
def double_fill():
    "reveal a bug that created a branch twice"
    conv = ensure_conversion('double-fill')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def double_fill2():
    "reveal a second bug that created a branch twice"
    conv = ensure_conversion('double-fill2')
    conv.logs.check_msg(6, sym_log_msg('BRANCH1'))
    conv.logs.check_msg(7, sym_log_msg('BRANCH2'))
    try:
        # This check should fail:
        conv.logs.check_msg(8, sym_log_msg('BRANCH2'))
    except Failure:
        pass
    else:
        raise Failure('Symbol filled twice in a row')


@Cvs2HgTestFunction
def resync_pass2_push_backward():
    "ensure pass2 doesn't push rev too far backward"
    conv = ensure_conversion('resync-pass2-push-backward')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def double_add():
    "reveal a bug that added a branch file twice"
    conv = ensure_conversion('double-add')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def bogus_branch_copy():
    "reveal a bug that copies a branch file wrongly"
    conv = ensure_conversion('bogus-branch-copy')
    # If the conversion succeeds, then we're okay.  We could check the
    # actual revisions, too, but the main thing is to know that the
    # conversion doesn't fail.
    assert conv


@Cvs2HgTestFunction
def nested_ttb_directories():
    "require error if ttb directories are not disjoint"
    opts_list = [
        {'trunk': 'a', 'branches': 'a'},
        {'trunk': 'a', 'tags': 'a'},
        {'branches': 'a', 'tags': 'a'},
        # This option conflicts with the default trunk path:
        {'branches': 'trunk'},
        # Try some nested directories:
        {'trunk': 'a', 'branches': 'a/b'},
        {'trunk': 'a/b', 'tags': 'a/b/c/d'},
        {'branches': 'a', 'tags': 'a/b'},
    ]

    for opts in opts_list:
        ensure_conversion(
            'main', error_re=r'The following paths are not disjoint\:', **opts
        )


@Cvs2HgTestFunction
def ctrl_char_in_filename():
    "do not allow control characters in filenames"

    try:
        srcrepos_path = os.path.join(test_data_dir, 'main-cvsrepos')
        dstrepos_path = os.path.join(test_data_dir, 'ctrl-char-filename-cvsrepos')
        if os.path.exists(dstrepos_path):
            safe_rmtree(dstrepos_path)

        # create repos from existing main repos
        shutil.copytree(srcrepos_path, dstrepos_path)
        base_path = os.path.join(dstrepos_path, 'single-files')
        try:
            shutil.copyfile(os.path.join(base_path, 'twoquick,v'),
                            os.path.join(base_path, 'two\rquick,v'))
        except:
            # Operating systems that don't allow control characters in
            # filenames will hopefully have thrown an exception; in that
            # case, just skip this test.
            raise cvs2hg_test.Skip()

        conv = ensure_conversion(
            'ctrl-char-filename',
            error_re=(r'.*Character .* in filename .* '
                      r'is not supported by Subversion\.'),
        )
        assert conv
    finally:
        safe_rmtree(dstrepos_path)


@Cvs2HgTestFunction
def commit_dependencies():
    "interleaved and multi-branch commits to same files"
    conv = ensure_conversion("commit-dependencies")
    conv.logs.check(2, 'adding', (
        ('interleaved', 'A'),
        ('interleaved/file1', 'A'),
        ('interleaved/file2', 'A'),
    ))

    conv.logs.check(3, 'big commit', (
        ('interleaved/file1', 'M'),
        ('interleaved/file2', 'M'),
    ))

    conv.logs.check(4, 'dependant small commit', (
        ('interleaved/file1', 'M'),
    ))
    conv.logs.check(5, 'adding', (
        ('multi-branch', 'A'),
        ('multi-branch/file1', 'A'),
        ('multi-branch/file2', 'A'),
    ))
    conv.logs.check(6, sym_log_msg("branch"), (
        ('branch/interleaved', 'D'),
    ), branch='branch')
    conv.logs.check(7, 'multi-branch-commit', (
        ('multi-branch/file1', 'M'),
        ('multi-branch/file2', 'M'),
        ('multi-branch/file1', 'M'),
        ('multi-branch/file2', 'M'),
    ), branch='multi-branch')


@Cvs2HgTestFunction
def double_branch_delete():
    "fill branches before modifying files on them"
    conv = ensure_conversion('double-branch-delete')

    # Test for issue #102.  The file IMarshalledValue.java is branched,
    # deleted, readded on the branch, and then deleted again.  If the
    # fill for the file on the branch is postponed until after the
    # modification, the file will end up live on the branch instead of
    # dead!  Make sure it happens at the right time.

    conv.logs.check(6, 'JBAS-2436 - Adding LGPL Header2', (
        ('/%(branches)s/Branch_4_0/IMarshalledValue.java', 'A'),
    ))

    conv.logs.check(7, 'JBAS-3025 - Removing dependency', (
        ('/%(branches)s/Branch_4_0/IMarshalledValue.java', 'D'),
    ))


@Cvs2HgTestFunction
def symbol_mismatches():
    "error for conflicting tag/branch"

    ensure_conversion(
        'symbol-mess',
        args=['--symbol-default=strict'],
        error_re=r'.*Problems determining how symbols should be converted',
    )


@Cvs2HgTestFunction
def overlook_symbol_mismatches():
    "overlook conflicting tag/branch when --trunk-only"

    # This is a test for issue #85.

    ensure_conversion('symbol-mess', args=['--trunk-only'])


@Cvs2HgTestFunction
def force_symbols():
    "force symbols to be tags/branches"

    conv = ensure_conversion(
        'symbol-mess',
        args=['--force-branch=MOSTLY_BRANCH', '--force-tag=MOSTLY_TAG'])
    if conv.path_exists('tags', 'BRANCH') \
       or not conv.path_exists('branches', 'BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'TAG') \
       or conv.path_exists('branches', 'TAG'):
        raise Failure()
    if conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or not conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY_TAG') \
       or conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def commit_blocks_tags():
    "commit prevents forced tag"

    basic_args = ['--force-branch=MOSTLY_BRANCH', '--force-tag=MOSTLY_TAG']
    ensure_conversion(
        'symbol-mess',
        args=(basic_args + ['--force-tag=BRANCH_WITH_COMMIT']),
        error_re=(
            r'.*The following branches cannot be forced to be tags '
            r'because they have commits'
        )
    )


@Cvs2HgTestFunction
def blocked_excludes():
    "error for blocked excludes"

    basic_args = ['--force-branch=MOSTLY_BRANCH', '--force-tag=MOSTLY_TAG']
    for blocker in ['BRANCH', 'COMMIT', 'UNNAMED']:
        try:
            ensure_conversion(
                'symbol-mess',
                args=(basic_args + ['--exclude=BLOCKED_BY_%s' % blocker]))
            raise MissingErrorException()
        except Failure:
            pass


@Cvs2HgTestFunction
def unblock_blocked_excludes():
    "excluding blocker removes blockage"

    basic_args = ['--force-branch=MOSTLY_BRANCH', '--force-tag=MOSTLY_TAG']
    for blocker in ['BRANCH', 'COMMIT']:
        ensure_conversion(
            'symbol-mess',
            args=(basic_args + ['--exclude=BLOCKED_BY_%s' % blocker,
                                '--exclude=BLOCKING_%s' % blocker]))


@Cvs2HgTestFunction
def regexp_force_symbols():
    "force symbols via regular expressions"

    conv = ensure_conversion(
        'symbol-mess',
        args=['--force-branch=MOST.*_BRANCH', '--force-tag=MOST.*_TAG'])
    if conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or not conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY_TAG') \
       or conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def heuristic_symbol_default():
    "test 'heuristic' symbol default"

    conv = ensure_conversion(
        'symbol-mess', args=['--symbol-default=heuristic'])
    if conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or not conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY_TAG') \
       or conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def branch_symbol_default():
    "test 'branch' symbol default"

    conv = ensure_conversion(
        'symbol-mess', args=['--symbol-default=branch'])
    if conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or not conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if conv.path_exists('tags', 'MOSTLY_TAG') \
       or not conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def tag_symbol_default():
    "test 'tag' symbol default"

    conv = ensure_conversion(
        'symbol-mess', args=['--symbol-default=tag'])
    if not conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY_TAG') \
       or conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def symbol_transform():
    "test --symbol-transform"

    conv = ensure_conversion(
        'symbol-mess',
        args=[
            '--symbol-default=heuristic',
            '--symbol-transform=BRANCH:branch',
            '--symbol-transform=TAG:tag',
            '--symbol-transform=MOSTLY_(BRANCH|TAG):MOSTLY.\\1',
        ])
    if not conv.path_exists('branches', 'branch'):
        raise Failure()
    if not conv.path_exists('tags', 'tag'):
        raise Failure()
    if not conv.path_exists('branches', 'MOSTLY.BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY.TAG'):
        raise Failure()


@Cvs2HgTestFunction
def write_symbol_info():
    "test --write-symbol-info"

    expected_lines = [
        ['0', '.trunk.',
         'trunk', 'trunk',
         '.'],
        ['0', 'BLOCKED_BY_UNNAMED',
         'branch', 'branches/BLOCKED_BY_UNNAMED',
         '.trunk.'],
        ['0', 'BLOCKING_COMMIT',
         'branch', 'branches/BLOCKING_COMMIT',
         'BLOCKED_BY_COMMIT'],
        ['0', 'BLOCKED_BY_COMMIT',
         'branch', 'branches/BLOCKED_BY_COMMIT',
         '.trunk.'],
        ['0', 'BLOCKING_BRANCH',
         'branch', 'branches/BLOCKING_BRANCH',
         'BLOCKED_BY_BRANCH'],
        ['0', 'BLOCKED_BY_BRANCH',
         'branch', 'branches/BLOCKED_BY_BRANCH',
         '.trunk.'],
        ['0', 'MOSTLY_BRANCH',
         '.',
         '.',
         '.'],
        ['0', 'MOSTLY_TAG',
         '.',
         '.',
         '.'],
        ['0', 'BRANCH_WITH_COMMIT',
         'branch', 'branches/BRANCH_WITH_COMMIT',
         '.trunk.'],
        ['0', 'BRANCH',
         'branch', 'branches/BRANCH',
         '.trunk.'],
        ['0', 'TAG',
         'tag',
         'tags/TAG',
         '.trunk.'],
        ['0', 'unlabeled-1.1.12.1.2',
         'branch', 'branches/unlabeled-1.1.12.1.2', 'BLOCKED_BY_UNNAMED'],
    ]
    expected_lines.sort()

    symbol_info_file = os.path.join(tmp_dir, 'symbol-mess-symbol-info.txt')
    try:
        ensure_conversion(
            'symbol-mess',
            args=[
                '--symbol-default=strict',
                '--write-symbol-info=%s' % (symbol_info_file,),
                '--passes=:CollateSymbolsPass',
            ],
        )
        raise MissingErrorException()
    except Failure:
        pass
    lines = []
    comment_re = re.compile(r'^\s*\#')
    for l in open(symbol_info_file, 'r'):
        if comment_re.match(l):
            continue
        lines.append(l.strip().split())
    lines.sort()
    if lines != expected_lines:
        s = ['Symbol info incorrect\n']
        differ = Differ()
        for diffline in differ.compare(
            [' '.join(line) + '\n' for line in expected_lines],
            [' '.join(line) + '\n' for line in lines],
        ):
            s.append(diffline)
        raise Failure(''.join(s))


@Cvs2HgTestFunction
def symbol_hints():
    "test --symbol-hints for setting branch/tag"

    conv = ensure_conversion(
        'symbol-mess', symbol_hints_file='symbol-mess-symbol-hints.txt',
    )
    if not conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if not conv.path_exists('tags', 'MOSTLY_TAG'):
        raise Failure()
    conv.logs.check(3, sym_log_msg('MOSTLY_TAG', 1), (
        ('/tags/MOSTLY_TAG (from /trunk:2)', 'A'),
    ))
    conv.logs.check(9, sym_log_msg('BRANCH_WITH_COMMIT'), (
        ('/branches/BRANCH_WITH_COMMIT (from /trunk:2)', 'A'),
    ))
    conv.logs.check(10, sym_log_msg('MOSTLY_BRANCH'), (
        ('/branches/MOSTLY_BRANCH (from /trunk:2)', 'A'),
    ))


@Cvs2HgTestFunction
def parent_hints():
    "test --symbol-hints for setting parent"

    conv = ensure_conversion(
        'symbol-mess', symbol_hints_file='symbol-mess-parent-hints.txt',
    )
    conv.logs.check(9, sym_log_msg('BRANCH_WITH_COMMIT'), (
        ('/%(branches)s/BRANCH_WITH_COMMIT (from /branches/BRANCH:8)', 'A'),
    ))


@Cvs2HgTestFunction
def parent_hints_invalid():
    "test --symbol-hints with an invalid parent"

    # BRANCH_WITH_COMMIT is usually determined to branch from .trunk.;
    # this symbol hints file sets the preferred parent to BRANCH
    # instead:
    conv = ensure_conversion(
        'symbol-mess', symbol_hints_file='symbol-mess-parent-hints-invalid.txt',
        error_re=(
            r"BLOCKED_BY_BRANCH is not a valid parent for BRANCH_WITH_COMMIT"
        ),
    )
    assert conv


@Cvs2HgTestFunction
def parent_hints_wildcards():
    "test --symbol-hints wildcards"

    # BRANCH_WITH_COMMIT is usually determined to branch from .trunk.;
    # this symbol hints file sets the preferred parent to BRANCH
    # instead:
    conv = ensure_conversion(
        'symbol-mess',
        symbol_hints_file='symbol-mess-parent-hints-wildcards.txt',
    )
    rev = 5  # rev = 9
    conv.logs.check_msg(rev, sym_log_msg('BRANCH_WITH_COMMIT'))
    conv.logs.check_branch(conv.logs.parent_of(rev), 'BRANCH')


@Cvs2HgTestFunction
def path_hints():
    "test --symbol-hints for setting svn paths"

    conv = ensure_conversion(
        'symbol-mess', symbol_hints_file='symbol-mess-path-hints.txt',
    )
    # conv.logs.check(1, 'Standard project directories initialized by cvs2svn.', (
    #  ('/trunk', 'A'),
    #  ('/a', 'A'),
    #  ('/a/strange', 'A'),
    #  ('/a/strange/trunk', 'A'),
    #  ('/a/strange/trunk/path', 'A'),
    #  ('/branches', 'A'),
    #  ('/tags', 'A'),
    #  ))
    conv.logs.check(0, 'Adding files on trunk', (
        ('dir/file3', 'D'),
        ('dir/file2', 'D'),
        ('dir/file1', 'D'),
    ))
    conv.logs.check(3, sym_log_msg('MOSTLY_TAG', 1), (
        ('/special', 'A'),
        ('/special/tag', 'A'),
        ('/special/tag/path (from /a/strange/trunk/path:2)', 'A'),
    ))
    conv.logs.check(9, sym_log_msg('BRANCH_WITH_COMMIT'), (
        ('/special/other', 'A'),
        ('/special/other/branch', 'A'),
        ('/special/other/branch/path (from /a/strange/trunk/path:2)', 'A'),
    ))
    conv.logs.check(10, sym_log_msg('MOSTLY_BRANCH'), (
        ('/special/branch', 'A'),
        ('/special/branch/path (from /a/strange/trunk/path:2)', 'A'),
    ))


@Cvs2HgTestFunction
def issue_99():
    "test problem from issue 99"

    conv = ensure_conversion('issue-99')
    assert conv


@Cvs2HgTestFunction
def issue_100():
    "test problem from issue 100"

    conv = ensure_conversion('issue-100')
    file1 = conv.get_wc('trunk', 'file1.txt')
    if file(file1).read() != 'file1.txt<1.2>\n':
        raise Failure()


@Cvs2HgTestFunction
def issue_106():
    "test problem from issue 106"

    conv = ensure_conversion('issue-106')
    assert conv


@Cvs2HgTestFunction
def options_option():
    "use of the --options option"

    conv = ensure_conversion('main', options_file='cvs2svn.options')
    assert conv


@Cvs2HgTestFunction
def multiproject():
    "multiproject conversion"

    conv = ensure_conversion(
        'main', options_file='cvs2svn-multiproject.options'
    )
    conv.logs.check(1, 'Standard project directories initialized by cvs2svn.', (
        ('/partial-prune', 'A'),
        ('/partial-prune/trunk', 'A'),
        ('/partial-prune/branches', 'A'),
        ('/partial-prune/tags', 'A'),
        ('/partial-prune/releases', 'A'),
    ))


@Cvs2HgTestFunction
def crossproject():
    "multiproject conversion with cross-project commits"

    conv = ensure_conversion(
        'main', options_file='cvs2svn-crossproject.options'
    )
    assert conv


@Cvs2HgTestFunction
def tag_with_no_revision():
    "tag defined but revision is deleted"

    conv = ensure_conversion('tag-with-no-revision')
    assert conv


@Cvs2HgTestFunction
def delete_cvsignore():
    "svn:ignore should vanish when .cvsignore does"

    # This is issue #81.

    conv = ensure_conversion('delete-cvsignore')

    wc_tree = conv.get_wc_tree()
    props = props_for_path(wc_tree, 'trunk/proj')

    if 'svn:ignore' in props:
        raise Failure()


@Cvs2HgTestFunction
def repeated_deltatext():
    "ignore repeated deltatext blocks with warning"

    conv = ensure_conversion('repeated-deltatext')
    warning_re = r'.*Deltatext block for revision 1.1 appeared twice'
    if not conv.output_found(warning_re):
        raise Failure()


@Cvs2HgTestFunction
def nasty_graphs():
    "process some nasty dependency graphs"

    # It's not how well the bear can dance, but that the bear can dance
    # at all:
    conv = ensure_conversion('nasty-graphs')
    assert conv


@Cvs2HgTestFunction
def tagging_after_delete():
    "optimal tag after deleting files"

    conv = ensure_conversion('tagging-after-delete')

    # tag should be 'clean', no deletes
    log = conv.logs.find_tag_log('tag1')
    expected = (
        ('/%(tags)s/tag1 (from /%(trunk)s:3)', 'A'),
    )
    log.check_changes(expected)


@Cvs2HgTestFunction
def crossed_branches():
    "branches created in inconsistent orders"

    conv = ensure_conversion('crossed-branches')
    assert conv


@Cvs2HgTestFunction
def file_directory_conflict():
    "error when filename conflicts with directory name"

    conv = ensure_conversion(
        'file-directory-conflict',
        error_re=r'.*Directory name conflicts with filename',
    )
    assert conv


@Cvs2HgTestFunction
def attic_directory_conflict():
    "error when attic filename conflicts with dirname"

    # This tests the problem reported in issue #105.

    conv = ensure_conversion(
        'attic-directory-conflict',
        error_re=r'.*Directory name conflicts with filename',
    )
    assert conv


@Cvs2HgTestFunction
def internal_co():
    "verify that --use-internal-co works"

    rcs_conv = ensure_conversion(
        'main', args=[
            '--use-rcs',
            # '--default-eol=native',
        ])
    conv = ensure_conversion(
        'main', args=[
            # '--default-eol=native',
        ])
    if conv.output_found(r'WARNING\: internal problem\: leftover revisions'):
        raise Failure()
    rcs_lines = run_program(
        cvs2hg_test.main.svnadmin_binary, None, 'dump', '-q', '-r', '1:HEAD',
        rcs_conv.repos)
    lines = run_program(
        cvs2hg_test.main.svnadmin_binary, None, 'dump', '-q', '-r', '1:HEAD',
        conv.repos)
    # Compare all lines following the repository UUID:
    if lines[3:] != rcs_lines[3:]:
        raise Failure()


@Cvs2HgTestFunction
def internal_co_exclude():
    "verify that --use-internal-co --exclude=... works"

    rcs_conv = ensure_conversion(
        'internal-co',
        args=[
            '--use-rcs',
            '--exclude=BRANCH',
            # '--default-eol=native',
        ])
    conv = ensure_conversion(
        'internal-co',
        args=['--exclude=BRANCH'],
    )
    if conv.output_found(r'WARNING\: internal problem\: leftover revisions'):
        raise Failure()
    rcs_lines = run_program(
        cvs2hg_test.main.svnadmin_binary, None, 'dump', '-q', '-r', '1:HEAD',
        rcs_conv.repos)
    lines = run_program(
        cvs2hg_test.main.svnadmin_binary, None, 'dump', '-q', '-r', '1:HEAD',
        conv.repos)
    # Compare all lines following the repository UUID:
    if lines[3:] != rcs_lines[3:]:
        raise Failure()


@Cvs2HgTestFunction
def internal_co_trunk_only():
    "verify that --use-internal-co --trunk-only works"

    conv = ensure_conversion(
        'internal-co',
        args=['--trunk-only'],
    )
    if conv.output_found(r'WARNING\: internal problem\: leftover revisions'):
        raise Failure()


@Cvs2HgTestFunction
def leftover_revs():
    "check for leftover checked-out revisions"

    conv = ensure_conversion(
        'leftover-revs',
        args=['--exclude=BRANCH'],
    )
    if conv.output_found(r'WARNING\: internal problem\: leftover revisions'):
        raise Failure()


@Cvs2HgTestFunction
def requires_internal_co():
    "test that internal co can do more than RCS"
    # See issues 4, 11 for the bugs whose regression we're testing for.
    # Unlike in requires_cvs above, issue 29 is not covered.
    conv = ensure_conversion('requires-cvs')

    atsign_contents = file(conv.get_wc("trunk", "atsign-add")).read()

    if atsign_contents[-1:] == "@":
        raise Failure()

    if not (conv.logs[21].author == "William Lyon Phelps III" and
            conv.logs[20].author == "j random"):
        raise Failure()


@Cvs2HgTestFunction
def internal_co_keywords():
    "test that internal co handles keywords correctly"
    conv_ic = ensure_conversion('internal-co-keywords',
                                args=[
                                    # "--keywords-off",
                                ])
    conv_cvs = ensure_conversion('internal-co-keywords',
                                 args=[
                                     "--use-cvs",
                                     # "--keywords-off",
                                 ])

    ko_ic = file(conv_ic.get_wc('dir', 'ko.txt')).read()
    ko_cvs = file(conv_cvs.get_wc('dir', 'ko.txt')).read()
    kk_ic = file(conv_ic.get_wc('dir', 'kk.txt')).read()
    kk_cvs = file(conv_cvs.get_wc('dir', 'kk.txt')).read()
    kv_ic = file(conv_ic.get_wc('dir', 'kv.txt')).read()
    kv_cvs = file(conv_cvs.get_wc('dir', 'kv.txt')).read()

    if ko_ic != ko_cvs:
        raise Failure()
    if kk_ic != kk_cvs:
        raise Failure()

    # The date format changed between cvs and co ('/' instead of '-').
    # Accept either one:
    date_substitution_re = re.compile(r' ([0-9]*)-([0-9]*)-([0-9]*) ')
    if (kv_ic != kv_cvs 
       and date_substitution_re.sub(r' \1/\2/\3 ', kv_ic) != kv_cvs):
        raise Failure()


@Cvs2HgTestFunction
def timestamp_chaos():
    """test timestamp adjustments"""

    conv = ensure_conversion('timestamp-chaos', args=["-v"])

    # The times are expressed here in UTC:
    times = [
        '2007-01-01 21:00:00',  # Initial commit
        '2007-01-01 21:00:00',  # revision 1.1 of both files
        '2007-01-01 21:00:01',  # revision 1.2 of file1.txt, adjusted forwards
        '2007-01-01 21:00:02',  # revision 1.2 of file2.txt, adjusted backwards
        '2007-01-01 22:00:00',  # revision 1.3 of both files
    ]

    # Convert the times to seconds since the epoch, in UTC:
    times = [calendar.timegm(svn_strptime(t)) for t in times]

    for i in range(len(times)):
        if abs(conv.logs[i + 1].date - times[i]) > 0.1:
            raise Failure()


@Cvs2HgTestFunction
def symlinks():
    "convert a repository that contains symlinks"

    # This is a test for issue #97.

    proj = os.path.join(test_data_dir, 'symlinks-cvsrepos', 'proj')
    links = [
        (
            os.path.join('..', 'file.txt,v'),
            os.path.join(proj, 'dir1', 'file.txt,v'),
        ),
        (
            'dir1',
            os.path.join(proj, 'dir2'),
        ),
    ]

    try:
        os.symlink
    except AttributeError:
        # Apparently this OS doesn't support symlinks, so skip test.
        raise cvs2hg_test.Skip()

    try:
        for (src, dst) in links:
            os.symlink(src, dst)

        conv = ensure_conversion('symlinks')
        conv.logs.check(2, '', (
            ('proj', 'A'),
            ('proj/file.txt', 'A'),
            ('proj/dir1', 'A'),
            ('proj/dir1/file.txt', 'A'),
            ('proj/dir2', 'A'),
            ('proj/dir2/file.txt', 'A'),
        ))
    finally:
        for (src, dst) in links:
            os.remove(dst)


@Cvs2HgTestFunction
def preferred_parent_cycle():
    "handle a cycle in branch parent preferences"

    conv = ensure_conversion('preferred-parent-cycle')
    assert conv


@Cvs2HgTestFunction
def branch_from_empty_dir():
    "branch from an empty directory"

    conv = ensure_conversion('branch-from-empty-dir')
    assert conv


@Cvs2HgTestFunction
def trunk_readd():
    "add a file on a branch then on trunk"

    conv = ensure_conversion('trunk-readd')
    assert conv


@Cvs2HgTestFunction
def branch_from_deleted_1_1():
    "branch from a 1.1 revision that will be deleted"

    conv = ensure_conversion('branch-from-deleted-1-1')
    conv.logs.check(5, 'Adding b.txt:1.1.2.1', (
        ('proj/b.txt', 'A'),
    ))
    conv.logs.check_branch(5, 'BRANCH1')

    conv.logs.check(6, 'Adding b.txt:1.1.4.1', (
        ('/%(branches)s/BRANCH2/proj/b.txt', 'A'),
    ))
    conv.logs.check_branch(6, 'BRANCH2')

    conv.logs.check(7, 'Adding b.txt:1.2', (
        ('proj/b.txt', 'A'),
    ))
    conv.logs.check_branch(7, 'default')

    conv.logs.check(8, 'Adding c.txt:1.1.2.1', (
        ('proj/c.txt', 'A'),
    ))
    conv.logs.check_branch(8, 'BRANCH1')

    conv.logs.check(9, 'Adding c.txt:1.1.4.1', (
        ('proj/c.txt', 'A'),
    ))
    conv.logs.check_branch(9, 'BRANCH1')


@Cvs2HgTestFunction
def add_on_branch():
    "add a file on a branch using newer CVS"

    conv = ensure_conversion('add-on-branch')
    conv.logs.check(4, 'Adding b.txt:1.1', (
        ('proj/b.txt', 'A'),
    ))
    conv.logs.check(5, 'Adding b.txt:1.1.2.2', (
        ('proj/b.txt', 'A'),
    ))
    conv.logs.check_branch(5, 'BRANCH1')
    conv.logs.check(6, 'Adding c.txt:1.1', (
        ('proj/c.txt', 'A'),
    ))
    conv.logs.check(7, 'Removing c.txt:1.2', (
        ('proj/c.txt', 'D'),
    ))
    conv.logs.check(8, 'Adding c.txt:1.2.2.2', (
        ('proj/c.txt', 'A'),
    ))
    conv.logs.check_branch(8, 'BRANCH2')
    conv.logs.check(9, 'Adding d.txt:1.1', (
        ('proj/d.txt', 'A'),
    ))
    conv.logs.check(10, 'Adding d.txt:1.1.2.2', (
        ('proj/d.txt', 'A'),
    ))
    conv.logs.check_branch(10, 'BRANCH3')


# Testing strategy for Mercurial conversion: the gold standard, of
# course, is to compare a CVS working copy with the hg working copy at
# various points in history.  contrib/verify-cvs2hg.py can do this for
# a single repository that has already been converted;
# contrib/verify-all does it for a bunch of repos (by default,
# test-data/*).
#
# It would be pointless (and slow) to repeat what verify-cvs2hg.py does
# here.  So instead, these tests concentrate on fine details that are
# not picked up by verify-cvs2hg (like, does the shape of my graph look
# right?) and on the repositories in test-data that caused more
# problems.
#
# The bulk of effort is expended on exhaustively testing the conversion
# of test-data/main-cvsrepos, because 1) that's where I started and 2)
# it exhibits a number of pathological CVS-isms.  Once the conversion of
# main-cvsrepos worked, the number of test repos that failed
# verification was fairly small -- so that's what the remaining test
# cases work on.

@Cvs2HgTestFunction
def main_hg():
    "output directly to Mercurial"
    repo_dir = "test-temporary-tmp-dir/main.hg"
    username = "cvs2hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [
        '--hgrepos=%s' % repo_dir,
        '--username=%s' % username,
        'test-data/main-cvsrepos',
    ])
    assert conv

    proj_files = [
        "proj/default",
        "proj/sub1/default",
        "proj/sub1/subsubA/default",
        "proj/sub1/subsubB/default",
        "proj/sub2/default",
        "proj/sub2/subsubA/default",
        "proj/sub3/default",
    ]
    number_files = [
        "interleaved/1",
        "interleaved/2",
        "interleaved/3",
        "interleaved/4",
        "interleaved/5",
    ]
    letter_files = [
        "interleaved/a",
        "interleaved/b",
        "interleaved/c",
        "interleaved/d",
        "interleaved/e",
    ]
    single_files = [
        "single-files/attr-exec",
        "single-files/space fname",
        "single-files/twoquick",
    ]
    prune_files = [
        "full-prune-reappear/appears-later",
        "partial-prune/permanent",
    ]

    tester = MercurialTester(repo_dir)

    # Sanity check where various tags and branch heads wind up.  This will
    # give us advance notice that revnum-dependent tests will have to
    # change.

    tester.revnum("after", 8)
    tester.revnum("T_ALL_INITIAL_FILES", 12)
    tester.revnum("T_ALL_INITIAL_FILES_BUT_ONE", 13)
    tester.revnum("B_SPLIT", 29)
    tester.revnum("default", 34)

    # First couple of commits.  N.B. timestamps here are all from "rlog" output,
    # therefore in UTC).
    tester.changeset(0, "jrandom", ("1993/06/18 05:46:08", 0),
                     "Updated CVS",
                     "default")
    tester.changeset(1, "jrandom", ("1994/06/18 05:46:08", 0),
                     "Updated CVS",
                     "default")
    tester.changeset(6, "jrandom", ("2002/09/29 00:00:00", 0),
                     "*** empty log message ***",
                     "default")
    tester.changeset(7, "jrandom", ("2002/09/29 00:00:01", 0),
                     "*** empty log message ***",
                     "default")

    # A tag fixup commit (and the artifical merge that prevents it from
    # being a head).
    tester.changeset(8, "cvs2hg", ("2002/09/29 00:00:02", 0),
                     "fixup commit for tag 'after'",
                     "default")
    tester.changeset(9, "jrandom", ("2002/11/30 19:27:42", 0),
                     "imported",
                     "default",
                     parents=(7, 8))

    # First commit contains just the three files that you get from
    # 'cvs up -D "1993/06/19"'.
    first = ["full-prune-reappear/sub/first",
             "partial-prune/sub/first",
             "full-prune/first"]
    tester.manifest(0, first)
    tester.manifest(1, first + ["partial-prune/permanent"])

    # Tag 'after' only tags one file.
    tester.manifest("after", ["single-files/twoquick"])

    # Changesets right around fixup for 'after' include more.
    tester.manifest(7, ["partial-prune/permanent",
                        "single-files/twoquick"])
    tester.manifest(9, ["partial-prune/permanent",
                        "single-files/twoquick",
                        "single-files/space fname"])

    tester.manifest("T_ALL_INITIAL_FILES", proj_files)
    tester.manifest("T_MIXED", proj_files)
    trimmed = proj_files[:]
    trimmed.remove("proj/sub1/subsubB/default")
    tester.manifest("T_ALL_INITIAL_FILES_BUT_ONE", trimmed)

    # Tip of trunk contains everything (plus .hgtags).
    all_files = (proj_files + number_files + letter_files +
                 single_files + prune_files)
    tester.manifest("default", all_files + [".hgtags"],
                    flags={'single-files/attr-exec': 'x'})

    trimmed = all_files[:]
    trimmed.remove("single-files/twoquick")
    tester.manifest("vendortag", trimmed)

    # Test file contents at various points.
    permanent = """\
This file was added in between the addition of sub/first and
sub/second, to demonstrate that when those two are both removed, the
pruning stops with sub/.
"""
    tester.contents(0, "full-prune/first", "")
    tester.contents(1, "full-prune/first", "")
    tester.contents(1, "partial-prune/permanent", permanent)

    tester.contents(6, "partial-prune/permanent", permanent)
    tester.contents(6, "single-files/twoquick",
                    "hello\n\n")
    tester.contents(7, "partial-prune/permanent", permanent)
    tester.contents(7, "single-files/twoquick",
                    "hello\nmodified after checked in\n\n\n")
    tester.contents("after", "single-files/twoquick",
                    "hello\nmodified after checked in\n\n\n")
    tester.contents(9, "single-files/space fname",
                    "Just a test for spaces in the file name.\n")

    default = """\
This is the file `default' in the top level of the project.

Every directory in the `proj' project has a file named `default'.
"""
    tester.contents(12, "proj/default", default)
    tester.contents("T_ALL_INITIAL_FILES", "proj/default", default)
    tester.contents("T_ALL_INITIAL_FILES_BUT_ONE", "proj/default", default)
    tester.contents("B_FROM_INITIALS", "proj/default", default)
    tester.contents("B_FROM_INITIALS_BUT_ONE", "proj/default", default)

    # B_SPLIT is a very odd beast (branch created twice in CVS): test the
    # living daylights out of it.
    fixup_rev = 21
    fixup_desc = "fixup commit for branch 'B_SPLIT'"
    tester.changeset(fixup_rev,
                     username,
                     ("2003/05/23 00:48:52", 0),
                     fixup_desc,
                     "B_SPLIT",
                     parents=(20,))
    # contents of B_SPLIT when it is first created
    initial_files = [
        "proj/default",
        "proj/sub1/default",
        "proj/sub1/subsubA/default",
        "proj/sub2/default",
        "proj/sub2/subsubA/default",
        "proj/sub3/default",
    ]
    tester.manifest(fixup_rev, initial_files)
    default = """\
This is the file `default' in the top level of the project.

Every directory in the `proj' project has a file named `default'.

This line was added in the second commit (affecting all 7 files).
"""
    tester.contents(fixup_rev, "proj/default", default)
    sub3_contents = """\
This is sub3/default.

Every directory in the `proj' project has a file named `default'.

This line was added by the first commit (affecting two files).

This line was added in the second commit (affecting all 7 files).
"""
    tester.contents(fixup_rev, "proj/sub3/default", sub3_contents)

    # First real commit on B_SPLIT.
    first_commit = 26
    description = """\
First change on branch B_SPLIT.

This change excludes sub3/default, because it was not part of this
commit, and sub1/subsubB/default, which is not even on the branch yet."""
    tester.changeset(first_commit,
                     "jrandom",
                     ("2003/06/03 03:20:31", 0),
                     description,
                     "B_SPLIT",
                     parents=(fixup_rev,))
    tester.manifest(first_commit, initial_files)
    tester.contents(first_commit, "proj/default",
                    default + "\nFirst change on branch B_SPLIT.\n")

    # The second coming of B_SPLIT.
    fixup2_rev = 28
    tester.changeset(fixup2_rev,
                     username,
                     ("2003/06/03 04:29:15", 0),
                     fixup_desc,
                     "B_SPLIT",
                     parents=(first_commit,))
    tester.manifest(fixup2_rev, initial_files + ["proj/sub1/subsubB/default"])
    tester.contents(fixup2_rev, "proj/sub1/subsubB/default",
                    """\
This is sub1/subsubB/default.

Every directory in the `proj' project has a file named `default'.

This line was added in the second commit (affecting all 7 files).

This bit was committed on trunk about an hour after an earlier change
to everyone else on branch B_SPLIT.  Afterwards, we'll finally branch
this file to B_SPLIT, but rooted in a revision that didn't exist at
the time the rest of B_SPLIT was created.
""")

    # Check that branch heads == heads: i.e. no stray heads left by
    # conversion; each CVS branch corresponds to exactly one Mercurial
    # head.
    repo = tester.repo
    bm = repo.branchmap()
    for branch in bm.keys():
        bheads = bm[branch]
        if len(bheads) != 1:
            raise Failure("expected 1 head for branch %r, but got %d heads"
                          % (branch, len(bheads)))
    if set(sum(bm.values(), [])) != set(repo.heads()):
        raise Failure("expected 1-to-1 correspondence between "
                      "heads and branch heads")


@Cvs2HgTestFunction
def hg_tag_fixup_always():
    "hg: force fixup changeset for every tag"
    repo_dir = "test-temporary-tmp-dir/main-tag-fixup-always.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [],
                          options_file='cvs2hg-tag-fixup-always.options')
    assert conv

    tester = MercurialTester(repo_dir)
    tester.revnum('after', 8)
    tester.revnum('T_ALL_INITIAL_FILES', 13)
    tester.revnum('T_MIXED', 19)

    tester.changeset(8,
                     'cvs2hg',
                     ('2002/09/29 00:00:02', 0),
                     "fixup commit for tag 'after'",
                     'default')

    # These two tags do not require a fixup: test that they get one
    # anyways with tag_fixup_mode='always'.
    tester.changeset(13,
                     'cvs2hg',
                     ('2003/05/22 23:20:21', 0),
                     "fixup commit for tag 'T_ALL_INITIAL_FILES'",
                     'B_FROM_INITIALS')   # XXX why not vendorbranch?!
    tester.changeset(19,
                     'cvs2hg',
                     ('2003/05/23 00:17:55', 0),
                     "fixup commit for tag 'T_MIXED'",
                     'B_MIXED')


@Cvs2HgTestFunction
def hg_tag_fixup_sloppy():
    "hg: sloppy tag fixups"
    repo_dir = "test-temporary-tmp-dir/main-tag-fixup-sloppy.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [],
                          options_file='cvs2hg-tag-fixup-sloppy.options')
    assert conv

    tester = MercurialTester(repo_dir)
    # no fixup for 'after' (would only delete files)
    tester.revnum('after', 7)
    # no fixup for T_ALL_INITIAL_FILES (simple copy)
    tester.revnum('T_ALL_INITIAL_FILES', 11)
    # no fixup for T_ALL_INITIAL_FILES_BUT_ONE (delete only)
    tester.revnum('T_ALL_INITIAL_FILES_BUT_ONE', 11)
    # no fixup for T_MIXED (simple copy)
    tester.revnum('T_MIXED', 15)
    # fixup for 'vendortag'
    tester.revnum('vendortag', 29)

    tester.changeset(7,
                     'jrandom',
                     ('2002/09/29 00:00:01', 0),
                     "*** empty log message ***",
                     'default')
    tester.changeset(11,
                     'cvs2hg',
                     ('2003/05/22 23:20:20', 0),
                     "fixup commit for branch 'B_FROM_INITIALS'",
                     'B_FROM_INITIALS')
    tester.changeset(15,
                     'cvs2hg',
                     ('2003/05/23 00:17:54', 0),
                     "fixup commit for branch 'B_MIXED'",
                     'B_MIXED')
    tester.changeset(29,
                     'cvs2hg',
                     ('2003/06/10 20:19:49', 0),
                     "fixup commit for tag 'vendortag'",
                     'default',
                     parents=(21,))

    # In sloppy fixup mode, the tag fixup does not remove any files
    # relative to its parent.  (This tag happens to add one, because
    # that's just the way the CVS repo is.)
    expect_manifest = list(tester.repo[21])
    expect_manifest.append("full-prune-reappear/appears-later")
    tester.manifest(29, expect_manifest)


@Cvs2HgTestFunction
def hg_branch_fixup_optional():
    "hg: optional branch fixups"
    repo_dir = "test-temporary-tmp-dir/branch-fixup-optional.hg"
    erase(repo_dir)
    conv = DVCSConversion('add-cvsignore-to-branch', cvs2hg, None, [],
                          options_file='cvs2hg-branch-fixup-optional.options')
    assert conv

    tester = MercurialTester(repo_dir)

    # With the default fixup mode ('always'), this one would be a fixup...
    # so test that it is not.
    tester.changeset(1,
                     'author1',
                     ('2004/05/03 15:31:02', 0),
                     "",
                     'BRANCH')
    tester.changeset(3,
                     'cvs2hg',
                     ('2004/09/30 09:26:42', 0),
                     "fixup commit for branch 'BRANCH'",
                     'BRANCH')


@Cvs2HgTestFunction
def hg_branch_fixup_sloppy():
    "hg: sloppy branch fixups"
    repo_dir = "test-temporary-tmp-dir/main-branch-fixup-sloppy.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [],
                          options_file='cvs2hg-branch-fixup-sloppy.options')
    assert conv

    tester = MercurialTester(repo_dir)

    # Without sloppy fixups, rev 12 would be a branch fixup: test that it
    # is not.
    tester.changeset(12,
                     'cvs2hg',
                     ('2003/05/22 23:20:22', 0),
                     "fixup commit for tag 'T_ALL_INITIAL_FILES_BUT_ONE'",
                     'B_FROM_INITIALS',
                     parents=(11,))

    # Manifest at head of B_FROM_INITIALS is same as its start point (rev 11).
    expect_manifest = list(tester.repo[11])
    tester.manifest("B_FROM_INITIALS", expect_manifest)

    # Hmmm: branch B_FROM_INITIALS_BUT_ONE won't exist at all.
    try:
        tester.repo.lookup('B_FROM_INITIALS_BUT_ONE')
        raise Failure("expected branch B_FROM_INITIALS_BUT_ONE to not exist")
    except Exception as expected:
        if not str(expected).startswith("unknown revision"):
            raise Failure("expected 'RepoError('unknown revision ...')' but got: %r"
                          % expected)

    # With sloppy fixups, the creation of B_MIXED will not delete any
    # files relative to its parent.
    tester.changeset(15,
                     'cvs2hg',
                     ('2003/05/23 00:17:54', 0),
                     "fixup commit for branch 'B_MIXED'",
                     'B_MIXED',
                     parents=(14,))
    expect_manifest = list(tester.repo[14])
    tester.manifest(15, expect_manifest)


@Cvs2HgTestFunction
def hg_options():
    "test cvs2hg using options file"
    repo_dir = 'test-temporary-tmp-dir/main.hg'      # from the options file
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [],
                          options_file='cvs2hg.options')
    assert conv
    tester = MercurialTester(repo_dir)
    tester.revnum("tip", 34)
    tester.revnum("default", 34)


@Cvs2HgTestFunction
def empty_trunk_hg():
    "hg: convert CVS with empty trunk"
    repo_dir = "test-temporary-tmp-dir/empty-trunk.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [
        '--hgrepos=%s' % repo_dir,
        'test-data/empty-trunk-cvsrepos',
    ])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'max',
                     ('2004/06/05 14:14:45', 0),
                     'Add a_file',
                     'mybranch',
                     parents=(-1,))
    tester.manifest('mytag', ['root/a_file'])
    tester.contents(0, 'root/a_file', '')

    # .hgtags is committed on mybranch, rather than create default
    tester.manifest('tip', ['root/a_file', '.hgtags'])
    repo = tester.repo
    if repo.lookup('tip') != repo.lookup('mybranch'):
        raise Failure("expected tip == mybranch")

    # default does not exist at all
    try:
        repo.lookup('default')
        raise Failure("expected mercurial.repo.RepoError")
    except Exception:  # as expected:
        pass


@Cvs2HgTestFunction
def branch_from_default_branch_hg():
    "hg: non-trunk default branch"

    # hmmm: this test repo is really about a branch off the default
    # branch, but most of my testing effort here is expended on those
    # weird compensation commits that mirror changes on the non-trunk
    # default branch on the trunk

    repo_dir = "test-temporary-tmp-dir/branch-from-default-branch.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [
        '--hgrepos=%s' % repo_dir,
        'test-data/branch-from-default-branch-cvsrepos',
    ])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     "fitz",
                     ("2000/10/20 07:15:19", 0),
                     "Initial Import.",
                     "upstream",
                     parents=(-1,))
    node0 = "7f7dddb6be7d"
    tester.node(0, node0)
    filename = "proj/file.txt"
    content = "This is the initial import of file.txt\n"
    tester.manifest(0, [filename])
    tester.contents(0, filename, content)

    # The choice of parent nodes is a little arbitrary here, and I'm not
    # convinced I've done it right.  So don't worry if you make it better
    # in hg_output_option and this test breaks: just fix the test's
    # expectation!
    message_fmt = ("artificial commit to compensate for changes in "
                   "%s from a CVS\nvendor branch")
    tester.changeset(1,
                     "fitz",
                     ("2000/10/20 07:15:19", 0),
                     message_fmt % node0,
                     "default",
                     parents=(0,))
    tester.manifest(1, [filename])
    tester.contents(1, filename, content)

    tester.changeset(2,
                     "fitz",
                     ("2002/01/10 11:03:58", 0),
                     "This is a log message.",
                     "upstream",
                     parents=(0,))
    node2 = "9e73811e49ae"
    tester.node(2, node2)
    tester.manifest(2, [filename])
    content = "This is the first commit on the default branch.\n"
    tester.contents(2, filename, content)

    tester.changeset(3,
                     "fitz",
                     ("2002/01/10 11:03:58", 0),
                     message_fmt % node2,
                     "default",
                     parents=(1, 2))
    tester.manifest(3, [filename])
    tester.contents(3, filename, content)


@Cvs2HgTestFunction
def vendor_branch_sameness_hg():
    "hg: vendor branch sameness"
    repo_dir = "test-temporary-tmp-dir/vendor-branch-sameness.hg"
    erase(repo_dir)
    conv = DVCSConversion('vendor-branch-sameness',
                          cvs2hg, None,
                          ['--hgrepos=%s' % repo_dir,
                           'test-data/vendor-branch-sameness-cvsrepos'])
    assert conv

    # Test the living daylights out of this conversion, since vendor
    # branches are tricky and weird and I don't really understand them.
    # (The expected output is based on the output of cvs2svn.)

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'kfogel',
                     ('2004/02/12 22:01:44', 0),
                     "Initial revision",
                     'default')
    tester.changeset(1,
                     'kfogel',
                     ('2004/02/12 22:01:45', 0),
                     "First vendor branch revision.",
                     'default')
    tester.revnum('vtag-1', 2)
    tester.changeset(2,
                     'cvs2hg',
                     ('2004/02/12 22:01:46', 0),
                     "fixup commit for tag 'vtag-1'",
                     'default')
    tester.changeset(3,
                     'kfogel',
                     ('2005/02/12 22:01:44', 0),
                     "This log message is not the standard "
                     "'Initial revision\\n' that\n"
                     "indicates an import.",
                     'default')
    tester.changeset(4,
                     'kfogel',
                     ('2005/02/12 22:01:45', 0),
                     "First vendor branch revision.",
                     'default')
    tester.revnum('vtag-2', 5)
    tester.changeset(5,
                     'cvs2hg',
                     ('2005/02/12 22:01:46', 0),
                     "fixup commit for tag 'vtag-2'",
                     'default')

    tester.manifest(0, ['proj/b.txt', 'proj/c.txt', 'proj/d.txt'])
    tester.manifest(1, ['proj/a.txt', 'proj/b.txt', 'proj/d.txt'])
    tester.manifest(2, ['proj/a.txt', 'proj/b.txt'])  # tag fixup: vtag-1
    tester.manifest(3, ['proj/a.txt', 'proj/b.txt', 'proj/d.txt', 'proj/e.txt'])
    tester.manifest(4, ['proj/a.txt', 'proj/b.txt', 'proj/d.txt', 'proj/e.txt'])
    tester.manifest(5, ['proj/e.txt'])    # tag fixup: vtag-2

    import1_text = "Import vtag-1 on vbranchA.\n"
    tester.contents(0, 'proj/b.txt', import1_text)
    tester.contents(0, 'proj/d.txt',
                    "Added d.txt via 'cvs add', but with same "
                    "timestamp as the imports.\n")
    tester.contents(1, 'proj/a.txt', import1_text)
    vbranch_text = "The text on the vendor branch is different.\n"
    tester.contents(1, 'proj/b.txt', import1_text + vbranch_text)
    tester.contents(2, 'proj/a.txt', import1_text)
    tester.contents(2, 'proj/b.txt', import1_text + vbranch_text)
    import2_text = "Import vtag-2 on vbranchB.\n"
    tester.contents(4, 'proj/e.txt', import2_text)
    tester.contents(5, 'proj/e.txt', import2_text)


@Cvs2HgTestFunction
def vendor_branch_delete_add_hg():
    "hg: vendor branch delete-add"
    repo_dir = "test-temporary-tmp-dir/vendor-branch-delete-add.hg"
    erase(repo_dir)
    conv = DVCSConversion('vendor-branch-delete-add',
                          cvs2hg, None,
                          ['--hgrepos=%s' % repo_dir,
                           'test-data/vendor-branch-delete-add-cvsrepos'])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'aa',
                     ('2001/01/01 01:01:01', 0),
                     "1.1.1.1",
                     'vendorbranch')
    tester.node(0, 'a081c2991a08')
    tester.changeset(1,
                     'aa',
                     ('2001/01/01 01:01:01', 0),
                     "artificial commit to compensate for changes in "
                     "a081c2991a08 from a CVS\nvendor branch",
                     'default')
    tester.changeset(2,
                     'bb',
                     ('2002/02/02 02:02:02', 0),
                     "1.1.1.2",
                     'vendorbranch')
    tester.node(2, '0415ca4c53e0')
    tester.changeset(3,
                     'bb',
                     ('2002/02/02 02:02:02', 0),
                     "artificial commit to compensate for changes in "
                     "0415ca4c53e0 from a CVS\nvendor branch",
                     'default')
    tester.changeset(4,
                     'cc',
                     ('2003/03/03 03:03:03', 0),
                     "1.2",
                     'default')

    tester.manifest(0, ['proj/file.txt'])  # on vendorbranch
    tester.manifest(1, ['proj/file.txt'])  # on default (compensation cset)
    tester.manifest(2, [])                 # in svn: "D /branches/vendorbranch"
    tester.manifest(3, [])                 # on default (compensation cset)
    tester.manifest(4, ['proj/file.txt'])


@Cvs2HgTestFunction
def compose_tag_three_sources_hg():
    "hg: compose a tag from three source branches"
    repo_dir = "test-temporary-tmp-dir/compose-tag-three-sources.hg"
    erase(repo_dir)
    conv = DVCSConversion('main', cvs2hg, None, [
        '--hgrepos=%s' % repo_dir,
        'test-data/compose-tag-three-sources-cvsrepos',
    ])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.manifest('T', ['tagged-on-b1',
                          'tagged-on-b2',
                          'tagged-on-trunk-1.1',
                          'tagged-on-trunk-1.2-a',
                          'tagged-on-trunk-1.2-b'])
    tester.contents('T', 'tagged-on-b1', 'b1\n')
    tester.contents('T', 'tagged-on-b2', 'b2\n')
    tester.contents('T', 'tagged-on-trunk-1.1', '')
    tester.contents('T', 'tagged-on-trunk-1.2-a', 'trunk-again\n')
    tester.contents('T', 'tagged-on-trunk-1.2-b', 'trunk-again\n')


@Cvs2HgTestFunction
def author_transform_hg():
    "hg: convert with author_transform"
    repo_dir = 'test-temporary-tmp-dir/unicode-author.hg'
    erase(repo_dir)
    conv = DVCSConversion('unicode-author', cvs2hg, None, [],
                          options_file='cvs2hg-author.options',)
    assert conv

    author1 = u'Branko \u010Cibej <brane@xbc.nu>'.encode('UTF-8')
    author2 = u'Tobias Ringstr\u00F6m <tobias@ringstrom.mine.nu>'.encode('UTF-8')
    author3 = u'h\u00FClsmann'.encode('UTF-8')

    # Monkey-patch Mercurial's default encoding for this test, since we
    # know this conversion generates UTF-8 author names.
    # XXX this is somewhat redundant with similar a monkeypatch in
    # HgOutputOption.setup().
    try:
        from mercurial import util          # Mercurial 1.1, 1.2
        oldencoding = util._encoding

        def setencoding(encoding):
            util._encoding = encoding
    except AttributeError:
        from mercurial import encoding
        oldencoding = encoding.encoding

        def setencoding(enc):
            encoding.encoding = enc

    setencoding('UTF-8')
    try:
        tester = MercurialTester(repo_dir)
        tester.changeset(0,
                         author1,
                         ('2007/02/13 21:13:21', 0),
                         'Revision 1.1',
                         'default')
        tester.changeset(2,
                         author2,
                         ('2008/02/03 22:15:20', 0),
                         'Revision 1.3',
                         'default')
        tester.changeset(4,
                         author3,
                         ('2008/02/03 22:15:22', 0),
                         'Revision 1.5',
                         'default')
    finally:
        setencoding(oldencoding)


@Cvs2HgTestFunction
def timezone_hg():
    "hg: convert with timezone"
    try:
        import pytz
    except ImportError:
        raise cvs2hg_test.Skip()

    # XXX really should use a source repository with times in winter and summer,
    # and should convert with several different timezones
    repo_dir = 'test-temporary-tmp-dir/keywords-timezone.hg'
    erase(repo_dir)
    conv = DVCSConversion('keywords', cvs2hg, None, [],
                          options_file='cvs2hg-timezone.options',)
    assert conv

    # The conversion timezone is Canada/Newfoundland, which is 2.5 hours
    # west of UTC in the summer (and both timestamps in this repository
    # happen to be in the summer).
    expect_tzoffset = int(2.5 * 3600)

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'jrandom',
                     ('2004/07/19 20:57:24', expect_tzoffset),
                     'Add a file.',
                     'default')
    tester.changeset(1,
                     'kfogel',
                     ('2004/07/28 10:42:27', expect_tzoffset),
                     'Commit a second revision, appending text to the first revision.',
                     'default')


@Cvs2HgTestFunction
def existing_hg():
    "hg: add changesets to existing repo"
    repo_dir = 'test-temporary-tmp-dir/symlinks.hg'
    erase(repo_dir)
    _populate_repo(repo_dir)

    conv = DVCSConversion('symlinks', cvs2hg, None,
                          ['--existing-hgrepos', repo_dir,
                           'test-data/symlinks-cvsrepos/proj'])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'test',
                     ('1970/01/01 00:00:00', 0),
                     'init repo',
                     'default',
                     (-1,))

    tester.changeset(1,
                     'mhagger',
                     ('2007/04/08 08:10:10', 0),
                     '',
                     'default',
                     (0,))

    tester.manifest(0, ['README'])
    tester.manifest(1, ['README', 'file.txt'])

    tester.contents(0, 'README', 'hello!\n')
    tester.contents(1, 'README', 'hello!\n')


@Cvs2HgTestFunction
def clobber_hg():
    "hg: clobber existing repo"
    repo_dir = 'test-temporary-tmp-dir/symlinks.hg'
    erase(repo_dir)
    _populate_repo(repo_dir)

    conv = DVCSConversion('symlinks', cvs2hg, None,
                          ['--hgrepos', repo_dir, '--clobber',
                           'test-data/symlinks-cvsrepos/proj'])
    assert conv

    tester = MercurialTester(repo_dir)
    tester.changeset(0,
                     'mhagger',
                     ('2007/04/08 08:10:10', 0),
                     '',
                     'default',
                     (-1,))
    tester.manifest(0, ['file.txt'])


def _populate_repo(repo_dir):
    # Initialize the target repo with one changeset.
    run_program('hg', None, 'init', repo_dir)
    open(os.path.join(repo_dir, 'README'), 'wt').write('hello!\n')
    run_program('hg', None, '-R', repo_dir, 'add')
    run_program('hg', None, '-R', repo_dir,
                'commit', '-m', 'init repo', '-u', 'test', '-d', '0 0')


class MercurialTester(object):
    def __init__(self, repo_dir):
        from mercurial import ui, hg, node
        ui = ui.ui()
        self.repo = hg.repository(ui, repo_dir)
        self.hgnode = node

    def revnum(self, name, expect_revnum):
        # TODO: some smarter api…
        hex = self.repo.lookup(name)  # THrows RepoLookupError on missing
        chg = self.repo[hex]  # → changectx
        actual_revnum = chg.rev()
        if actual_revnum != expect_revnum:
            raise Failure("name %r: expected rev %d, but got %d"
                          % (name, expect_revnum, actual_revnum))

    def node(self, rev, node):
        actual_node = self.hgnode.short(self.repo[rev].node())
        if actual_node != node:
            raise Failure("rev %s: expected node id %s, but got %s"
                          % (rev, node, actual_node))

    def changeset(self, revnum, user, date, description, branch, parents=None):
        cctx = self.repo[revnum]
        if cctx.user() != user:
            raise Failure("rev %d: expected user %r, but got %r"
                          % (revnum, user, cctx.user()))

        if date is not None:
            (timestamp, tzoffset) = date
            fmt = "%Y/%m/%d %H:%M:%S"
            timestamp = datetime.datetime.strptime(timestamp, fmt)

            (actual_timestamp, actual_tzoffset) = cctx.date()
            actual_timestamp = datetime.datetime.utcfromtimestamp(actual_timestamp)

            if (timestamp, tzoffset) != (actual_timestamp, actual_tzoffset):
                raise Failure(
                    "rev %d: expected date %s (tzoffset %d), but got %s (tzoffset %d)"
                    % (revnum, timestamp, tzoffset, actual_timestamp, actual_tzoffset))

        if description != cctx.description():
            raise Failure("rev %d: expected description %r, but got %r"
                          % (revnum, description, cctx.description()))

        if branch != cctx.branch():
            raise Failure("rev %d: expected branch %r, but got %r"
                          % (revnum, branch, cctx.branch()))

        if parents is not None:
            actual_parents = tuple([p.rev() for p in cctx.parents()])
            if parents != actual_parents:
                raise Failure("rev %d: expected parents %r, but got %r"
                              % (revnum, parents, actual_parents))

    def manifest(self, rev, expect_files, flags=None):
        if isinstance(rev, str):  # tag or branch
            rev_id = self.repo.lookup(rev)
        else:
            rev_id = rev
        cctx = self.repo[rev_id]
        expect_files = set(expect_files)
        actual_files = set(cctx.manifest().keys())
        if expect_files != actual_files:
            raise Failure("rev %s: expected manifest:\n  %s\nbut got:\n  %s\n"
                          "missing: %s\n"
                          "extra:   %s"
                          % (rev,
                             "\n  ".join(sorted(expect_files)),
                             "\n  ".join(sorted(actual_files)),
                             ", ".join(sorted(expect_files - actual_files)),
                             ", ".join(sorted(actual_files - expect_files))))

        if flags:
            for filename in cctx:
                expect_flags = flags.get(filename, "")
                actual_flags = cctx.manifest().flags(filename)
                if expect_flags != actual_flags:
                    raise Failure("rev %s, file %s: expected flags %r, but got %r"
                                  % (rev, filename, expect_flags, actual_flags))

    def contents(self, rev, filename, data):
        if isinstance(rev, str):  # tag or branch
            rev_id = self.repo.lookup(rev)
        else:
            rev_id = rev
        fctx = self.repo.filectx(filename, changeid=rev_id)
        if data != fctx.data():
            raise Failure("rev %s, file %s: expected content:\n%r\nbut got:\n%r"
                          % (rev, filename, data, fctx.data()))


@Cvs2HgTestFunction
def invalid_symbol():
    "a symbol with the incorrect format"

    conv = ensure_conversion('invalid-symbol')
    if not conv.output_found(
            r".*branch 'SYMBOL' references invalid revision 1$"
    ):
        raise Failure()


@Cvs2HgTestFunction
def no_revs_file():
    "handle a file with no revisions (issue #80)"

    conv = ensure_conversion('no-revs-file')
    assert conv


@Cvs2HgTestFunction
def mirror_keyerror_test():
    "a case that gave KeyError in SVNRepositoryMirror"

    conv = ensure_conversion('mirror-keyerror')
    assert conv


@Cvs2HgTestFunction
def exclude_ntdb_test():
    "exclude a non-trunk default branch"

    symbol_info_file = os.path.join(tmp_dir, 'exclude-ntdb-symbol-info.txt')
    conv = ensure_conversion(
        'exclude-ntdb',
        args=[
            '--write-symbol-info=%s' % (symbol_info_file,),
            '--exclude=branch3',
            '--exclude=tag3',
            '--exclude=vendortag3',
            '--exclude=vendorbranch',
        ],
    )
    assert conv


@Cvs2HgTestFunction
def mirror_keyerror2_test():
    "a case that gave KeyError in RepositoryMirror"

    conv = ensure_conversion('mirror-keyerror2')
    assert conv


@Cvs2HgTestFunction
def mirror_keyerror3_test():
    "a case that gave KeyError in RepositoryMirror"

    conv = ensure_conversion('mirror-keyerror3')
    assert conv


@Cvs2HgTestFunction
def missing_deltatext():
    "a revision's deltatext is missing"

    # This is a type of RCS file corruption that has been observed.
    conv = ensure_conversion(
        'missing-deltatext',
        error_re=(
            r"ERROR\: .* has no deltatext section for revision 1\.1\.4\.4"
        ),
    )
    assert conv


@Cvs2HgTestFunction
def transform_unlabeled_branch_name():
    "transform name of unlabeled branch"

    conv = ensure_conversion(
        'unlabeled-branch',
        args=[
            '--symbol-transform=unlabeled-1.1.4:BRANCH2',
        ],
    )
    assert conv


@Cvs2HgTestFunction
def unlabeled_branch_name_collision():
    "transform branch to same name as unlabeled branch"

    conv = ensure_conversion(
        'unlabeled-branch',
        args=[
            '--symbol-transform=unlabeled-1.1.4:BRANCH',
        ],
        error_re=(
            r"ERROR\: Symbol name \'BRANCH\' is already used"
        ),
    )
    assert conv


@Cvs2HgTestFunction
def collision_with_unlabeled_branch_name():
    "transform unlabeled branch to same name as branch"

    conv = ensure_conversion(
        'unlabeled-branch',
        args=[
            '--symbol-transform=BRANCH:unlabeled-1.1.4',
        ],
        error_re=(
            r"ERROR\: Symbol name \'unlabeled\-1\.1\.4\' is already used"
        ),
    )
    assert conv


@Cvs2HgTestFunction
def many_deletes():
    "a repo with many removable dead revisions"

    conv = ensure_conversion('many-deletes')
    conv.logs.check(3, 'Add files on BRANCH', (
        ('proj/b.txt', 'A'),
    ), branch='BRANCH')
    conv.logs.check(4, 'Add files on BRANCH2', (
        ('proj/b.txt', 'A'),
        ('proj/c.txt', 'A'),
        ('proj/d.txt', 'A'),
    ), branch='BRANCH2')


@Cvs2HgTestFunction
def branch_heads():
    "record head of each branch"
    import cPickle
    from cvs2hg_lib.symbol import Trunk, Branch

    conv = ensure_conversion('main', args=['--skip-cleanup'])
    assert conv

    file = open('test-temporary-tmp-dir/svn-branch-heads.pck', 'rb')
    branch_heads = cPickle.load(file)
    file.close()

    expect = {
        # these are easy and obvious, since they all have CVS commits
        "Trunk": 34,
        "B_SPLIT": 33,
        "B_MIXED": 26,
    }

    actual = {}
    for ((id, name), revnum) in branch_heads.items():
        actual[name] = revnum

    if expect != actual:
        raise Failure("branch heads: expected:\n%s\nbut got:\n%s"
                      % (expect, actual))


@Cvs2HgTestFunction
def include_empty_directories():
    "test --include-empty-directories option"

    conv = ensure_conversion(
        'empty-directories', args=[
            # '--include-empty-directories',
        ])
    conv.logs.check(1, 'Add b.txt.', (
        ('direct/b.txt', 'A'),
    ))
    conv.logs.check(2, 'Add c.txt.', (
        ('indirect/subdirectory/c.txt', 'A'),
    ))
    conv.logs.check(3, 'Remove b.txt', (
        ('direct/b.txt', 'D'),
    ))
    conv.logs.check(4, 'Remove c.txt', (
        ('indirect/subdirectory/c.txt', 'D'),
    ))
    conv.logs.check(5, 'Re-add b.txt.', (
        ('direct/b.txt', 'A'),
    ))
    conv.logs.check(6, 'Re-add c.txt.', (
        ('indirect/subdirectory/c.txt', 'A'),
    ))
    conv.logs.check(9, 'artificial commit to compensate for changes', (
        ('import/d.txt', 'A'),
    ))
    conv.logs.check(11, 'artificial commit to compensate', (
        ('import/d.txt', 'M'),
    ))
    conv.logs.check(8, 'Import d.txt.', (
        ('import/d.txt', 'A'),
    ), branch='VENDORBRANCH')
    conv.logs.check(7, 'fixup commit for branch \'BRANCH\'', (
    ), branch='BRANCH')


@Cvs2HgTestFunction
def include_empty_directories_no_prune():
    "test --include-empty-directories with --no-prune"

    conv = ensure_conversion(
        'empty-directories', args=[
            # '--include-empty-directories', 
            # '--no-prune',
        ])
    conv.logs.check(1, 'Add b.txt.', (
        ('direct/b.txt', 'A'),
    ))
    conv.logs.check(2, 'Add c.txt.', (
        ('indirect/subdirectory/c.txt', 'A'),
    ))
    conv.logs.check(3, 'Remove b.txt', (
        ('direct/b.txt', 'D'),
    ))
    conv.logs.check(4, 'Remove c.txt', (
        ('indirect/subdirectory/c.txt', 'D'),
    ))
    conv.logs.check(5, 'Re-add b.txt.', (
        ('direct/b.txt', 'A'),
    ))
    conv.logs.check(6, 'Re-add c.txt.', (
        ('indirect/subdirectory/c.txt', 'A'),
    ))
    conv.logs.check(7, 'fixup commit for branch \'BRANCH\'', (
    ))
    conv.logs.check(9, 'artificial commit to compensate for changes', (
        ('import/d.txt', 'A'),
    ))


@Cvs2HgTestFunction
def exclude_symbol_default():
    "test 'exclude' symbol default"

    conv = ensure_conversion(
        'symbol-mess', args=['--symbol-default=exclude'])
    if conv.path_exists('tags', 'MOSTLY_BRANCH') \
       or conv.path_exists('branches', 'MOSTLY_BRANCH'):
        raise Failure()
    if conv.path_exists('tags', 'MOSTLY_TAG') \
       or conv.path_exists('branches', 'MOSTLY_TAG'):
        raise Failure()


@Cvs2HgTestFunction
def add_on_branch2():
    "another add-on-branch test case"

    conv = ensure_conversion('add-on-branch2')
    conv.logs.check_logs_count(1)
    conv.logs.check_branch(0, 'BRANCH')
    conv.logs.check_changes(0, (
        ('file1', 'A'),
    ))


########################################################################
# Run the tests

# Wimp (work in progress) is used to mark tests not ported from svn to Mercurial (but kept
# as they may be ported in the future)
def HgPortToDo(x):
    return Wimp("not yet ported to Hg", x)


# list all tests here, starting with None:
test_list = [
    None,
    show_usage,
    cvs2hg_manpage,
    attr_exec,
    space_fname,
    two_quick,
    HgPortToDo(PruneWithCare()),
    HgPortToDo(interleaved_commits),
    HgPortToDo(simple_commits),
    HgPortToDo(SimpleTags()),
    simple_branch_commits,
    HgPortToDo(mixed_time_tag),
    HgPortToDo(mixed_time_branch_with_added_file),
    HgPortToDo(mixed_commit),
    HgPortToDo(split_time_branch),
    bogus_tag,
    HgPortToDo(overlapping_branch),
    HgPortToDo(PhoenixBranch()),
    HgPortToDo(ctrl_char_in_log),
    overdead,
    HgPortToDo(NoTrunkPrune()),
    HgPortToDo(double_delete),
    split_branch,
    resync_misgroups,
    HgPortToDo(TaggedBranchAndTrunk()),
    HgPortToDo(enroot_race),
    HgPortToDo(enroot_race_obo),
    HgPortToDo(BranchDeleteFirst()),
    nonascii_filenames,
    UnicodeAuthor(
        warning_expected=1),
    UnicodeAuthor(
        warning_expected=0,
        variant='encoding', args=['--encoding=utf_8']),
    UnicodeAuthor(
        warning_expected=0,
        variant='fallback-encoding', args=['--fallback-encoding=utf_8']),
    UnicodeLog(
        warning_expected=1),
    UnicodeLog(
        warning_expected=0,
        variant='encoding', args=['--encoding=utf_8']),
    UnicodeLog(
        warning_expected=0,
        variant='fallback-encoding', args=['--fallback-encoding=utf_8']),
    HgPortToDo(vendor_branch_sameness),
    HgPortToDo(vendor_branch_trunk_only),
    HgPortToDo(default_branches),
    HgPortToDo(default_branches_trunk_only),
    default_branch_and_1_2,
    HgPortToDo(compose_tag_three_sources),
    pass5_when_to_fill,
    HgPortToDo(PeerPathPruning()),
    EmptyTrunk(),
    HgPortToDo(no_spurious_svn_commits),
    invalid_closings_on_trunk,
    HgPortToDo(individual_passes),
    resync_bug,
    HgPortToDo(branch_from_default_branch),
    file_in_attic_too,
    HgPortToDo(retain_file_in_attic_too),
    symbolic_name_filling_guide,
    HgPortToDo(ignore),
    HgPortToDo(requires_cvs),
    questionable_branch_names,
    HgPortToDo(questionable_tag_names),
    revision_reorder_bug,
    HgPortToDo(exclude),
    vendor_branch_delete_add,
    resync_pass2_pull_forward,
    double_fill,
    XFail(double_fill2),
    resync_pass2_push_backward,
    double_add,
    bogus_branch_copy,
    HgPortToDo(nested_ttb_directories),
    ctrl_char_in_filename,
    HgPortToDo(commit_dependencies),
    HgPortToDo(show_help_passes),
    HgPortToDo(multiple_tags),
    multiply_defined_symbols,
    HgPortToDo(multiply_defined_symbols_renamed),
    HgPortToDo(multiply_defined_symbols_ignored),
    repeatedly_defined_symbols,
    HgPortToDo(double_branch_delete),
    symbol_mismatches,
    overlook_symbol_mismatches,
    HgPortToDo(force_symbols),
    commit_blocks_tags,
    blocked_excludes,
    unblock_blocked_excludes,
    HgPortToDo(regexp_force_symbols),
    HgPortToDo(heuristic_symbol_default),
    HgPortToDo(branch_symbol_default),
    HgPortToDo(tag_symbol_default),
    HgPortToDo(symbol_transform),
    HgPortToDo(write_symbol_info),
    HgPortToDo(symbol_hints),
    HgPortToDo(parent_hints),
    parent_hints_invalid,
    parent_hints_wildcards,
    HgPortToDo(path_hints),
    issue_99,
    HgPortToDo(issue_100),
    issue_106,
    HgPortToDo(options_option),
    HgPortToDo(multiproject),
    HgPortToDo(crossproject),
    tag_with_no_revision,
    HgPortToDo(delete_cvsignore),
    repeated_deltatext,
    nasty_graphs,
    XFail(tagging_after_delete),
    crossed_branches,
    file_directory_conflict,
    attic_directory_conflict,
    HgPortToDo(internal_co),
    HgPortToDo(internal_co_exclude),
    internal_co_trunk_only,
    internal_co_keywords,
    leftover_revs,
    HgPortToDo(requires_internal_co),
    HgPortToDo(timestamp_chaos),
    HgPortToDo(symlinks),
    preferred_parent_cycle,
    branch_from_empty_dir,
    trunk_readd,
    HgPortToDo(branch_from_deleted_1_1),
    HgPortToDo(add_on_branch),
    main_hg,
    hg_tag_fixup_always,
    hg_tag_fixup_sloppy,
    hg_branch_fixup_optional,
    hg_branch_fixup_sloppy,
    hg_options,
    empty_trunk_hg,
    branch_from_default_branch_hg,
    vendor_branch_sameness_hg,
    vendor_branch_delete_add_hg,
    compose_tag_three_sources_hg,
    author_transform_hg,
    timezone_hg,
    existing_hg,
    clobber_hg,
    invalid_symbol,
    no_revs_file,
    mirror_keyerror_test,
    exclude_ntdb_test,
    mirror_keyerror2_test,
    mirror_keyerror3_test,
    missing_deltatext,
    transform_unlabeled_branch_name,
    unlabeled_branch_name_collision,
    collision_with_unlabeled_branch_name,
    HgPortToDo(many_deletes),
    branch_heads,
    HgPortToDo(include_empty_directories),
    HgPortToDo(include_empty_directories_no_prune),
    exclude_symbol_default,
    add_on_branch2,
]

if __name__ == '__main__':

    # Configure the environment for reproducible output
    os.environ["LC_ALL"] = "C"

    print(b'Running tests with Mercurial ' + hgversion.version)
    cvs2hg_test.main.run_tests(test_list)

    # NOTREACHED


# End of file.
