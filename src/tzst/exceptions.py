"""Exception classes for tzst."""


class TzstError(Exception):
    """Base exception for tzst operations."""

    pass


class TzstCompressionError(TzstError):
    """Exception raised when compression fails."""

    pass


class TzstDecompressionError(TzstError):
    """Exception raised when decompression fails."""

    pass


class TzstArchiveError(TzstError):
    """Exception raised when archive operations fail."""

    pass


class TzstFileNotFoundError(TzstError, FileNotFoundError):
    """Exception raised when a file is not found."""

    pass
