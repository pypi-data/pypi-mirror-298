#!/usr/bin/env python

from setuptools import setup


def get_version():
    from cvs2hg_lib.version import VERSION
    return VERSION


def get_description():
    with open("README.rst") as readme:
        return readme.read()


setup(
    name="cvs2hg",
    version=get_version(),
    description="cvs2hg repository converter (based on cvs2svn)",
    long_description=get_description(),
    author="The cvs2svn team, Greg Ward, Marcin Kasperski",
    author_email="Marcin.Kasperski@mekk.waw.pl",
    url="https://foss.heptapod.net/mercurial/mercurial-cvs2hg",
    license="Apache-style",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: CVS',
        'Topic :: Utilities',
    ],
    # Data.
    packages=["cvs2hg_lib", "cvs2hg_rcsparse"],
    scripts=["cvs2hg"],
)
