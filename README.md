# second-brain

A Python application.

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Usage

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

`.env.example` is the template — copy it to `.env` for development:

```bash
cp .env.example .env
```

Then run with `uv run --env-file .env` to load the dev environment.

| Variable    | Default    | Description                          |
|-------------|------------|--------------------------------------|
| `LOG_LEVEL` | `INFO`     | Console log level (DEBUG, INFO, …); set to DEBUG in `.env` for verbose output |
| `LOG_FILE`  | `app.log`  | Path to the log file                 |

## Logging

Log output uses a compact format with no milliseconds and single-letter levels:

```
2026-03-21 19:29:10 | I | second_brain.app:main:28 | Hello from second_brain!
```

See [docs/usage.md](docs/usage.md#logging) for the full format specification.

## Testing

Run tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov
```

## Documentation

Preview docs locally:

```bash
uv run python scripts/serve_docs.py
```

Build static docs:

```bash
uv run mkdocs build
```
