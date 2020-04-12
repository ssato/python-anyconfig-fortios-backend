#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import, print_function

import unittest

import anyconfig
import tests.common as TBC


class Test_90(unittest.TestCase):

    def _try_loads(self, files):
        for filepath in files:
            try:
                cnf = anyconfig.load(filepath, ac_parser="fortios")
                self.assertTrue(cnf)

                exp_path = filepath.replace(".txt", ".json")
                ref = anyconfig.load(exp_path, ordered=True)

            except anyconfig.UnknownFileTypeError:
                print("all types=%r" % anyconfig.list_types())
                raise

            self.assertEqual(cnf, ref)

    def test_10_load(self):
        self._try_loads(TBC.CNF_FILES)

# vim:sw=4:ts=4:et:
