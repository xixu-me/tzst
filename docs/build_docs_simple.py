#!/usr/bin/env python3
"""Simple development script for building documentation locally."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build(build_dir):
    """Clean the build directory."""
    if build_dir.exists():
        print(f"Cleaning {build_dir}")
        shutil.rmtree(build_dir)


def build_docs(source_dir, build_dir):
    """Build the documentation."""
    print(f"Building documentation: {source_dir} -> {build_dir}")
    cmd = [
        sys.executable, "-m", "sphinx",
        "-b", "html",
        str(source_dir),
        str(build_dir)
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Documentation built successfully!")
        index_file = build_dir / "index.html"
        print(f"Open {index_file} in your browser to view the documentation")
        return True
    except subprocess.CalledProcessError:
        print("Build failed!")
        return False


def main():
    parser = argparse.ArgumentParser(description="Build tzst documentation")
    parser.add_argument(
        "command",
        choices=["build", "clean"],
        help="Command to execute"
    )

    args = parser.parse_args()

    # Get directories
    script_dir = Path(__file__).parent
    source_dir = script_dir
    build_dir = script_dir / "_build"

    if args.command == "clean":
        clean_build(build_dir)
    elif args.command == "build":
        success = build_docs(source_dir, build_dir)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
