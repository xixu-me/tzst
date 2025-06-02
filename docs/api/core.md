# Core API

The core module provides the main functionality for working with tzst archives.

```{eval-rst}
.. automodule:: tzst.core
   :members:
   :undoc-members:
   :show-inheritance:
```

## TzstArchive Class

The main class for handling `.tzst`/`.tar.zst` archives.

```{eval-rst}
.. autoclass:: tzst.TzstArchive
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __enter__, __exit__
```

## Convenience Functions

High-level functions for common archive operations.

### create_archive

```{eval-rst}
.. autofunction:: tzst.create_archive
```

### extract_archive

```{eval-rst}
.. autofunction:: tzst.extract_archive
```

### list_archive

```{eval-rst}
.. autofunction:: tzst.list_archive
```

### test_archive

```{eval-rst}
.. autofunction:: tzst.test_archive
```
