"""Targeted tests for remaining uncovered core branches."""

import os
import tarfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import tzst.core as core_module
from tzst.core import (
    ConflictResolution,
    ConflictResolutionState,
    TzstArchive,
    _get_unique_filename,
    _move_file_cross_platform,
    create_archive,
    extract_archive,
)
from tzst.exceptions import TzstArchiveError, TzstDecompressionError


def _make_read_archive() -> TzstArchive:
    archive = TzstArchive("dummy.tzst", "r")
    archive._tarfile = Mock()
    archive.mode = "r"
    return archive


def _make_write_archive() -> TzstArchive:
    archive = TzstArchive("dummy.tzst", "w")
    archive._tarfile = Mock()
    archive.mode = "w"
    return archive


class TestCoreCoverageGaps:
    """Exercise the remaining core coverage hotspots."""

    def test_conflict_resolution_state_apply_to_all(self):
        state = ConflictResolutionState(ConflictResolution.AUTO_RENAME_ALL)
        assert state.apply_to_all is True

        state = ConflictResolutionState(ConflictResolution.REPLACE)
        assert state.apply_to_all is False

    def test_get_unique_filename_returns_original_for_missing_path(self, temp_dir):
        missing_path = temp_dir / "missing.txt"
        assert _get_unique_filename(missing_path) == missing_path

    def test_move_file_cross_platform_falls_back_to_copy_and_delete(
        self, temp_dir, monkeypatch
    ):
        src = temp_dir / "source.txt"
        dst = temp_dir / "target.txt"
        src.write_text("cross-drive content")

        def fail_rename(self, target):
            raise OSError("cross-device link")

        monkeypatch.setattr(Path, "rename", fail_rename)

        _move_file_cross_platform(src, dst)

        assert dst.read_text() == "cross-drive content"
        assert not src.exists()

    def test_move_file_cross_platform_reraises_original_rename_error(
        self, temp_dir, monkeypatch
    ):
        src = temp_dir / "source.txt"
        dst = temp_dir / "target.txt"
        src.write_text("cross-drive content")

        def fail_rename(self, target):
            raise OSError("rename failed")

        def fail_copy(*args, **kwargs):
            raise RuntimeError("copy failed")

        monkeypatch.setattr(Path, "rename", fail_rename)
        monkeypatch.setattr("shutil.copy2", fail_copy)

        with pytest.raises(OSError, match="rename failed"):
            _move_file_cross_platform(src, dst)

    def test_exit_suppresses_close_errors(self, monkeypatch):
        archive = TzstArchive("dummy.tzst", "w")
        monkeypatch.setattr(archive, "close", Mock(side_effect=RuntimeError("boom")))

        archive.__exit__(None, None, None)

    def test_open_wraps_zstd_failures(self, temp_dir, monkeypatch):
        archive_path = temp_dir / "broken.tzst"
        archive_path.write_bytes(b"not-a-valid-archive")

        class BrokenDecompressor:
            def stream_reader(self, fileobj):
                raise RuntimeError("zstd decoder exploded")

        monkeypatch.setattr(core_module.zstd, "ZstdDecompressor", BrokenDecompressor)

        with pytest.raises(TzstDecompressionError, match="zstd decoder exploded"):
            TzstArchive(archive_path, "r").open()

    def test_open_wraps_append_mode_when_mode_changes_after_init(self):
        archive = TzstArchive("dummy.tzst", "w")
        archive.mode = "a"

        with pytest.raises(TzstArchiveError, match="Append mode is not currently supported"):
            archive.open()

    def test_open_wraps_invalid_mode_when_mode_changes_after_init(self):
        archive = TzstArchive("dummy.tzst", "w")
        archive.mode = "invalid"

        with pytest.raises(TzstArchiveError, match="Invalid mode: invalid"):
            archive.open()

    def test_add_requires_open_archive(self, temp_dir):
        archive = TzstArchive(temp_dir / "archive.tzst", "w")

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.add(temp_dir / "file.txt")

    def test_add_requires_write_mode(self, temp_dir):
        archive = _make_write_archive()
        archive.mode = "r"
        file_path = temp_dir / "file.txt"
        file_path.write_text("content")

        with pytest.raises(RuntimeError, match="Archive not open for writing"):
            archive.add(file_path)

    def test_add_raises_file_not_found_for_missing_input(self, temp_dir):
        archive = _make_write_archive()

        with pytest.raises(FileNotFoundError, match="File not found"):
            archive.add(temp_dir / "missing.txt")

    def test_add_wraps_permission_errors(self, temp_dir):
        archive = _make_write_archive()
        archive._tarfile.add.side_effect = PermissionError("denied")
        file_path = temp_dir / "file.txt"
        file_path.write_text("content")

        with pytest.raises(TzstArchiveError, match="Failed to add"):
            archive.add(file_path)

    def test_extract_validates_open_state_and_mode(self, temp_dir):
        closed_archive = TzstArchive(temp_dir / "archive.tzst", "r")
        with pytest.raises(RuntimeError, match="Archive not open"):
            closed_archive.extract()

        wrong_mode_archive = _make_write_archive()
        with pytest.raises(RuntimeError, match="Archive not open for reading"):
            wrong_mode_archive.extract()

    def test_extract_rejects_specific_members_in_streaming_mode(self):
        archive = _make_read_archive()
        archive.streaming = True

        with pytest.raises(RuntimeError, match="specific members is not supported"):
            archive.extract("file.txt")

    def test_extract_passes_member_specific_kwargs(self, temp_dir):
        archive = _make_read_archive()
        output_dir = temp_dir / "extract"

        archive.extract(
            "nested/file.txt",
            output_dir,
            set_attrs=False,
            numeric_owner=True,
            filter="tar",
        )

        archive._tarfile.extract.assert_called_once_with(
            "nested/file.txt",
            path=output_dir,
            set_attrs=False,
            numeric_owner=True,
            filter="tar",
        )

    def test_extract_wraps_streaming_structure_errors(self, temp_dir):
        archive = _make_read_archive()
        archive.streaming = True
        archive._tarfile.extractall.side_effect = tarfile.StreamError("stream seeking failed")

        with pytest.raises(RuntimeError, match="Extraction failed in streaming mode"):
            archive.extract(path=temp_dir / "extract")

    def test_extract_reraises_non_streaming_errors(self, temp_dir):
        archive = _make_read_archive()
        archive._tarfile.extractall.side_effect = OSError("disk full")

        with pytest.raises(OSError, match="disk full"):
            archive.extract(path=temp_dir / "extract")

    def test_extractall_validates_open_state_and_members_behavior(self, temp_dir):
        closed_archive = TzstArchive(temp_dir / "archive.tzst", "r")
        with pytest.raises(RuntimeError, match="Archive not open"):
            closed_archive.extractall()

        wrong_mode_archive = _make_write_archive()
        with pytest.raises(RuntimeError, match="Archive not open for reading"):
            wrong_mode_archive.extractall()

        streaming_archive = _make_read_archive()
        streaming_archive.streaming = True
        with pytest.raises(RuntimeError, match="specific members is not supported"):
            streaming_archive.extractall(members=[Mock()])

    def test_extractall_passes_members_and_reraises_other_errors(self, temp_dir):
        archive = _make_read_archive()
        members = [SimpleNamespace(name="file.txt")]
        output_dir = temp_dir / "extract"

        archive.extractall(output_dir, members=members, numeric_owner=True, filter="tar")

        archive._tarfile.extractall.assert_called_once_with(
            path=output_dir,
            numeric_owner=True,
            filter="tar",
            members=members,
        )

        archive = _make_read_archive()
        archive._tarfile.extractall.side_effect = OSError("permission denied")
        with pytest.raises(OSError, match="permission denied"):
            archive.extractall(output_dir)

    def test_getnames_list_and_test_runtime_paths(self):
        archive = _make_read_archive()
        archive._tarfile.getnames.return_value = ["a.txt"]
        assert archive.getnames() == ["a.txt"]

        closed_archive = TzstArchive("dummy.tzst", "r")
        with pytest.raises(RuntimeError, match="Archive not open"):
            closed_archive.list()

        wrong_mode_archive = _make_write_archive()
        with pytest.raises(RuntimeError, match="Archive not open for reading"):
            wrong_mode_archive.list()

        failing_archive = _make_read_archive()
        failing_archive.getmembers = Mock(side_effect=RuntimeError("boom"))
        assert failing_archive.test() is False

    def test_create_archive_supports_tar_extension(self, temp_dir):
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive me")

        create_archive(temp_dir / "bundle.tar", [source_file], use_temp_file=False)

        assert (temp_dir / "bundle.tar.zst").exists()

    def test_create_archive_ignores_unlink_cleanup_failures(self, temp_dir, monkeypatch):
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive me")
        archive_path = temp_dir / "broken.tzst"
        temp_path = temp_dir / ".broken.tzst.tmp"

        def fake_mkstemp(*args, **kwargs):
            fd = os.open(temp_path, os.O_CREAT | os.O_RDWR)
            return fd, str(temp_path)

        def fail_unlink(self):
            raise OSError("locked")

        monkeypatch.setattr(core_module.tempfile, "mkstemp", fake_mkstemp)
        monkeypatch.setattr(core_module, "_create_archive_impl", Mock(side_effect=RuntimeError("boom")))
        monkeypatch.setattr(Path, "unlink", fail_unlink)

        with pytest.raises(RuntimeError, match="boom"):
            create_archive(archive_path, [source_file])

        assert temp_path.exists()

    def test_extract_archive_handles_flatten_members_and_invalid_resolution(
        self, temp_dir
    ):
        file_path = temp_dir / "source.txt"
        file_path.write_text("content")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [file_path], use_temp_file=False)

        output_dir = temp_dir / "extract"
        extract_archive(
            archive_path,
            output_dir,
            members=["source.txt"],
            flatten=True,
            conflict_resolution="definitely-invalid",
        )

        assert (output_dir / "source.txt").read_text() == "content"

    def test_extract_archive_flatten_respects_initial_exit_resolution(self, temp_dir):
        file_path = temp_dir / "source.txt"
        file_path.write_text("content")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [file_path], use_temp_file=False)

        output_dir = temp_dir / "extract"
        extract_archive(
            archive_path,
            output_dir,
            flatten=True,
            conflict_resolution=ConflictResolution.EXIT,
        )

        assert not (output_dir / "source.txt").exists()

    def test_extract_archive_flatten_conflict_skip_exit_and_auto_rename(
        self, temp_dir
    ):
        first = temp_dir / "first.txt"
        second = temp_dir / "second.txt"
        first.write_text("first")
        second.write_text("second")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [first, second], use_temp_file=False)

        skip_output = temp_dir / "skip"
        skip_output.mkdir()
        (skip_output / "first.txt").write_text("existing")
        extract_archive(
            archive_path,
            skip_output,
            members=["first.txt"],
            flatten=True,
            conflict_resolution=ConflictResolution.SKIP,
        )
        assert (skip_output / "first.txt").read_text() == "existing"

        rename_output = temp_dir / "rename"
        rename_output.mkdir()
        (rename_output / "first.txt").write_text("existing")
        extract_archive(
            archive_path,
            rename_output,
            members=["first.txt"],
            flatten=True,
            conflict_resolution=ConflictResolution.AUTO_RENAME,
        )
        assert (rename_output / "first.txt").read_text() == "existing"
        assert (rename_output / "first_1.txt").read_text() == "first"

        exit_output = temp_dir / "exit"
        exit_output.mkdir()
        (exit_output / "first.txt").write_text("existing")
        extract_archive(
            archive_path,
            exit_output,
            members=["first.txt", "second.txt"],
            flatten=True,
            conflict_resolution=ConflictResolution.ASK,
            interactive_callback=lambda _path: ConflictResolution.EXIT,
        )
        assert (exit_output / "first.txt").read_text() == "existing"
        assert not (exit_output / "second.txt").exists()

    def test_extract_archive_members_support_auto_rename_and_plain_extract(
        self, temp_dir
    ):
        source_root = temp_dir / "source"
        nested_dir = source_root / "nested"
        nested_dir.mkdir(parents=True)
        conflict_file = nested_dir / "conflict.txt"
        plain_file = source_root / "plain.txt"
        conflict_file.write_text("conflict-content")
        plain_file.write_text("plain-content")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [conflict_file, plain_file], use_temp_file=False)

        output_dir = temp_dir / "extract"
        output_dir.mkdir()
        target_conflict = output_dir / "nested" / "conflict.txt"
        target_conflict.parent.mkdir(parents=True, exist_ok=True)
        target_conflict.write_text("existing")

        extract_archive(
            archive_path,
            output_dir,
            members=["nested/conflict.txt", "plain.txt"],
            flatten=False,
            conflict_resolution=ConflictResolution.AUTO_RENAME,
        )

        assert target_conflict.read_text() == "existing"
        assert (output_dir / "nested" / "conflict_1.txt").read_text() == "conflict-content"
        assert (output_dir / "plain.txt").read_text() == "plain-content"

    def test_extract_archive_members_honor_initial_exit_state(self, temp_dir):
        file_path = temp_dir / "source.txt"
        file_path.write_text("content")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [file_path], use_temp_file=False)

        output_dir = temp_dir / "extract"
        extract_archive(
            archive_path,
            output_dir,
            members=["source.txt"],
            conflict_resolution=ConflictResolution.EXIT,
        )

        assert not (output_dir / "source.txt").exists()

    def test_extract_archive_extractall_breaks_on_exit_conflict(self, temp_dir):
        file_path = temp_dir / "source.txt"
        file_path.write_text("content")
        archive_path = temp_dir / "archive.tzst"
        create_archive(archive_path, [file_path], use_temp_file=False)

        output_dir = temp_dir / "extract"
        output_dir.mkdir()
        (output_dir / "source.txt").write_text("existing")

        extract_archive(
            archive_path,
            output_dir,
            conflict_resolution=ConflictResolution.ASK,
            interactive_callback=lambda _path: ConflictResolution.EXIT,
        )

        assert (output_dir / "source.txt").read_text() == "existing"
