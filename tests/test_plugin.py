#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Plugin test cases.
"""
import anyconfig
import pytest

import tests.constants


def _try_loads(ipath, epath, ac_parser: str = "fortios"):
    try:
        cnf = anyconfig.load(ipath, ac_parser=ac_parser)
        assert cnf

        ref = anyconfig.load(epath, ordered=True)

    except anyconfig.UnknownFileTypeError:
        print(f"all types={anyconfig.list_types()}")
        raise

    assert cnf == ref


@pytest.mark.parametrize(
    ("ipath", "epath"),
    tests.constants.IPATH_EPATH_PAIRS,
    ids=[p.name for p, _e in tests.constants.IPATH_EPATH_PAIRS],
)
def test_load(ipath, epath):
    _try_loads(ipath, epath)
    _try_loads(ipath, epath, ac_parser="fortios.builtin")
