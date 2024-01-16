#
# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=protected-access
import pytest

import anyconfig
import anyconfig.ioinfo

import anyconfig_fortios_backend as TT
import anyconfig_fortios_backend.fortios as F

import tests.constants


@pytest.mark.parametrize(
    ("line", "exp"),
    (("", None),
     ('set service "HTTP" "PING" "TRACEROUTE""\n', None),
     ('set foo "bar\n',
      {"type": "set", "name": "foo", "values": ["bar\n"]}),
     ('set foo "bar baz \n',
      {"type": "set", "name": "foo", "values": ["bar baz \n"]}),
     ('   set foo "bar" "baz\n',
      {"type": "set", "name": "foo", "values": ["bar", "baz\n"]}
      ),
     ),
)
def test__process_set_multiline_value_start(line, exp):
    res = F._process_set_with_multiline_value_start(line, container=dict)
    assert res == exp


@pytest.mark.parametrize(
    ("line", "exp"),
    (("", None),
     ('"\n', ''),
     ('foo "\n', 'foo '),
     ),
)
def test__process_set_multiline_value_end(line, exp):
    res = F._process_set_multiline_value_end(line)
    assert res == exp


_CNF_FILES = [str(p) for p in tests.constants.CNF_FILES]
_IPATH_EPATH_PAIRS = [
    (p, p.parent / p.name.replace('.txt', '.json'))
    for p in tests.constants.CNF_FILES
]
assert _IPATH_EPATH_PAIRS


@pytest.mark.parametrize(
    ("ipath", "epath"),
    _IPATH_EPATH_PAIRS,
    ids=[p.name for p, _e in _IPATH_EPATH_PAIRS],
)
def test_load(ipath, epath, tmp_path):
    out_path = tmp_path / 'out.json'

    try:
        cnf = TT.Parser().load(anyconfig.ioinfo.make(ipath), ac_ordered=True)
        assert cnf
        assert isinstance(cnf, F.DEF_DICT)

        anyconfig.dump(cnf, out_path)

        ocnf = anyconfig.load(out_path, ac_ordered=False)
        exp = anyconfig.load(epath, ac_ordered=False)

        assert ocnf == exp, f'{ocnf!r} vs. {exp!r}'

    except AssertionError as exc:
        raise AssertionError(f'file: {ipath}, exc={exc!s}') from exc

# vim:sw=4:ts=4:et:
