"""anyconfig backend to load and parse fortios' "show *configuration" outputs.
"""
from .fortios import Parser

__version__ = "0.2.0"
__all__ = ["Parser"]
