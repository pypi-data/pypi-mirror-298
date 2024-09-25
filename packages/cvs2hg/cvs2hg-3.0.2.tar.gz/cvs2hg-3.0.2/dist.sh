#!/bin/sh
set -e

# Build a cvs2hg distribution.

VERSION=`python cvs2hg_lib/version.py`
echo "Building cvs2hg ${VERSION}"
DIST_BASE=cvs2hg-${VERSION}
DIST_FULL=${DIST_BASE}.tar.gz

# Clean up anything that might have been left from a previous run.
rm -rf dist MANIFEST ${DIST_FULL}
make clean

# Build the dist, Python's way.
./setup.py sdist
mv dist/${DIST_FULL} .

# Clean up after this run.
rm -rf dist MANIFEST

# We're outta here.
echo ""
echo "Done:"
echo ""
ls -l ${DIST_FULL}
md5sum ${DIST_FULL}
echo ""
