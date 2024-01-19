#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>.
# SPDX-License-Identifier: MIT
#
r"""Loader fortios configuration files.
"""
import anyconfig.backend.base

from . import parser


def load(stream, container=parser.DEF_DICT):
    """
    Load and parse Java properties file given as a fiel or file-like object
    'stream'.

    :param stream:
        A file or file like object of fortigate "show *configuration" outputs
    :param container:
        Factory function to create a dict-like object to store configurations

    :return: A mapping object holding fortios' configurations
    """
    return container(
        configs=list(
            parser.parse_show_config_itr(stream, container=container)
        )
    )


class Loader(anyconfig.backend.base.FromStreamLoaderMixin):
    """
    Loader for fortios (fortigate) "show *configuration" outputs.
    """
    _cid = "fortios.builtin"
    _type = "fortios"
    _extensions = []
    _load_opts = ["full"]
    _ordered = True

    def load_from_stream(self, stream, container, **kwargs):
        """
        Load config from given file or file-like object `stream`.

        :param stream: A file or file like object of Java properties files
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return load(stream, container=container)
