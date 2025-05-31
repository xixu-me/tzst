"""tzst - A Python library for creating and manipulating .tzst/.tar.zst archives."""

import sys

# Compatibility fix for Python 3.14 - ByteString was removed from typing
# This is required for the zstandard library to work with Python 3.14+
if sys.version_info >= (3, 14):
    # ByteString was removed in Python 3.14, provide compatibility for zstandard
    import typing

    try:
        from collections.abc import ByteString

        typing.ByteString = ByteString
    except ImportError:
        pass

__version__ = "0.4.0"

from .core import (
    TzstArchive,
    create_archive,
    extract_archive,
    list_archive,
    test_archive,
)

__all__ = [
    "TzstArchive",
    "create_archive",
    "extract_archive",
    "list_archive",
    "test_archive",
]
