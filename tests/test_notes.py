import pytest

from second_brain.notes import save_note


def test_save_note_creates_file(tmp_path):
    path = save_note("My idea", tmp_path)
    assert path.exists()


def test_save_note_content(tmp_path):
    path = save_note("My idea", tmp_path)
    assert path.read_text() == "# My idea\n"


def test_save_note_filename_uses_title(tmp_path):
    path = save_note("My brilliant idea", tmp_path)
    assert path.name == "My brilliant idea.md"


def test_save_note_handles_duplicate_title(tmp_path):
    path1 = save_note("My idea", tmp_path)
    path2 = save_note("My idea", tmp_path)
    assert path1.name == "My idea.md"
    assert path2.name == "My idea (2).md"


def test_save_note_creates_dir_if_missing(tmp_path):
    notes_dir = tmp_path / "notes" / "sub"
    save_note("test", notes_dir)
    assert notes_dir.exists()


def test_save_note_sanitizes_slashes(tmp_path):
    path = save_note("ideas/thoughts", tmp_path)
    assert path.name == "ideas-thoughts.md"
