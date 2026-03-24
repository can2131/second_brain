import os
import subprocess
import sys
from pathlib import Path

import click
from loguru import logger

LEVEL_SHORT = {
    "TRACE": "TRC",
    "DEBUG": "DBG",
    "INFO": "INF",
    "SUCCESS": "SUC",
    "WARNING": "WRN",
    "ERROR": "ERR",
    "CRITICAL": "CRT",
}


def console_format(record):
    """Return a compact log format string for console output.

    Loguru calls this with each log record and evaluates the returned
    template. Callable formats do not auto-append ``\\n{exception}``,
    so we include it explicitly.
    """
    short = LEVEL_SHORT.get(record["level"].name, record["level"].name[:3])
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>" + short + "</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>\n{exception}"
    )


def configure_logging():
    """Configure loguru for console and file logging.

    Removes the default handler and sets up:
    - stderr handler at LOG_LEVEL (default: INFO) with compact format
    - File handler at DEBUG level writing to LOG_FILE (default: app.log)
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log_file = os.environ.get("LOG_FILE", "app.log")
    logger.remove()
    logger.add(sys.stderr, level=log_level, format=console_format)
    logger.add(log_file, level="DEBUG", rotation="50 KB", retention=1)


@click.group()
def main():
    """Second brain — capture thoughts from the command line."""
    configure_logging()


@main.command()
@click.argument("text")
def new(text):
    """Save TEXT as a new note."""
    from second_brain.notes import save_note

    notes_dir = Path(os.environ.get("NOTES_DIR", "~/second_brain")).expanduser()
    path = save_note(text, notes_dir)
    logger.success(f"Note saved: {path}")
    subprocess.run(["nano", str(path)])


@main.command(name="list")
def list_notes():
    """List all notes with their last-modified dates."""
    from datetime import datetime

    notes_dir = Path(os.environ.get("NOTES_DIR", "~/second_brain")).expanduser()
    logger.debug(f"Listing notes in: {notes_dir}")
    click.echo(f"Notes directory: {notes_dir}")
    click.echo()

    if not notes_dir.exists():
        click.echo("No notes found.")
        return

    notes = sorted(
        (p for p in notes_dir.iterdir() if p.suffix == ".md"),
        key=lambda p: p.stat().st_mtime,
    )

    if not notes:
        click.echo("No notes found.")
        return

    for i, note in enumerate(notes, start=1):
        date = datetime.fromtimestamp(note.stat().st_mtime).strftime("%Y-%m-%d")
        click.echo(f"{i}. {note.name:<40} {date}")


@main.command()
@click.argument("number", type=int)
def show(number: int) -> None:
    """Print the content of note NUMBER to stdout."""
    notes_dir = Path(os.environ.get("NOTES_DIR", "~/second_brain")).expanduser()

    if not notes_dir.exists():
        click.echo("No notes found.")
        return

    notes = sorted(
        (p for p in notes_dir.iterdir() if p.suffix == ".md"),
        key=lambda p: p.stat().st_mtime,
    )

    if not notes:
        click.echo("No notes found.")
        return

    if number < 1 or number > len(notes):
        click.echo(f"Error: note {number} not found. Run 'second_brain list' to see available notes.")
        sys.exit(1)

    path = notes[number - 1]
    logger.debug(f"Showing note: {path}")
    click.echo(path.read_text())
