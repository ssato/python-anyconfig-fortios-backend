#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato at redhat.com>
#
"""Constants for test cases.
"""
import pathlib


CURDIR = pathlib.Path(__file__).parent
CNF_FILES = sorted((CURDIR / 'res').glob('*.txt'))
