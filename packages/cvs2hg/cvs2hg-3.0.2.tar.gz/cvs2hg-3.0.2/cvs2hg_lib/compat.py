# -*- coding: utf-8 -*-

"""
Some compatibility helpers
"""

import sys

if sys.version_info.major < 3:
    import cPickle
    from cStringIO import StringIO
    from ConfigParser import ConfigParser

    perform_execfile = execfile
else:
    from io import StringIO
    import pickle as cPickle
    from configparser import ConfigParser

    def perform_execfile(fname, glb=None, loc=None):
        with open(fname) as fd:
            exec(fd.read(), glb, loc)
