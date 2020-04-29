"""anyconfig backend to load and parse fortios' "show *configuration" outputs.
"""
from __future__ import absolute_import
from .fortios import Parser

__version__ = "0.1.6"
__all__ = ["Parser"]
