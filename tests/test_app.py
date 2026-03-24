import re
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from second_brain.app import console_format, main


class _Level:
    """Minimal stand-in for loguru's record level object."""

    def __init__(self, name):
        self.name = name


# -- Unit tests for console_format ------------------------------------------


def test_console_format_returns_compact_string():
    record = {"level": _Level("INFO")}
    result = console_format(record)

    assert "INF" in result
    assert " | " in result
    assert result.endswith("\n{exception}")
    assert "INFO" not in result


@pytest.mark.parametrize(
    "level_name,expected_short",
    [
        ("TRACE", "TRC"),
        ("DEBUG", "DBG"),
        ("INFO", "INF"),
        ("SUCCESS", "SUC"),
        ("WARNING", "WRN"),
        ("ERROR", "ERR"),
        ("CRITICAL", "CRT"),
    ],
)
def test_console_format_all_levels(level_name, expected_short):
    record = {"level": _Level(level_name)}
    result = console_format(record)
    assert expected_short in result


def test_console_format_unknown_level_falls_back_to_slice():
    record = {"level": _Level("CUSTOM_LEVEL")}
    result = console_format(record)
    assert "CUS" in result


# -- CLI integration tests ---------------------------------------------------


def test_new_command_saves_note(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    runner = CliRunner()
    with patch("second_brain.app.subprocess.run"):
        result = runner.invoke(main, ["new", "My idea"], catch_exceptions=False)
    assert result.exit_code == 0
    assert (tmp_path / "My idea.md").exists()
    assert (tmp_path / "My idea.md").read_text() == "# My idea\n"


def test_new_command_respects_notes_dir_env(tmp_path, monkeypatch):
    custom_dir = tmp_path / "custom_notes"
    monkeypatch.setenv("NOTES_DIR", str(custom_dir))
    runner = CliRunner()
    with patch("second_brain.app.subprocess.run"):
        runner.invoke(main, ["new", "test"], catch_exceptions=False)
    assert (custom_dir / "test.md").exists()


def test_new_command_opens_editor(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    runner = CliRunner()
    with patch("second_brain.app.subprocess.run") as mock_run:
        runner.invoke(main, ["new", "My idea"], catch_exceptions=False)
    mock_run.assert_called_once_with(["nano", str(tmp_path / "My idea.md")])


def test_list_command_shows_directory_and_notes(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "alpha.md").write_text("# alpha")
    (tmp_path / "beta.md").write_text("# beta")
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    assert result.exit_code == 0
    assert f"Notes directory: {tmp_path}" in result.output
    assert "alpha.md" in result.output
    assert "beta.md" in result.output


def test_list_command_shows_numbered_entries(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "note.md").write_text("# note")
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    assert "1." in result.output


def test_list_command_shows_modified_date(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "note.md").write_text("# note")
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    import re
    assert re.search(r"\d{4}-\d{2}-\d{2}", result.output)


def test_list_command_skips_non_markdown_files(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "note.md").write_text("# note")
    (tmp_path / "other.txt").write_text("ignore me")
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    assert "other.txt" not in result.output


def test_list_command_empty_directory(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "No notes found." in result.output


def test_list_command_missing_directory(tmp_path, monkeypatch):
    missing = tmp_path / "does_not_exist"
    monkeypatch.setenv("NOTES_DIR", str(missing))
    runner = CliRunner()
    result = runner.invoke(main, ["list"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "No notes found." in result.output


def test_show_command_prints_note_content(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "first.md").write_text("# First note\nContent A")
    (tmp_path / "second.md").write_text("# Second note\nContent B")
    # ensure second is newer
    import time
    time.sleep(0.01)
    (tmp_path / "second.md").touch()
    runner = CliRunner()
    result = runner.invoke(main, ["show", "2"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "# Second note" in result.output
    assert "Content B" in result.output


def test_show_command_numbering_matches_list(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    older = tmp_path / "older.md"
    newer = tmp_path / "newer.md"
    older.write_text("# Older")
    import time
    time.sleep(0.01)
    newer.write_text("# Newer")
    runner = CliRunner()
    show1 = runner.invoke(main, ["show", "1"], catch_exceptions=False)
    show2 = runner.invoke(main, ["show", "2"], catch_exceptions=False)
    assert "# Older" in show1.output
    assert "# Newer" in show2.output


def test_show_command_out_of_range(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    (tmp_path / "note.md").write_text("# note")
    runner = CliRunner()
    result = runner.invoke(main, ["show", "99"])
    assert result.exit_code == 1
    assert "Error: note 99 not found." in result.output
    assert "second_brain list" in result.output


def test_show_command_empty_directory(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTES_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["show", "1"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "No notes found." in result.output


def test_show_command_missing_directory(tmp_path, monkeypatch):
    missing = tmp_path / "does_not_exist"
    monkeypatch.setenv("NOTES_DIR", str(missing))
    runner = CliRunner()
    result = runner.invoke(main, ["show", "1"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "No notes found." in result.output


def test_file_handler_uses_default_format(tmp_path, monkeypatch):
    log_file = tmp_path / "verify.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    monkeypatch.setenv("NOTES_DIR", str(tmp_path / "notes"))
    runner = CliRunner()
    with patch("second_brain.app.subprocess.run"):
        runner.invoke(main, ["new", "test note"], catch_exceptions=False)
    content = log_file.read_text()
    assert "SUCCESS" in content
    assert "Note saved:" in content
