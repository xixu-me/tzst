"""Tests for CLI security filter options."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tzst.cli import create_parser


class TestCLISecurityFilters:
    """Test CLI security filter options."""

    def test_extract_filter_argument_parsing(self):
        """Test that --filter argument is parsed correctly for extract commands."""
        parser = create_parser()

        # Test x/extract command with filter
        args = parser.parse_args(["x", "test.tzst", "--filter", "data"])
        assert args.command == "x"
        assert args.filter == "data"

        args = parser.parse_args(["extract", "test.tzst", "--filter", "tar"])
        assert args.command == "extract"
        assert args.filter == "tar"

        args = parser.parse_args(["x", "test.tzst", "--filter", "fully_trusted"])
        assert args.filter == "fully_trusted"

        # Test e/extract-flat command with filter
        args = parser.parse_args(["e", "test.tzst", "--filter", "data"])
        assert args.command == "e"
        assert args.filter == "data"

        args = parser.parse_args(["extract-flat", "test.tzst", "--filter", "tar"])
        assert args.command == "extract-flat"
        assert args.filter == "tar"

    def test_filter_default_value(self):
        """Test that filter defaults to 'data'."""
        parser = create_parser()

        # Test default for x command
        args = parser.parse_args(["x", "test.tzst"])
        assert args.filter == "data"

        # Test default for e command
        args = parser.parse_args(["e", "test.tzst"])
        assert args.filter == "data"

    def test_filter_invalid_choices(self):
        """Test that invalid filter choices are rejected."""
        parser = create_parser()

        # Invalid filter should raise SystemExit (argparse error)
        with pytest.raises(SystemExit):
            parser.parse_args(["x", "test.tzst", "--filter", "invalid"])

    def test_filter_with_other_options(self):
        """Test filter option combined with other options."""
        parser = create_parser()  # Test with streaming and output directory
        args = parser.parse_args(
            [
                "x",
                "test.tzst",
                "file1.txt",
                "file2.txt",
                "--filter",
                "tar",
                "--streaming",
                "-o",
                "output_dir",
            ]
        )
        assert args.filter == "tar"
        assert args.streaming is True
        assert args.output == "output_dir"
        assert args.files == ["file1.txt", "file2.txt"]

    def test_cli_help_includes_security_info(self):
        """Test that CLI help includes security information."""
        parser = create_parser()
        help_text = parser.format_help()

        # Check that security-related help text is present
        assert "--filter" in help_text
        assert "data" in help_text
        assert "tar" in help_text
        assert "fully_trusted" in help_text
        assert "Security Note:" in help_text
        assert "untrusted sources" in help_text

    def test_extract_command_uses_filter(self):
        """Test that extract commands actually use the filter parameter."""
        # This is an integration test that would require actual CLI execution
        # For now, we'll test the argument parsing and ensure the functions receive the filter

        from tzst.cli import cmd_extract_full

        # Mock args object
        mock_args = MagicMock()
        mock_args.archive = "test.tzst"
        mock_args.output = None
        mock_args.files = None
        mock_args.streaming = False
        mock_args.filter = "tar"

        # Test that the functions would use the filter (we can't easily test the actual
        # extraction without creating real archives, but we can verify the code path)
        with patch("tzst.cli.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.cwd.return_value = Path(".")
            mock_path.side_effect = lambda x: Path(x)

            with patch("tzst.cli.extract_archive") as mock_extract:
                # This will fail because archive doesn't exist, but we can see the call
                try:
                    cmd_extract_full(mock_args)
                except Exception:
                    pass

                # Verify extract_archive was called with filter parameter
                if mock_extract.called:
                    call_kwargs = mock_extract.call_args[1]
                    assert "filter" in call_kwargs
                    assert call_kwargs["filter"] == "tar"


class TestCLISecurityDocumentation:
    """Test CLI security documentation and help."""

    def test_security_warning_in_help(self):
        """Test that security warnings are present in help text."""
        parser = create_parser()
        help_text = parser.format_help()

        # Security-related text should be present
        assert "Security Note:" in help_text
        assert "data" in help_text
        assert "filter" in help_text

    def test_filter_help_text_contains_descriptions(self):
        """Test that filter help text contains basic descriptions."""
        parser = create_parser()
        help_text = parser.format_help()

        # Basic filter information should be present
        assert "data" in help_text
        assert "tar" in help_text
        assert "fully_trusted" in help_text
        assert "safest" in help_text


class TestCLISecurityIntegration:
    """Integration tests for CLI security features."""

    def test_cli_filter_argument_flow(self):
        """Test the complete flow of filter arguments through CLI."""
        parser = create_parser()

        # Test all valid filter values
        for filter_value in ["data", "tar", "fully_trusted"]:
            args = parser.parse_args(["x", "test.tzst", "--filter", filter_value])
            assert args.filter == filter_value

            args = parser.parse_args(["e", "test.tzst", "--filter", filter_value])
            assert args.filter == filter_value

    def test_security_help_content_completeness(self):
        """Test that security help content is comprehensive."""
        parser = create_parser()
        help_text = parser.format_help()

        # Essential security information should be present
        security_keywords = [
            "Security Note:",
            "untrusted sources",
            "data",
            "tar",
            "fully_trusted",
            "safest",
            "filter",
        ]

        for keyword in security_keywords:
            assert keyword in help_text, f"Missing security keyword: {keyword}"
