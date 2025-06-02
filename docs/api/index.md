# API Reference

This section contains the complete API documentation for tzst.

```{toctree}
:maxdepth: 2

core
cli
exceptions
```

## Overview

The tzst library provides both high-level convenience functions and a comprehensive class-based API for working with `.tzst`/`.tar.zst` archives.

### Main Components

- **{doc}`core`**: Core functionality including `TzstArchive` class and convenience functions
- **{doc}`cli`**: Command-line interface functions and utilities  
- **{doc}`exceptions`**: Custom exception classes for error handling

### Quick Reference

#### Core Classes

```{eval-rst}
.. currentmodule:: tzst

.. autosummary::
   :nosignatures:
   
   TzstArchive
```

#### Convenience Functions

```{eval-rst}
.. autosummary::
   :nosignatures:
   
   create_archive
   extract_archive
   list_archive
   test_archive
```

#### Exceptions

```{eval-rst}
.. currentmodule:: tzst.exceptions

.. autosummary::
   :nosignatures:
   
   TzstArchiveError
   TzstDecompressionError
```
