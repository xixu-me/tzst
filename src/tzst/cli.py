"""Command-line interface for tzst."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import create_archive, extract_archive, list_archive, test_archive
from .exceptions import TzstArchiveError, TzstDecompressionError


def print_banner() -> None:
    """Print the version and copyright banner.

    Displays the tzst version number and copyright information to stdout.
    Used as a header for CLI operations.

    Returns:
        None
    """
    print()
    print(f"tzst {__version__} : Copyright (c) 2025 Xi Xu")
    print()


def format_size(size: int) -> str:
    """Format file size in human-readable format.

    Converts byte values to human-readable format using standard units
    (B, KB, MB, GB, TB, PB) with appropriate decimal places.

    Args:
        size (int): Size in bytes to format

    Returns:
        str: Formatted size string with units (e.g., "1.5 KB", "2.3 GB")

    Examples:
        >>> format_size(1024)
        '  1.0 KB'
        >>> format_size(1536)
        '  1.5 KB'
        >>> format_size(2048576)
        '  2.0 MB'
    """
    size_float = float(size)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_float < 1024.0:
            return f"{size_float:6.1f} {unit}"
        size_float /= 1024.0
    return f"{size_float:6.1f} PB"


def validate_compression_level(value: str) -> int:
    """Validate and return compression level.

    Args:
        value: String value from command line

    Returns:
        int: Valid compression level (1-22)

    Raises:
        argparse.ArgumentTypeError: If value is not a valid compression level
    """
    try:
        level = int(value)
        if not 1 <= level <= 22:
            raise argparse.ArgumentTypeError(
                f"Invalid compression level: {level}. Must be between 1 and 22."
            )
        return level
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid compression level: '{value}'. Must be an integer between 1 and 22."
        ) from None


def _process_file_paths(file_args: list[str]) -> list[Path]:
    """Process file arguments into resolved Path objects.

    Args:
        file_args: List of file path strings from command line

    Returns:
        list[Path]: List of resolved Path objects
    """
    files: list[Path] = []
    for file_arg in file_args:
        file_path = Path(file_arg).resolve()
        files.append(file_path)
    return files


def _validate_files(files: list[Path]) -> list[Path]:
    """Validate that files exist and are accessible.

    Args:
        files: List of Path objects to validate

    Returns:
        list[Path]: List of missing files (empty if all files exist)

    Raises:
        OSError: If a file cannot be accessed due to permissions or invalid characters
    """
    missing_files = []
    for f in files:
        try:
            if not f.exists():
                missing_files.append(f)
        except OSError as e:
            # Handle path issues (invalid characters, permissions, etc.)
            print(f"Error: Cannot access file '{f}' - {e}", file=sys.stderr)
            raise
    return missing_files


def _extract_add_params(args) -> tuple[int, bool]:
    """Extract compression parameters from arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        tuple[int, bool]: (compression_level, use_temp_file)
    """
    compression_level = getattr(args, "compression_level", 3)
    use_temp_file = not getattr(args, "no_atomic", False)
    return compression_level, use_temp_file


def _prepare_archive_creation(args) -> tuple[Path, list[Path], int, bool] | int:
    """Prepare and validate inputs for archive creation.

    Args:
        args: Parsed command line arguments

    Returns:
        tuple or int: Either (archive_path, files, compression_level, use_temp_file)
                     or error code if validation fails
    """
    archive_path = Path(args.archive)
    files = _process_file_paths(args.files)

    # Validate files
    missing_files = _validate_files(files)
    if missing_files:
        print(
            f"Error: Files not found - {', '.join(map(str, missing_files))}",
            file=sys.stderr,
        )
        return 1

    compression_level, use_temp_file = _extract_add_params(args)
    return archive_path, files, compression_level, use_temp_file


def _execute_archive_creation(
    archive_path: Path, files: list[Path], compression_level: int, use_temp_file: bool
) -> int:
    """Execute the archive creation process.

    Args:
        archive_path: Path where archive will be created
        files: List of files to add to archive
        compression_level: Compression level to use
        use_temp_file: Whether to use atomic file operations

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    print(f"Creating archive: {archive_path}")
    for file_path in files:
        print(f"  Adding: {file_path}")

    # Use atomic file operations by default for better reliability
    # This creates the archive in a temporary file first, then moves it
    create_archive(archive_path, files, compression_level, use_temp_file=use_temp_file)
    print(f"Archive created successfully - {archive_path}")
    return 0


def _handle_archive_creation_exceptions(func, *args, **kwargs) -> int:
    """Handle exceptions during archive creation.

    Args:
        func: Function to execute
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        int: Exit code based on exception type
    """
    try:
        return func(*args, **kwargs)
    except OSError:
        return 1  # Error already printed in _validate_files
    except ValueError as e:
        print(f"Error: Invalid parameter - {e}", file=sys.stderr)
        return 1
    except TzstArchiveError as e:
        print(f"Error: Archive operation failed - {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation interrupted by user", file=sys.stderr)
        # Clean up any partial files - the atomic operations in create_archive
        # handle this
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        print(f"Error: Failed to create archive - {e}", file=sys.stderr)
        return 1


def cmd_add(args) -> int:
    """Command handler for creating/adding to archives.

    Processes the 'add', 'create', or 'a' CLI commands to create new tzst archives
    with the specified files and directories. Uses atomic file operations by
    default to ensure data integrity.

    Args:
        args: Parsed command line arguments containing:
            - archive (str): Path to the archive file to create
            - files (list[str]): List of files/directories to add
            - compression_level (int, optional): Compression level 1-22
            - no_atomic (bool, optional): Disable atomic file operations

    Returns:
        int: Exit code (0 for success, non-zero for failure)
            - 0: Success
            - 1: File not found, invalid parameters, or archive operation failed
            - 130: Operation interrupted by user (Ctrl+C)

    Note:
        This function uses atomic file operations by default, creating the
        archive in a temporary file first, then atomically moving it to the
        final location to prevent incomplete archives.

    See Also:
        :func:`tzst.create_archive`: The underlying function for archive creation
        :meth:`TzstArchive.add`: The core method for adding files to archives
    """

    def _create_archive_workflow():
        preparation_result = _prepare_archive_creation(args)
        if isinstance(preparation_result, int):
            return preparation_result

        archive_path, files, compression_level, use_temp_file = preparation_result
        return _execute_archive_creation(
            archive_path, files, compression_level, use_temp_file
        )

    return _handle_archive_creation_exceptions(_create_archive_workflow)


def cmd_extract_full(args) -> int:
    """Command handler for extracting archives with full directory structure.

    Processes the 'extract' or 'x' CLI commands to extract files from tzst
    archives while preserving the original directory structure.

    Args:
        args: Parsed command line arguments containing:
            - archive (str): Path to the archive file to extract
            - output (str, optional): Output directory path
            - files (list[str], optional): Specific files to extract
            - streaming (bool, optional): Use streaming mode for large archives
            - filter (str, optional): Security filter ('data', 'tar', 'fully_trusted')

    Returns:
        int: Exit code (0 for success, non-zero for failure)
            - 0: Success
            - 1: File not found, decompression failed, or archive operation failed
            - 130: Operation interrupted by user (Ctrl+C)

    Note:
        Uses the 'data' security filter by default for safe extraction from
        untrusted sources. Streaming mode is recommended for archives > 100MB.

    See Also:
        :func:`tzst.extract_archive`: The underlying function for extraction
        :meth:`TzstArchive.extract`: The core method for extracting from archives
        :func:`cmd_extract_flat`: For flat extraction without directory structure
    """
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found - {archive_path}", file=sys.stderr)
            return 1

        output_dir = Path(args.output) if args.output else Path.cwd()
        members = args.files if hasattr(args, "files") and args.files else None
        streaming = getattr(args, "streaming", False)
        filter_type = getattr(args, "filter", "data")

        print(f"Extracting from: {archive_path}")
        print(f"Output directory: {output_dir}")
        if streaming:
            print("Using streaming mode (memory efficient)")
        if filter_type != "data":
            print(f"Using security filter: {filter_type}")

        extract_archive(
            archive_path,
            output_dir,
            members,
            flatten=False,
            streaming=streaming,
            filter=filter_type,
        )
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
    except KeyboardInterrupt:
        print("\nOperation interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: Failed to extract archive - {e}", file=sys.stderr)
        return 1


def cmd_extract_flat(args) -> int:
    """Command handler for flat extraction without directory structure.

    Processes the 'extract-flat' or 'e' CLI commands to extract files from
    tzst archives without preserving directory structure (all files extracted
    to a single directory).

    Args:
        args: Parsed command line arguments containing:
            - archive (str): Path to the archive file to extract
            - output (str, optional): Output directory path
            - files (list[str], optional): Specific files to extract
            - streaming (bool, optional): Use streaming mode for large archives
            - filter (str, optional): Security filter ('data', 'tar', 'fully_trusted')

    Returns:
        int: Exit code (0 for success, non-zero for failure)
            - 0: Success
            - 1: File not found, decompression failed, or archive operation failed
            - 130: Operation interrupted by user (Ctrl+C)

    Warning:
        Flat extraction may cause filename conflicts if multiple files have
        the same name but are in different directories within the archive.

    See Also:
        :func:`tzst.extract_archive`: The underlying function for extraction
        :meth:`TzstArchive.extract`: The core method for extracting from archives
        :func:`cmd_extract_full`: For extraction with directory structure
    """
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found - {archive_path}", file=sys.stderr)
            return 1

        output_dir = Path(args.output) if args.output else Path.cwd()
        members = args.files if hasattr(args, "files") and args.files else None
        streaming = getattr(args, "streaming", False)
        filter_type = getattr(args, "filter", "data")

        print(f"Extracting from: {archive_path}")
        print(f"Output directory: {output_dir}")
        if filter_type != "data":
            print(f"Using security filter: {filter_type}")

        extract_archive(
            archive_path,
            output_dir,
            members,
            flatten=True,
            streaming=streaming,
            filter=filter_type,
        )
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
        print(f"Error: Failed to extract archive - {e}", file=sys.stderr)
        return 1


def _print_verbose_listing(contents: list) -> None:
    """Print detailed listing of archive contents.

    Args:
        contents: List of archive items with metadata
    """
    print(f"{'Mode':<10} {'Size':<10} {'Modified':<20} {'Name'}")
    print("-" * 60)
    for item in contents:
        mode_str = oct(item.get("mode", 0))[-4:] if item.get("mode") else "----"
        size_str = format_size(item["size"]) if item["is_file"] else "<DIR>"
        mtime_str = item.get("mtime_str", "")[:19] if item.get("mtime_str") else ""
        print(f"{mode_str:<10} {size_str:<10} {mtime_str:<20} {item['name']}")


def _print_simple_listing(contents: list) -> None:
    """Print simple listing of archive contents with summary.

    Args:
        contents: List of archive items
    """
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
    total_msg = (
        f"Total: {total_files} files, {total_dirs} directories, "
        f"{format_size(total_size)}"
    )
    print(total_msg)


def cmd_list(args) -> int:
    """Command handler for listing archive contents.

    Processes the 'list' or 'l' CLI commands to display the contents of tzst
    archives. Supports both simple and verbose listing modes.

    Args:
        args: Parsed command line arguments containing:
            - archive (str): Path to the archive file to list
            - verbose (bool, optional): Show detailed file information
            - streaming (bool, optional): Use streaming mode for large archives

    Returns:
        int: Exit code (0 for success, non-zero for failure)
            - 0: Success
            - 1: File not found, decompression failed, or archive operation failed
            - 130: Operation interrupted by user (Ctrl+C)

    Note:
        Verbose mode displays file permissions, sizes, modification times,
        and other metadata. Streaming mode is recommended for archives > 100MB.

    See Also:
        :func:`tzst.list_archive`: The underlying function for listing contents
        :meth:`TzstArchive.list`: The core method for listing archive contents
    """
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found - {archive_path}", file=sys.stderr)
            return 1

        verbose = getattr(args, "verbose", False)
        streaming = getattr(args, "streaming", False)

        print(f"Listing contents of: {archive_path}")
        if streaming:
            print("Using streaming mode (memory efficient)")
        print()

        contents = list_archive(archive_path, verbose=verbose, streaming=streaming)

        if verbose:
            _print_verbose_listing(contents)
        else:
            _print_simple_listing(contents)

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
        print(f"Error: Failed to list archive - {e}", file=sys.stderr)
        return 1


