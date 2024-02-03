#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Base class for loader and dumper cclasses for fortios configuration files.

Base class to hold common memmbers.
"""
import anyconfig.models.processor


class Base(anyconfig.models.processor.Processor):
    """
    Base class for loader and dumper classes.
    """

    _cid = "fortios.builtin"
    _type = "fortios"
    _extensions = []
    _ordered = True
