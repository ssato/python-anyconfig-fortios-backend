#
# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=protected-access
import pytest

import anyconfig
import anyconfig.ioinfo

import anyconfig_fortios_backend.fortios.loader as TT
import anyconfig_fortios_backend.fortios.parser as P

import tests.constants


@pytest.mark.parametrize(
    ("ipath", "epath"),
    tests.constants.IPATH_EPATH_PAIRS,
    ids=[p.name for p, _e in tests.constants.IPATH_EPATH_PAIRS],
)
def test_load(ipath, epath, tmp_path):
    out_path = tmp_path / 'out.json'

    try:
        cnf = TT.Loader().load(anyconfig.ioinfo.make(ipath), ac_ordered=True)
        assert cnf
        assert isinstance(cnf, P.DEF_DICT)

        anyconfig.dump(cnf, out_path)

        ocnf = anyconfig.load(out_path, ac_ordered=False)
        exp = anyconfig.load(epath, ac_ordered=False)

        assert ocnf == exp, f'{ocnf!r} vs. {exp!r}'

    except AssertionError as exc:
        raise AssertionError(f'file: {ipath}, exc={exc!s}') from exc
