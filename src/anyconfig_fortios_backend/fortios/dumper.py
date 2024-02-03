#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Very experimental dumpers for fortios configuration objects.

.. note:: This is NOT implemented yet.
"""
import anyconfig.backend.base

from . import base


class Dumper(base.Base, anyconfig.backend.base.ToStreamDumperMixin):
    """
    Dumper class to dump fortios (fortigate) configuration object which is
    originally load using the loader, anyconfig_fortios_backend.loader.Loader.
    """

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file or file-like object 'stream'.

        :param cnf: Java properties config data to dump
        :param stream: Java properties file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        raise NotImplementedError("Not implemented yet")
