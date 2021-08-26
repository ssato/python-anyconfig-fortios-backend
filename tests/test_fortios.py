#
# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
import anyconfig
import anyconfig.ioinfo

import anyconfig_fortios_backend as TT
import anyconfig_fortios_backend.fortios as F

import tests.constants


_CNF_FILES = [str(p) for p in tests.constants.CNF_FILES]


def test_load(tmp_path):
    assert _CNF_FILES

    for in_path in _CNF_FILES:
        exp_path = in_path.replace('.txt', '.json')
        out_path = tmp_path / 'out.json'

        if not out_path.exists():
            continue  # The reference test data is not ready.

        try:
            psr = TT.Parser()
            cnf = psr.load(anyconfig.ioinfo.make(in_path),
                           ac_ordered=True)
            assert cnf
            assert isinstance(cnf, F.DEF_DICT)

            anyconfig.dump(cnf, out_path)
            ocnf = anyconfig.load(out_path, ac_ordered=False)
            exp = anyconfig.load(exp_path, ac_ordered=False)
            assert ocnf == exp, f'{ocnf!r} vs. {exp!r}'

        except AssertionError as exc:
            raise AssertionError(f'file: {in_path}, exc={exc!s}')

# vim:sw=4:ts=4:et:
