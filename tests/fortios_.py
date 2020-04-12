#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

import glob
import os.path
import unittest

import anyconfig
import anyconfig.ioinfo
import anyconfig_fortios_backend as TT
import anyconfig_fortios_backend.fortios as F
import tests.common as TBC


_CNF_FILES = sorted(glob.glob(os.path.join(TBC.selfdir(), "res/*.txt")))


class Test_10(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.workdir = TBC.setup_workdir()
        self.psr = TT.Parser()

    def tearDown(self):
        TBC.cleanup_workdir(self.workdir)

    def test_load(self):
        self.assertTrue(_CNF_FILES)

        for in_path in _CNF_FILES:
            exp_path = in_path.replace(".txt", ".json")
            out_path = os.path.join(self.workdir, "out.json")

            if not os.path.exists(exp_path):
                continue  # The reference test data is not ready.

            try:
                cnf = self.psr.load(anyconfig.ioinfo.make(in_path),
                                    ac_ordered=True)
                self.assertTrue(cnf)
                self.assertTrue(isinstance(cnf, F.DEF_DICT))

                anyconfig.dump(cnf, out_path)
                self.assertEqual(anyconfig.load(out_path, ac_ordered=False),
                                 anyconfig.load(exp_path, ac_ordered=False))
            except AssertionError as exc:
                raise AssertionError("file: {}, exc={!s}".format(in_path, exc))

# vim:sw=4:ts=4:et:
