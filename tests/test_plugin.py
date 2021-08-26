#
# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Plugin test cases.
"""
import anyconfig

import tests.constants


def _try_loads(files):
    for filepath in files:
        try:
            cnf = anyconfig.load(filepath, ac_parser="fortios")
            assert cnf

            exp_path = str(filepath).replace(".txt", ".json")
            ref = anyconfig.load(exp_path, ordered=True)

        except anyconfig.UnknownFileTypeError:
            print("all types=%r" % anyconfig.list_types())
            raise

        assert cnf == ref


def test_load():
    _try_loads(tests.constants.CNF_FILES)

# vim:sw=4:ts=4:et:
