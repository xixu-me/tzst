"""Command-line interface for tzst."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .core import create_archive, extract_archive, list_archive, test_archive
from .exceptions import TzstArchiveError, TzstDecompressionError


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    size_float = float(size)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_float < 1024.0:
            return f"{size_float:6.1f} {unit}"
        size_float /= 1024.0
    return f"{size_float:6.1f} PB"


def cmd_add(args) -> int:
    """Add/create archive command."""
    try:
        archive_path = Path(args.archive)
        files: List[Path] = [Path(f) for f in args.files]

        # Check if files exist
        missing_files = [f for f in files if not f.exists()]
        if missing_files:
            print(
                f"Error: Files not found: {', '.join(map(str, missing_files))}",
                file=sys.stderr,
            )
            return 1

        compression_level = getattr(args, "compression_level", 3)

        print(f"Creating archive: {archive_path}")
        for file_path in files:
            print(
                f"  Adding: {file_path}"
            )  # Convert to the right type for create_archive function
        create_archive(archive_path, files, compression_level)
        print(f"Archive created successfully: {archive_path}")
        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: Invalid parameter - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error creating archive: {e}", file=sys.stderr)
        return 1


def cmd_extract_full(args) -> int:
    """Extract with full paths command."""
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
            return 1

        output_dir = Path(args.output) if args.output else Path.cwd()
        members = args.files if hasattr(args, "files") and args.files else None

        print(f"Extracting from: {archive_path}")
        print(f"Output directory: {output_dir}")

        extract_archive(archive_path, output_dir, members, flatten=False)
        print("Extraction completed successfully")
        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except TzstDecompressionError as e:
        print(f"Error: Archive decompression failed - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error extracting archive: {e}", file=sys.stderr)
        return 1


def cmd_extract_flat(args) -> int:
    """Extract without paths (flat) command."""
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
            return 1

        output_dir = Path(args.output) if args.output else Path.cwd()
        members = args.files if hasattr(args, "files") and args.files else None

        print(f"Extracting from: {archive_path}")
        print(f"Output directory: {output_dir}")

        extract_archive(archive_path, output_dir, members, flatten=True)
        print("Extraction completed successfully")
        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except TzstDecompressionError as e:
        print(f"Error: Archive decompression failed - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error extracting archive: {e}", file=sys.stderr)
        return 1


def cmd_list(args) -> int:
    """List contents of archive command."""
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
            return 1

        verbose = getattr(args, "verbose", False)

        print(f"Listing contents of: {archive_path}")
        print()

        contents = list_archive(archive_path, verbose=verbose)

        if verbose:
            # Detailed listing
            print(f"{'Mode':<10} {'Size':<10} {'Modified':<20} {'Name'}")
            print("-" * 60)
            for item in contents:
                mode_str = oct(item.get("mode", 0))[-4:] if item.get("mode") else "----"
                size_str = format_size(item["size"]) if item["is_file"] else "<DIR>"
                mtime_str = (
                    item.get("mtime_str", "")[:19] if item.get("mtime_str") else ""
                )
                print(f"{mode_str:<10} {size_str:<10} {mtime_str:<20} {item['name']}")
        else:
            # Simple listing
            total_files = 0
            total_dirs = 0
            total_size = 0

            for item in contents:
                if item["is_file"]:
                    total_files += 1
                    total_size += item["size"]
                elif item["is_dir"]:
                    total_dirs += 1
                print(item["name"])

            print()
            print(
                f"Total: {total_files} files, {total_dirs} directories, {format_size(total_size)}"
            )

        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except TzstDecompressionError as e:
        print(f"Error: Archive decompression failed - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error listing archive: {e}", file=sys.stderr)
        return 1


def cmd_test(args) -> int:
    """Test integrity of archive command."""
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
            return 1

        print(f"Testing archive: {archive_path}")

        if test_archive(archive_path):
            print("Archive test passed - no errors detected")
            return 0
        else:
            print("Archive test failed - errors detected", file=sys.stderr)
            return 1

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except TzstDecompressionError as e:
        print(f"Error: Archive decompression failed - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error testing archive: {e}", file=sys.stderr)
        return 1


def create_parser() -> argparse.ArgumentParser:
    epilog = """
Command Reference:
  Archive:
    a, add, create     tzst a archive.tzst files...  [-l LEVEL]

  Extract:
    x, extract         tzst x archive.tzst [files...] [-o DIR]  # with paths
    e, extract-flat    tzst e archive.tzst [files...] [-o DIR]  # without paths

  Manage:
    l, list            tzst l archive.tzst [-v]
    t, test            tzst t archive.tzst
"""

    parser = argparse.ArgumentParser(
        prog="tzst",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"tzst {__version__} : Copyright (c) 2025 Xi Xu",
    )

    subparsers = parser.add_subparsers(
        dest="command", title="commands", help="Available commands", metavar="COMMAND"
    )

    # Add/Create command
    parser_add = subparsers.add_parser(
        "a", aliases=["add", "create"], help="Add files to archive"
    )
    parser_add.add_argument("archive", help="Archive file path")
    parser_add.add_argument("files", nargs="+", help="Files/directories to add")
    parser_add.add_argument(
        "-l",
        "--level",
        dest="compression_level",
        type=int,
        default=3,
        choices=range(1, 23),
        metavar="LEVEL",
        help="Compression level (1-22, default: 3)",
    )
    parser_add.set_defaults(func=cmd_add)

    # Extract with full paths command
    parser_extract = subparsers.add_parser(
        "x", aliases=["extract"], help="eXtract files with full paths"
    )
    parser_extract.add_argument("archive", help="Archive file path")
    parser_extract.add_argument("files", nargs="*", help="Specific files to extract")
    parser_extract.add_argument(
        "-o", "--output", help="Output directory (default: current directory)"
    )
    parser_extract.set_defaults(func=cmd_extract_full)

    # Extract flat command
    parser_extract_flat = subparsers.add_parser(
        "e",
        aliases=["extract-flat"],
        help="Extract files from archive (without using directory names)",
    )
    parser_extract_flat.add_argument("archive", help="Archive file path")
    parser_extract_flat.add_argument(
        "files", nargs="*", help="Specific files to extract"
    )
    parser_extract_flat.add_argument(
        "-o", "--output", help="Output directory (default: current directory)"
    )
    parser_extract_flat.set_defaults(func=cmd_extract_flat)

    # List command
    parser_list = subparsers.add_parser(
        "l", aliases=["list"], help="List contents of archive"
    )
    parser_list.add_argument("archive", help="Archive file path")
    parser_list.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed information"
    )
    parser_list.set_defaults(func=cmd_list)

    # Test command
    parser_test = subparsers.add_parser(
        "t", aliases=["test"], help="Test integrity of archive"
    )
    parser_test.add_argument("archive", help="Archive file path")
    parser_test.set_defaults(func=cmd_test)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
