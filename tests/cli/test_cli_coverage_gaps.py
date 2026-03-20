"""Targeted tests for remaining uncovered CLI branches."""

import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tzst import create_archive
from tzst.cli import (
    _interactive_conflict_callback,
    _is_extreme_compression_level_in_argv,
    _normalize_archive_path,
    _validate_command_in_argv,
    _validate_compression_level_in_argv,
    _validate_filter_in_argv,
    cmd_extract_flat,
    cmd_extract_full,
    cmd_version,
    main,
)


class TestCliCoverageGaps:
    """Exercise the remaining CLI coverage hotspots."""

    def test_normalize_archive_path_handles_tar_and_custom_extensions(self):
        assert _normalize_archive_path(Path("bundle.tar")) == Path("bundle.tar.zst")
        assert _normalize_archive_path(Path("bundle.backup")) == Path(
            "bundle.backup.tzst"
        )

    @pytest.mark.parametrize(
        ("choice", "expected"),
        [
            ("A", "replace_all"),
            ("S", "skip_all"),
            ("U", "auto_rename_all"),
        ],
    )
    def test_interactive_conflict_callback_covers_remaining_choices(
        self, monkeypatch, temp_dir, choice, expected
    ):
        monkeypatch.setattr("builtins.input", lambda _prompt: choice)

        result = _interactive_conflict_callback(temp_dir / "existing.txt")

        assert result.value == expected

    def test_extract_full_rejects_json_interactive_conflicts(self, temp_dir):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        args = SimpleNamespace(
            archive=str(archive_path),
            output=None,
            files=[],
            streaming=False,
            filter="data",
            conflict_resolution="replace",
            interactive=True,
            json_output=True,
            no_banner=True,
        )

        assert cmd_extract_full(args) == 1

    def test_extract_full_json_success_payload(self, temp_dir, capsys):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)
        output_dir = temp_dir / "extract"

        result = main(
            [
                "--json",
                "x",
                str(archive_path),
                "-o",
                str(output_dir),
                "--conflict-resolution",
                "replace",
            ]
        )

        assert result == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["command"] == "extract"
        assert payload["flatten"] is False

    def test_extract_full_handles_file_not_found_from_backend(
        self, temp_dir, monkeypatch
    ):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        def fail_extract(*args, **kwargs):
            raise FileNotFoundError("backend missing file")

        monkeypatch.setattr("tzst.cli.extract_archive", fail_extract)

        assert main(["x", str(archive_path)]) == 1

    def test_extract_flat_rejects_json_interactive_conflicts(self, temp_dir):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        args = SimpleNamespace(
            archive=str(archive_path),
            output=None,
            files=[],
            streaming=False,
            filter="data",
            conflict_resolution="replace",
            interactive=True,
            json_output=True,
            no_banner=True,
        )

        assert cmd_extract_flat(args) == 1

    def test_extract_flat_json_success_payload(self, temp_dir, capsys):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)
        output_dir = temp_dir / "extract"

        result = main(
            [
                "--json",
                "e",
                str(archive_path),
                "-o",
                str(output_dir),
                "--conflict-resolution",
                "replace",
            ]
        )

        assert result == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["command"] == "extract-flat"
        assert payload["flatten"] is True

    def test_extract_flat_handles_file_not_found_from_backend(
        self, temp_dir, monkeypatch
    ):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        def fail_extract(*args, **kwargs):
            raise FileNotFoundError("backend missing file")

        monkeypatch.setattr("tzst.cli.extract_archive", fail_extract)

        assert main(["e", str(archive_path)]) == 1

    def test_list_handles_file_not_found_from_backend(self, temp_dir, monkeypatch):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        def fail_list(*args, **kwargs):
            raise FileNotFoundError("backend missing file")

        monkeypatch.setattr("tzst.cli.list_archive", fail_list)

        assert main(["l", str(archive_path)]) == 1

    def test_test_command_json_success_and_file_not_found_backend(
        self, temp_dir, capsys, monkeypatch
    ):
        archive_path = temp_dir / "archive.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("content")
        create_archive(archive_path, [source_file], use_temp_file=False)

        result = main(["--json", "t", str(archive_path)])
        assert result == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["command"] == "test"
        assert payload["healthy"] is True

        def fail_test(*args, **kwargs):
            raise FileNotFoundError("backend missing file")

        monkeypatch.setattr("tzst.cli.test_archive", fail_test)
        assert main(["t", str(archive_path)]) == 1

    def test_cmd_version_prints_when_no_banner_requested(self, capsys):
        args = SimpleNamespace(json_output=False, no_banner=True)

        assert cmd_version(args) == 0
        assert capsys.readouterr().out.startswith("tzst ")

    def test_validate_compression_level_in_argv_covers_short_flag_and_index_error(
        self, capsys
    ):
        assert _validate_compression_level_in_argv(["-c", "0"]) is True
        assert "Invalid compression level: 0" in capsys.readouterr().err
        assert _validate_compression_level_in_argv(["-c"]) is False

    def test_validate_filter_in_argv_handles_missing_value(self):
        assert _validate_filter_in_argv(["--filter"]) is False

    def test_validate_command_in_argv_handles_empty_and_invalid_input(self, capsys):
        assert _validate_command_in_argv([]) is False
        assert _validate_command_in_argv(["bogus"]) is True
        assert "Invalid command: 'bogus'" in capsys.readouterr().err

    def test_is_extreme_compression_level_in_argv_covers_all_remaining_paths(self):
        assert _is_extreme_compression_level_in_argv([]) is False
        assert _is_extreme_compression_level_in_argv(["-c", "1000"]) is True
        assert _is_extreme_compression_level_in_argv(["-l", "abc"]) is False
        assert _is_extreme_compression_level_in_argv(["--level"]) is False

    def test_cli_module_main_guard_executes(self, monkeypatch):
        monkeypatch.delitem(sys.modules, "tzst.cli", raising=False)
        monkeypatch.setattr(sys, "argv", ["tzst", "--version"])

        with pytest.raises(SystemExit) as exc_info:
            runpy.run_module("tzst.cli", run_name="__main__")

        assert exc_info.value.code == 0

    def test_package_main_module_executes(self, monkeypatch):
        monkeypatch.delitem(sys.modules, "tzst.__main__", raising=False)
        monkeypatch.setattr(sys, "argv", ["python", "--version"])

        with pytest.raises(SystemExit) as exc_info:
            runpy.run_module("tzst.__main__", run_name="__main__")

        assert exc_info.value.code == 0
