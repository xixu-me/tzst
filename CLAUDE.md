# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

tzst is a next-generation Python library for modern archive management using Zstandard compression. It provides both a Python API and a command-line interface for creating, extracting, listing, and testing .tzst/.tar.zst archives. The library focuses on performance, security, and reliability with features like atomic operations, streaming mode for large archives, and security filtering for extraction.

## Architecture

The codebase is structured as follows:

- `src/tzst/core.py` - Core implementation containing the `TzstArchive` class and convenience functions
- `src/tzst/cli.py` - Command-line interface built with argparse
- `src/tzst/exceptions.py` - Custom exception classes
- `src/tzst/__init__.py` - Public API exports

The library wraps Python's tarfile module with Zstandard compression/decompression streams. It supports both buffered and streaming modes for memory efficiency with large archives.

## Commands

### Development Environment

```bash
# Development installation with dev dependencies
pip install -e .[dev]

# Run tests
pytest
pytest --cov=tzst --cov-report=html  # with coverage
```

### Code Quality

```bash
# Check code quality
ruff check src tests

# Format code
ruff format src tests
```

### Building and Distribution

```bash
# Build package
python -m build

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

## Key Features to Consider

1. **Streaming Mode**: For archives >100MB, always recommend using streaming mode to reduce memory usage
2. **Security Filters**: Use 'data' filter by default for extraction to prevent path traversal attacks
3. **Atomic Operations**: Archive creation uses temporary files by default for safety
4. **Conflict Resolution**: During extraction, implement proper file conflict resolution strategies
5. **Compression Levels**: Default to level 3 unless the user has specific performance/size requirements

## Testing Patterns

The project uses pytest with comprehensive test coverage including:

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- CLI-specific tests in `tests/cli/`
- Edge case handling in `tests/test_core_edge_cases.py`

## Common Tasks

- To add functionality: work in `src/tzst/core.py` following existing patterns
- To modify CLI behavior: update `src/tzst/cli.py` and adjust argument parsing as needed
- To add new command: extend `create_parser()` in cli.py and add appropriate handler function
- For error handling: use appropriate TzstError subclasses from exceptions.py
