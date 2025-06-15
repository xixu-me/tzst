"""tzst - The next-generation Python library engineered for modern archive management.

Leveraging cutting-edge Zstandard compression to deliver superior performance,
security, and reliability.
"""

__version__ = "1.2.8"

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