def cmd_test(args) -> int:
    """Command handler for testing archive integrity.

    Processes the 'test' or 't' CLI commands to verify the integrity of tzst
    archives by attempting to read all files and checking for corruption.

    Args:
        args: Parsed command line arguments containing:
            - archive (str): Path to the archive file to test
            - streaming (bool, optional): Use streaming mode for large archives

    Returns:
        int: Exit code (0 for success, non-zero for failure)
            - 0: Archive passed integrity test
            - 1: Archive failed integrity test, file not found, or operation failed
            - 130: Operation interrupted by user (Ctrl+C)

    Note:
        This command verifies that the archive can be read and all files
        can be decompressed without errors. Streaming mode is recommended
        for archives > 100MB to reduce memory usage.

    See Also:
        :func:`tzst.test_archive`: The underlying function for integrity testing
        :meth:`TzstArchive.test`: The core method for testing archive integrity
    """
    try:
        archive_path = Path(args.archive)
        if not archive_path.exists():
            print(f"Error: Archive not found - {archive_path}", file=sys.stderr)
            return 1

        streaming = getattr(args, "streaming", False)

        print(f"Testing archive: {archive_path}")
        if streaming:
            print("Using streaming mode (memory efficient)")

        if test_archive(archive_path, streaming=streaming):
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
        print(f"Error: Failed to test archive - {e}", file=sys.stderr)
        return 1


def cmd_version(args) -> int:
    """Command handler for version display.

    Returns:
        int: Exit code (always 0)
    """
    # Version is already printed in print_banner(), so just exit
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser.

    Sets up the argparse ArgumentParser with all subcommands and their
    respective arguments for the tzst CLI interface. Includes comprehensive
    help text and command reference documentation.

    Returns:
        argparse.ArgumentParser: Configured parser ready for argument parsing

    Note:
        The parser is configured with RawDescriptionHelpFormatter to preserve
        formatting in the epilog help text, and includes detailed command
        reference and security notes.

    Commands Created:
        - a, add, create: Archive creation with compression levels
        - x, extract: Full extraction with directory structure
        - e, extract-flat: Flat extraction without directories
        - l, list: Archive content listing
        - t, test: Archive integrity testing

    See Also:
        :func:`main`: The main entry point that uses this parser
    """
    epilog = """
Command Reference:
  Archive:
    a, add, create    tzst a archive.tzst files...  [-l LEVEL] [--no-atomic]

  Extract:
    x, extract        tzst x archive.tzst [files...] [-o DIR] [--streaming] [--filter FILTER]
    e, extract-flat   tzst e archive.tzst [files...] [-o DIR] [--streaming] [--filter FILTER]

  Manage:
    l, list           tzst l archive.tzst [-v] [--streaming]
    t, test           tzst t archive.tzst [--streaming]

Arguments:
  -l, --level LEVEL   Compression level (1-22, default: 3)
  -o, --output DIR    Output directory (default: current directory)
  -v, --verbose       Show detailed information
  --streaming         Use streaming mode for memory efficiency with large archives
  --filter FILTER     Security filter for extraction: data (safest, default), tar, fully_trusted
  --no-atomic         Disable atomic file operations (not recommended)

Security Note:
  Always use --filter=data (default) when extracting archives from untrusted sources.
  Never use --filter=fully_trusted unless you completely trust the archive source.

Documentation:
  https://github.com/xixu-me/tzst#readme
