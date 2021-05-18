#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
import pathlib
import tempfile
import unittest

import anyconfig
import anyconfig.ioinfo
import anyconfig_fortios_backend as TT
import anyconfig_fortios_backend.fortios as F


_CNF_FILES = sorted(
    str(p) for p in (pathlib.Path(__file__).parent / 'res').glob('*.txt')
)


class Test_10(unittest.TestCase):

    maxDiff = None

    def test_load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = pathlib.Path(temp_dir)

            self.assertTrue(_CNF_FILES)

            for in_path in _CNF_FILES:
                exp_path = in_path.replace('.txt', '.json')
                out_path = workdir / 'out.json'

                if not out_path.exists():
                    continue  # The reference test data is not ready.

                try:
                    psr = TT.Parser()
                    cnf = psr.load(anyconfig.ioinfo.make(in_path),
                                   ac_ordered=True)
                    self.assertTrue(cnf)
                    self.assertTrue(isinstance(cnf, F.DEF_DICT))

                    anyconfig.dump(cnf, out_path)
                    self.assertEqual(
                        anyconfig.load(out_path, ac_ordered=False),
                        anyconfig.load(exp_path, ac_ordered=False)
                    )
                except AssertionError as exc:
                    raise AssertionError(f'file: {in_path}, exc={exc!s}')

# vim:sw=4:ts=4:et:
