---
html_meta:
  description: "tzst CLI API - Command-line interface functions and utilities for tar.zst archive operations"
  keywords: "tzst CLI API, command line interface, Python CLI, tar.zst commands"
  og:title: "tzst CLI API Reference"
  og:description: "CLI API documentation for tzst - Command-line interface functions and utilities"
  twitter:title: "tzst CLI API Reference"
  twitter:description: "CLI API documentation for tzst - Command-line interface functions and utilities"
---

# CLI API

The command-line interface module provides comprehensive functionality for the tzst CLI tool, including argument parsing, command execution, and interactive features.

```{eval-rst}
.. automodule:: tzst.cli
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
```

## Overview

The tzst CLI provides a powerful command-line interface for archive operations with intuitive commands and comprehensive options. The interface is designed for both interactive use and scripting, with robust error handling and user-friendly output.

### 🔧 Core Commands

| Command | Aliases | Description | Streaming Support |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Create or add to archive | N/A |
| `x` | `extract` | Extract with full paths | ✓ `--streaming` |
| `e` | `extract-flat` | Extract without directory structure | ✓ `--streaming` |
| `l` | `list` | List archive contents | ✓ `--streaming` |
| `t` | `test` | Test archive integrity | ✓ `--streaming` |

### 🎯 Key Features

- **Intuitive Commands**: Simple, memorable command aliases (a, x, e, l, t)
- **Streaming Support**: Memory-efficient processing for large archives
- **Interactive Conflict Resolution**: User-friendly prompts for handling file conflicts
- **Comprehensive Options**: Fine-grained control over compression, extraction, and security
- **Cross-Platform**: Consistent behavior across Windows, macOS, and Linux

## Main Functions

### main

```{eval-rst}
.. autofunction:: tzst.cli.main
```

The main entry point for the CLI application. Handles argument parsing, command execution, and comprehensive error reporting.

**Key Features:**

- Robust argument validation and error handling
- Support for all archive operations
- Consistent exit codes for scripting
- User-friendly error messages

**Exit Codes:**

- `0`: Success
- `1`: General error (file not found, archive corruption, etc.)
- `2`: Argument parsing error
- `130`: Interrupted by user (Ctrl+C)

### create_parser

```{eval-rst}
.. autofunction:: tzst.cli.create_parser
```

Creates and configures the comprehensive argument parser for the CLI interface.

**Supported Arguments:**

- **Global**: `--version`, `--help`
- **Archive Creation**: `-l/--level`, `--no-atomic`
- **Extraction**: `-o/--output`, `--streaming`, `--filter`, `--conflict-resolution`
- **Listing**: `-v/--verbose`, `--streaming`
- **Testing**: `--streaming`

## Command Handlers

The CLI implements dedicated command handlers for each operation, providing specialized functionality and error handling.

### Archive Creation Commands

#### cmd_add

Creates new archives from files and directories with configurable compression and atomic operations.

**Features:**

- Configurable compression levels (1-22)
- Atomic file operations (default) for safe creation
- Recursive directory processing
- Path validation and normalization

**Usage Examples:**

```bash
# Basic archive creation
tzst a backup.tzst documents/ photos/

# High compression with atomic disabled
tzst a backup.tzst files/ -l 15 --no-atomic
```

### Extraction Commands

#### cmd_extract_full

Extracts archives preserving complete directory structure with advanced conflict resolution.

**Features:**

- Preserves full directory paths
- Multiple conflict resolution strategies
- Security filters for safe extraction
- Selective file extraction
- Streaming mode for large archives

#### cmd_extract_flat

Extracts archives flattening all files to a single directory, useful for consolidating files.

**Features:**

- Flattens directory structure
- Automatic conflict resolution for filename collisions
- Preserves file content while simplifying structure
- Same security and streaming features as full extraction

### Management Commands

#### cmd_list

Lists archive contents with optional detailed information and streaming support.

**Features:**

- Simple or verbose listing modes
- Human-readable file sizes
- Modification timestamps
- Streaming mode for memory efficiency

#### cmd_test

Tests archive integrity and validity with comprehensive error reporting.

**Features:**

- Complete archive validation
- Streaming mode support
- Detailed error reporting
- Exit codes for automated testing

#### cmd_version

Displays version information and system details.

## Utility Functions

### print_banner

```{eval-rst}
.. autofunction:: tzst.cli.print_banner
```

Displays the application banner with version and copyright information.

### format_size

```{eval-rst}
.. autofunction:: tzst.cli.format_size
```

Formats file sizes in a human-readable format (bytes, KB, MB, GB).

### validate_compression_level

```{eval-rst}
.. autofunction:: tzst.cli.validate_compression_level
```

Validates compression level arguments and converts them to integers.

## Interactive Features

The CLI includes interactive conflict resolution for file extraction conflicts, allowing users to choose how to handle existing files during extraction operations.

### Conflict Resolution Options

- **Replace**: Overwrite the existing file
- **Skip**: Keep the existing file, skip extraction
- **Replace All**: Apply replace to all subsequent conflicts
- **Skip All**: Apply skip to all subsequent conflicts  
- **Auto-rename All**: Automatically rename conflicting files
- **Exit**: Stop extraction process

### Security Considerations

The CLI implements multiple security filters for safe extraction:

- **`data` filter** (default): Safest option, blocks potentially dangerous archive members
- **`tar` filter**: Preserves more tar features while maintaining basic security
- **`fully_trusted` filter**: No restrictions, use only with completely trusted archives

### Performance Options

- **Streaming Mode**: Use `--streaming` for memory-efficient processing of large archives (>100MB)
- **Compression Levels**: Choose from 1 (fastest) to 22 (maximum compression)
- **Atomic Operations**: Default behavior uses temporary files for safe archive creation
