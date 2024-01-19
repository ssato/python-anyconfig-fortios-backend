#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=protected-access
import pytest

import anyconfig_fortios_backend.parser as TT


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
    res = TT._process_set_with_multiline_value_start(line, container=dict)
    assert res == exp


@pytest.mark.parametrize(
    ("line", "exp"),
    (("", None),
     ('"\n', ''),
     ('foo "\n', 'foo '),
     ),
)
def test__process_set_multiline_value_end(line, exp):
    res = TT._process_set_multiline_value_end(line)
    assert res == exp