"""
    parser = argparse.ArgumentParser(
        prog="tzst",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
    )
    parser.add_argument(
        "--version", action="store_true", help="show version information and exit"
    )

    # Add global arguments
    subparsers = parser.add_subparsers(
        dest="command", title="Commands", help="Available commands", metavar="COMMAND"
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
        type=validate_compression_level,
        default=3,
        metavar="LEVEL",
        help="Compression level (1-22, default: 3)",
    )
    parser_add.add_argument(
        "--no-atomic",
        action="store_true",
        help=(
            "Disable atomic file operations (not recommended - creates archive "
            "directly without temporary file)"
        ),
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
    parser_extract.add_argument(
        "--streaming",
        action="store_true",
        help="Use streaming mode for memory efficiency with large archives",
    )
    parser_extract.add_argument(
        "--filter",
        choices=["data", "tar", "fully_trusted"],
        default="data",
        help=(
            "Extraction filter for security (default: data). 'data' is safest "
            "for untrusted archives, 'tar' honors most tar features, "
            "'fully_trusted' honors all metadata"
        ),
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
    parser_extract_flat.add_argument(
        "--streaming",
        action="store_true",
        help="Use streaming mode for memory efficiency with large archives",
    )
    parser_extract_flat.add_argument(
        "--filter",
        choices=["data", "tar", "fully_trusted"],
        default="data",
        help=(
            "Extraction filter for security (default: data). 'data' is safest "
            "for untrusted archives, 'tar' honors most tar features, "
            "'fully_trusted' honors all metadata"
        ),
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
    parser_list.add_argument(
        "--streaming",
        action="store_true",
        help="Use streaming mode for memory efficiency with large archives",
    )
    parser_list.set_defaults(func=cmd_list)

    # Test command
    parser_test = subparsers.add_parser(
        "t", aliases=["test"], help="Test integrity of archive"
    )
    parser_test.add_argument("archive", help="Archive file path")
    parser_test.add_argument(
        "--streaming",
        action="store_true",
        help="Use streaming mode for memory efficiency with large archives",
    )
    parser_test.set_defaults(func=cmd_test)

    return parser


def _validate_compression_level_in_argv(argv: list[str]) -> bool:
    """Check for compression level validation errors in argv.

    Args:
        argv: Command line arguments

    Returns:
        bool: True if an error was found and handled, False otherwise
    """
    if "-l" not in argv and "--level" not in argv:
        return False

    try:
        level_index = argv.index("-l") if "-l" in argv else argv.index("--level")
        if level_index + 1 < len(argv):
            level_value = argv[level_index + 1]
            try:
                level = int(level_value)
                if not 1 <= level <= 22:
                    print(
                        f"Invalid compression level: {level}. "
                        f"Must be between 1 and 22.",
                        file=sys.stderr,
                    )
                    return True
            except ValueError:
                print(
                    f"Invalid compression level: '{level_value}'. "
                    f"Must be an integer between 1 and 22.",
                    file=sys.stderr,
                )
                return True
    except (ValueError, IndexError):
        pass
    return False


def _validate_filter_in_argv(argv: list[str]) -> bool:
    """Check for filter validation errors in argv.

    Args:
        argv: Command line arguments

    Returns:
        bool: True if an error was found and handled, False otherwise
    """
    if "--filter" not in argv:
        return False

    try:
        filter_index = argv.index("--filter")
        if filter_index + 1 < len(argv):
            filter_value = argv[filter_index + 1]
            valid_filters = ["data", "tar", "fully_trusted"]
            if filter_value not in valid_filters:
                print(
                    f"Invalid filter specified: {filter_value}. "
                    f"Must be one of: {', '.join(valid_filters)}",
                    file=sys.stderr,
                )
                return True
    except (ValueError, IndexError):
        pass
    return False


def _handle_parsing_errors(e: SystemExit, argv: list[str] | None) -> int:
    """Handle SystemExit exceptions from argument parsing.

    Args:
        e: SystemExit exception from argparse
        argv: Command line arguments, if any

    Returns:
        int: Appropriate exit code
    """
    # Help was requested
    if e.code == 0:
        return 0
    elif e.code == 2 and argv:
        # Check for validation errors we want to convert to exit code 1
        if _validate_filter_in_argv(argv):
            return 1

    # Return the original exit code for other cases
    return int(e.code) if e.code is not None else 1


def _parse_arguments(parser, argv: list[str] | None):
    """Parse command line arguments with error handling.

    Args:
        parser: The argument parser
        argv: Command line arguments

    Returns:
        tuple: (args, error_code) where error_code is None for success
    """
    try:
        args = parser.parse_args(argv)
        return args, None
    except SystemExit as e:
        return None, _handle_parsing_errors(e, argv)


def _execute_command(args, parser) -> int:
    """Execute the parsed command.

    Args:
        args: Parsed command line arguments
        parser: The argument parser for help display

    Returns:
        int: Exit code from command execution
    """
    # Handle --version flag
    if hasattr(args, "version") and args.version:
        return cmd_version(args)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the tzst command-line interface.

    Processes command-line arguments and dispatches to appropriate command
    handlers. Displays the version banner and provides error handling for
    the overall CLI execution.

    Args:
        argv (list[str] | None, optional): Command line arguments to parse.
            If None, uses sys.argv. Defaults to None.

    Returns:
        int: Exit code for the program
            - 0: Success
            - 1: Invalid compression level, filter, or command error
            - 2: Argument parsing error (help, unknown options)
            - Other codes: Specific to individual command handlers

    Note:
        This function serves as the console script entry point defined in
        pyproject.toml. It displays the version banner before executing
        any commands.

    See Also:
        :func:`create_parser`: Creates the argument parser used by this function
    """
    print_banner()

    parser = create_parser()
    args, error_code = _parse_arguments(parser, argv)

    if error_code is not None:
        return error_code

    return _execute_command(args, parser)


if __name__ == "__main__":
    sys.exit(main())
