"""Exception classes for tzst."""


class TzstError(Exception):
    """Base exception for all tzst operations.

    This is the parent class for all tzst-specific exceptions.
    Catch this to handle any tzst-related error.
    """

    pass


class TzstCompressionError(TzstError):
    """Exception raised when compression operations fail.

    This can occur when:
    - Invalid compression level is specified
    - Disk space is insufficient during compression
    - Input data cannot be compressed due to corruption
    - Zstandard compression encounters an internal error
    """

    pass


class TzstDecompressionError(TzstError):
    """Exception raised when decompression operations fail.

    This can occur when:
    - Archive file is corrupted or incomplete
    - Archive was not created with zstandard compression
    - Decompression buffer overflows or underflows
    - Archive format is invalid or unsupported
    """

    pass


class TzstArchiveError(TzstError):
    """Exception raised when archive operations fail.

    This can occur when:
    - Archive file cannot be opened or created
    - File permissions prevent archive access
    - Archive structure is malformed
    - Tar operations fail within the archive
    - Atomic file operations fail during creation
    """

    pass


class TzstFileNotFoundError(TzstError, FileNotFoundError):
    """Exception raised when a required file is not found.

    This can occur when:
    - Archive file does not exist for reading operations
    - Input files for archiving do not exist
    - Output directory cannot be created for extraction
    - Temporary files cannot be created during atomic operations

    Inherits from both TzstError and FileNotFoundError for compatibility
    with standard Python exception handling patterns.
    """

    pass
