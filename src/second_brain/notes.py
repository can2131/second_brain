from pathlib import Path


def _safe_filename(title: str) -> str:
    return title.strip().replace("/", "-").replace("\x00", "")


def save_note(text: str, notes_dir: Path) -> Path:
    """Save a note as a titled markdown file.

    Args:
        text: The note title and initial content.
        notes_dir: Directory where the note file will be created.

    Returns:
        The path to the saved note file.
    """
    notes_dir.mkdir(parents=True, exist_ok=True)
    stem = _safe_filename(text)
    path = notes_dir / f"{stem}.md"
    counter = 2
    while path.exists():
        path = notes_dir / f"{stem} ({counter}).md"
        counter += 1
    path.write_text(f"# {text}\n")
    return path
