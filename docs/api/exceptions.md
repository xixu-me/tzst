# Exceptions API

Custom exception classes used by tzst for comprehensive error handling and debugging.

```{eval-rst}
.. automodule:: tzst.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
```

## Overview

The tzst library provides a comprehensive hierarchy of exceptions to help identify and handle different types of errors that may occur during archive operations. All exceptions inherit from the base `TzstError` class, making it easy to catch all tzst-related errors with a single exception handler.

### Exception Hierarchy

```text
TzstError (base exception)
├── TzstArchiveError (archive operation failures)
├── TzstCompressionError (compression failures)
└── TzstDecompressionError (decompression failures)
```

## Exception Classes

### Base Exception

#### TzstError

```{eval-rst}
.. autoexception:: tzst.exceptions.TzstError
   :members:
   :show-inheritance:
```

The base exception class for all tzst operations. Catch this exception to handle any tzst-related error in your application.

**Usage:**

```python
from tzst import create_archive, TzstError

try:
    create_archive("backup.tzst", ["files/"])
except TzstError as e:
    print(f"tzst operation failed: {e}")
```

### Archive Operation Exceptions

#### TzstArchiveError

```{eval-rst}
.. autoexception:: tzst.exceptions.TzstArchiveError
   :members:
   :show-inheritance:
```

Raised when archive operations fail, such as:

- Archive file cannot be opened or created
- File permissions prevent archive access
- Archive structure is malformed
- Tar operations fail within the archive
- Atomic file operations fail during creation

**Common Scenarios:**

- Invalid archive file path
- Insufficient disk space
- File permission errors
- Corrupt archive structure

### Compression Exceptions

#### TzstCompressionError

```{eval-rst}
.. autoexception:: tzst.exceptions.TzstCompressionError
   :members:
   :show-inheritance:
```

Raised when compression operations fail, including:

- Invalid compression level is specified
- Disk space is insufficient during compression
- Input data cannot be compressed due to corruption
- Zstandard compression encounters an internal error

**Common Scenarios:**

- Compression level out of range (1-22)
- Insufficient disk space during compression
- Source file corruption
- Zstandard library errors

### Decompression Exceptions

#### TzstDecompressionError

```{eval-rst}
.. autoexception:: tzst.exceptions.TzstDecompressionError
   :members:
   :show-inheritance:
```

Raised when decompression operations fail, such as:

- Archive file is corrupted or incomplete
- Archive was not created with zstandard compression
- Decompression buffer overflows or underflows
- Archive format is invalid or unsupported

**Common Scenarios:**

- Corrupted or truncated archive files
- Non-zstandard compressed archives
- Invalid tar structure within archive
- Archive format version mismatches

## Error Handling Best Practices

### Basic Error Handling

```python
from tzst import create_archive, TzstArchiveError, TzstCompressionError

try:
    create_archive("backup.tzst", ["documents/"])
except TzstCompressionError as e:
    print(f"Compression failed: {e}")
except TzstArchiveError as e:
    print(f"Archive operation failed: {e}")
```

### Comprehensive Error Handling

```python
from tzst import extract_archive, TzstError

try:
    extract_archive("backup.tzst", "restore/")
except TzstError as e:
    # Catch any tzst-related error
    print(f"Operation failed: {e}")
    # Perform cleanup or fallback operations
```

### Specific Exception Handling

```python
from tzst import TzstArchive, TzstDecompressionError, TzstArchiveError

def safe_extract(archive_path, output_dir):
    try:
        with TzstArchive(archive_path, "r") as archive:
            # Test integrity first
            if not archive.test():
                print("Archive integrity check failed")
                return False
            
            # Extract files
            archive.extractall(output_dir)
            return True
            
    except TzstDecompressionError as e:
        print(f"Archive is corrupted or invalid: {e}")
        return False
    except TzstArchiveError as e:
        print(f"Archive operation failed: {e}")
        return False
    except FileNotFoundError:        print(f"Archive file not found: {archive_path}")
        return False
    except PermissionError:
        print(f"Permission denied accessing: {archive_path}")
        return False

```

### Logging Integration

```python
import logging
from tzst import test_archive, TzstDecompressionError, TzstError

logger = logging.getLogger(__name__)

def verify_archive(archive_path):
    """Verify archive integrity with comprehensive logging."""
    try:
        if test_archive(archive_path):
            logger.info(f"Archive {archive_path} is valid")
            return True
    except TzstDecompressionError as e:
        logger.error(f"Archive {archive_path} is corrupted: {e}")
    except TzstError as e:
        logger.error(f"tzst error for {archive_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error testing {archive_path}: {e}")
    
    return False
```

### Error Recovery Patterns

```python
from tzst import create_archive, extract_archive, TzstError
from pathlib import Path
import tempfile
import shutil

def robust_backup_and_restore(source_dir, backup_path, restore_dir):
    """Robust backup with error recovery and validation."""
    temp_backup = None
    
    try:
        # Create backup with temporary file for atomicity
        with tempfile.NamedTemporaryFile(suffix='.tzst', delete=False) as temp_file:
            temp_backup = Path(temp_file.name)
        
        # Create archive
        create_archive(temp_backup, [source_dir], compression_level=6)
        
        # Verify archive before moving to final location
        if not test_archive(temp_backup):
            raise TzstArchiveError("Created archive failed integrity check")
        
        # Move to final location atomically
        shutil.move(temp_backup, backup_path)
        temp_backup = None  # Successfully moved
        
        # Test restoration
        extract_archive(backup_path, restore_dir)
        
        print(f"Backup and restore completed successfully")
        return True
        
    except TzstError as e:
        print(f"tzst operation failed: {e}")
        # Cleanup and recovery logic
        if restore_dir.exists():
            shutil.rmtree(restore_dir)
        return False
          except Exception as e:
        print(f"Unexpected error: {e}")
        return False
        
    finally:
        # Cleanup temporary files
        if temp_backup and temp_backup.exists():
            temp_backup.unlink()
```
