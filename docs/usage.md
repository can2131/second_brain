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
