# tzst Documentation

Welcome to **tzst**, the next-generation Python library engineered for modern archive management, leveraging cutting-edge Zstandard compression to deliver superior performance, security, and reliability.

```{toctree}
:maxdepth: 2
:caption: Contents:

quickstart
api/index
examples
changelog
```

## What is tzst?

**tzst** is a Python library built exclusively for Python 3.12+ that provides enterprise-grade solutions for handling `.tzst`/`.tar.zst` archives. It combines atomic operations, streaming efficiency, and a meticulously crafted API to redefine how developers handle compressed archives in production environments.

## Key Features

- **🚀 High Performance**: Leverages Zstandard compression for superior speed and compression ratios
- **🔒 Security First**: Built-in extraction filters protect against malicious archives
- **⚡ Streaming Support**: Memory-efficient handling of large archives
- **🛡️ Atomic Operations**: Ensures data integrity with fail-safe file operations
- **🎯 Modern API**: Clean, intuitive interface designed for Python 3.12+
- **📦 CLI Tools**: Comprehensive command-line interface for everyday tasks

## Quick Example

```python
from tzst import TzstArchive

# Create a new archive
with TzstArchive("backup.tzst", "w", compression_level=5) as archive:
    archive.add("documents/")
    archive.add("photos/", recursive=True)

# Extract with security
with TzstArchive("backup.tzst", "r") as archive:
    archive.extract("documents/", filter="data")
```

## Installation

Install tzst from PyPI:

```bash
pip install tzst
```

## Getting Started

For a quick introduction to using tzst, see the {doc}`quickstart` guide.

For detailed API documentation, browse the {doc}`api/index` section.

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
