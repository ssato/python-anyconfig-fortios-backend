#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import glob
import os.path
import os
import tempfile


def selfdir():
    """
    >>> os.path.exists(selfdir())
    True
    """
    return os.path.dirname(__file__)


CNF_FILES = sorted(glob.glob(os.path.join(selfdir(), "/res/*.txt")))


def setup_workdir():
    """
    >>> workdir = setup_workdir()
    >>> assert workdir != '.'
    >>> assert workdir != '/'
    >>> os.path.exists(workdir)
    True
    >>> os.rmdir(workdir)
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-anyconfig-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!

    >>> from os import linesep as lsep
    >>> workdir = setup_workdir()
    >>> os.path.exists(workdir)
    True
    >>> open(os.path.join(workdir, "workdir.stamp"), 'w').write("OK!" + lsep)
    >>> cleanup_workdir(workdir)
    >>> os.path.exists(workdir)
    False
    """
    assert workdir != '/'
    assert workdir != '.'

    os.system("rm -rf " + workdir)

# vim:sw=4:ts=4:et:
