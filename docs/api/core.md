---
html_meta:
  description: "tzst Core API - TzstArchive class and convenience functions for tar.zst archive operations"
  keywords: "tzst core API, TzstArchive, Python archive class, tar.zst functions"
  og:title: "tzst Core API Reference"
  og:description: "Core API documentation for tzst - TzstArchive class and convenience functions"
  twitter:title: "tzst Core API Reference"
  twitter:description: "Core API documentation for tzst - TzstArchive class and convenience functions"
---

# Core API

The core module provides the main functionality for working with tzst archives, including the primary `TzstArchive` class and high-level convenience functions.

```{eval-rst}
.. automodule:: tzst.core
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
```

## TzstArchive Class

The main class for handling `.tzst`/`.tar.zst` archives with comprehensive functionality for creation, extraction, and manipulation.

```{eval-rst}
.. autoclass:: tzst.TzstArchive
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __enter__, __exit__
```

### Key Features

- **Context Manager Support**: Use with `with` statements for automatic resource management
- **Multiple Access Modes**: Read ('r'), write ('w'), and append ('a') modes
- **Streaming Support**: Memory-efficient processing for large archives
- **Security Features**: Built-in protection against path traversal attacks
- **Flexible Extraction**: Support for selective extraction and conflict resolution

### Usage Examples

```python
# Create a new archive
with TzstArchive("backup.tzst", "w", compression_level=6) as archive:
    archive.add("important_file.txt")
    archive.add("documents/", recursive=True)

# Read an existing archive
with TzstArchive("backup.tzst", "r") as archive:
    contents = archive.list(verbose=True)
    is_valid = archive.test()
    archive.extractall("restore/")
```

## Convenience Functions

High-level functions for common archive operations without needing to instantiate the `TzstArchive` class directly.

### create_archive

```{eval-rst}
.. autofunction:: tzst.create_archive
```

Creates a new tzst archive from the specified files and directories.

**Key Features:**

- Configurable compression levels (1-22)
- Atomic creation using temporary files
- Automatic path validation and normalization
- Support for both files and directories

### extract_archive

```{eval-rst}
.. autofunction:: tzst.extract_archive
```

Extracts files from a tzst archive with advanced options for handling conflicts and filtering.

**Key Features:**

- Selective extraction with member filtering
- Multiple conflict resolution strategies
- Flatten option to extract all files to a single directory
- Streaming mode for memory efficiency
- Security filters to prevent path traversal attacks

### list_archive

```{eval-rst}
.. autofunction:: tzst.list_archive
```

Lists the contents of a tzst archive with optional detailed information.

**Returns:**

- List of dictionaries containing file information
- Each entry includes name, size, modification time, and type
- Verbose mode provides additional metadata

### test_archive

```{eval-rst}
.. autofunction:: tzst.test_archive
```

Tests the integrity of a tzst archive to verify it can be successfully decompressed.

**Returns:**

- `True` if the archive is valid and can be extracted
- `False` if the archive is corrupted or cannot be processed

## Enums and Supporting Classes

### ConflictResolution

Enumeration for handling file conflicts during extraction:

- `REPLACE`: Overwrite existing files
- `SKIP`: Skip existing files
- `REPLACE_ALL`: Overwrite all existing files without prompting
- `SKIP_ALL`: Skip all existing files without prompting
- `AUTO_RENAME`: Automatically rename conflicting files
- `AUTO_RENAME_ALL`: Automatically rename all conflicting files
- `ASK`: Prompt user for each conflict (interactive mode)
- `EXIT`: Stop extraction on first conflict

### ConflictResolutionState

State management class for tracking conflict resolution decisions during batch operations.
