# Usage

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Running

Via the CLI entrypoint:

```bash
uv run second_brain                          # production defaults
uv run --env-file .env second_brain          # dev settings
```

Or as a Python module:

```bash
uv run python -m second_brain
```

## Commands

### `new`

Save a new note and open it in nano:

```bash
uv run --env-file .env second_brain new "My idea"
```

### `list`

Show all notes in the notes directory with their last-modified dates:

```bash
uv run --env-file .env second_brain list
```

Example output:

```
Notes directory: /home/user/second_brain

1. My idea.md                            2026-03-20
2. Shopping list.md                      2026-03-21
```

Notes are sorted oldest-modified first. Only `.md` files are shown.

### `show`

Print the full content of a note by its number (matching `list` order):

```bash
uv run --env-file .env second_brain show 2
```

Example session:

```
$ second_brain list
Notes directory: /home/user/second_brain

1. My idea.md                            2026-03-20
2. Shopping list.md                      2026-03-21
3. Work notes.md                         2026-03-24

$ second_brain show 2
# Shopping list

- Milk
- Eggs
- Bread
```

If the number is out of range, an error is printed and the command exits with code 1.

## Environment Variables

| Variable    | Default    | Description                          |
|-------------|------------|--------------------------------------|
| `LOG_LEVEL` | `INFO`     | Console log level (DEBUG, INFO, …)   |
| `LOG_FILE`  | `app.log`  | Path to the log file                 |

Copy `.env.example` to `.env` for development defaults, then run with `uv run --env-file .env`.

## Log Output

### Console

The console (stderr) uses a compact format:

```
2026-03-21 20:34:28 | INF | second_brain.app:main:29 | Hello from second_brain!
```

Level names are shortened to 3 letters: TRC, DBG, INF, SUC, WRN, ERR, CRT.

### File

The file handler (`LOG_FILE`, default `app.log`) uses loguru's default verbose
format with millisecond timestamps, full level names, and automatic rotation.
