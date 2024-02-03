"""Loader and dumper backend to load from and dump to fortios' "show
*configuration" outputs.

.. note:: dumper is NOT implemented yet actually.
"""
from .fortios.fortios import Parser
from .fortios.loader import Loader

__version__ = "0.2.0"
__all__ = ["Parser", "Loader"]
