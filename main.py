#!/usr/bin/env python3
"""Standalone entry point for tzst - used for PyInstaller builds."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from tzst.cli import main

if __name__ == "__main__":
    sys.exit(main())
