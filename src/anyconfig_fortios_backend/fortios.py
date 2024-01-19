#
# Copyright (C) 2020 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>.
# SPDX-License-Identifier: MIT
#
r"""Very experimental parser parses fortios configuration.

- Format to support: Fortios' "show *configuration" outputs
- Requirements: None
- Development Status :: 4 - Beta
- Limitations:

  - Load function only and it doesn't support dump function
  - It should have some more I'm not aware of

Chnagelog:

   .. versionchanged:: 0.2.0

       retustured; split loader and dumper.

   .. versionchanged:: 0.1.5

       Support multiple VDoms, workaround for corrupt outputs without correct
       indents and edit section ends without 'next' end marker.

    .. versionadded:: 0.1.0
"""
import anyconfig.backend.base

from . import dumper, loader


class Parser(anyconfig.backend.base.Parser, loader.Loader, dumper.Dumper):
    """
    Parser for fortios (fortigate) "show *configuration" outputs.
    """
    dump_to_stream = dumper.Dumper.dump_to_stream
