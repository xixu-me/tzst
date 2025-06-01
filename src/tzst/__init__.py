"""tzst - A Python library for creating and manipulating .tzst/.tar.zst archives."""

__version__ = "1.1.0"

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
