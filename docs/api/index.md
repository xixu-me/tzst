---
myst:
  html_meta:
    description: "Complete tzst API reference - Core functions, CLI tools, and exception handling for tar.zst archives"
    keywords: "tzst API, Python API documentation, tar.zst API reference, archive API"
    og:title: "tzst API Reference"
    og:description: "Complete API reference for tzst - Core functions, CLI tools, and exception handling"
    twitter:title: "tzst API Reference"
    twitter:description: "Complete API reference for tzst - Core functions, CLI tools, and exception handling"
---

# API Reference

This section contains the complete API documentation for tzst, providing detailed information about classes, functions, and exceptions.

```{toctree}
:maxdepth: 2

core
cli
exceptions
```

## Overview

The tzst library provides both high-level convenience functions and a comprehensive class-based API for working with `.tzst`/`.tar.zst` archives. The library is designed with security, performance, and ease of use in mind.

### Main Components

- **{doc}`core`**: Core functionality including `TzstArchive` class and convenience functions for archive operations
- **{doc}`cli`**: Command-line interface functions and utilities for batch operations
- **{doc}`exceptions`**: Custom exception classes for comprehensive error handling and debugging

### Architecture Overview

The tzst library follows a layered architecture:

1. **High-Level API**: Convenience functions for common operations
2. **Class-Based API**: `TzstArchive` class for advanced control
3. **CLI Interface**: Command-line tools for interactive and scripted use
4. **Exception System**: Comprehensive error handling for robust applications

### Quick Reference

#### Core Classes

```{eval-rst}
.. currentmodule:: tzst

.. autosummary::
   :nosignatures:
   
   TzstArchive
```

The main class for archive manipulation with context manager support and comprehensive functionality.

#### Convenience Functions

```{eval-rst}
.. autosummary::
   :nosignatures:
   
   create_archive
   extract_archive
   list_archive
   test_archive
```

High-level functions that provide simple interfaces for common archive operations.

#### CLI Functions

```{eval-rst}
.. currentmodule:: tzst.cli

.. autosummary::
   :nosignatures:
   
   main
   create_parser
   print_banner
   format_size
   validate_compression_level
```

Command-line interface utilities for interactive and batch operations.

#### Exception Classes

```{eval-rst}
.. currentmodule:: tzst.exceptions

.. autosummary::
   :nosignatures:
   
   TzstError
   TzstArchiveError
   TzstCompressionError
   TzstDecompressionError
```

Exception hierarchy for comprehensive error handling and debugging support.

## Key Features

### 🛡️ Security First

- Built-in path traversal protection
- Multiple security filter options
- Safe extraction by default

### ⚡ High Performance  

- Zstandard compression with configurable levels
- Streaming support for large archives
- Memory-efficient operations

### 🔧 Developer Friendly

- Clean, Pythonic API
- Comprehensive error handling
- Context manager support
- Extensive documentation and examples

### 🌐 Cross-Platform

- Works on Windows, macOS, and Linux
- Consistent behavior across platforms
- Native performance optimizations
