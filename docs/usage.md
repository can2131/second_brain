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

## Logging

All log output uses a compact format:

```
2026-03-21 19:29:10 | I | second_brain.app:main:28 | Hello from second_brain!
```

| Field     | Example                      | Notes                                                                     |
|-----------|------------------------------|---------------------------------------------------------------------------|
| Timestamp | `2026-03-21 19:29:10`        | No milliseconds                                                           |
| Level     | `I`                          | Single letter: **D**ebug, **I**nfo, **W**arning, **E**rror, **C**ritical  |
| Location  | `second_brain.app:main:28`   | module:function:line                                                      |
| Message   | `Hello from second_brain!`   |                                                                           |

Separators are uniform pipes (`|`). The format is defined in `second_brain.app.LOG_FMT`
and used by both the stderr and file handlers.
