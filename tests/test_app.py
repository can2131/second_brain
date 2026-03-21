"""Tests for second_brain.app logging configuration."""

import re

from second_brain.app import LOG_FMT, configure_logging, main

# Regex for the tight log format (non-TTY, no ANSI codes):
#   2026-03-21 19:29:10 | I | second_brain.app:main:28 | Hello from second_brain!
LOG_LINE_RE = re.compile(
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| [DIWECS] \| [\w.]+:\w+:\d+ \| .+"
)


class TestLogFmtConstant:
    """Tests for the module-level LOG_FMT constant."""

    def test_log_fmt_exists_and_is_string(self):
        assert isinstance(LOG_FMT, str)

    def test_log_fmt_contains_no_milliseconds(self):
        assert "HH:mm:ss}" in LOG_FMT or "HH:mm:ss}<" in LOG_FMT
        assert ".SSS" not in LOG_FMT

    def test_log_fmt_uses_single_letter_level(self):
        assert "{level.name:.1s}" in LOG_FMT

    def test_log_fmt_uses_pipe_separators(self):
        assert " - " not in LOG_FMT
        assert " | " in LOG_FMT


class TestConfigureLogging:
    """Tests for configure_logging output format."""

    def test_stderr_format_matches_spec(self, capfd):
        from loguru import logger

        configure_logging()
        logger.info("format check")
        captured = capfd.readouterr()
        assert LOG_LINE_RE.search(captured.err), (
            f"stderr output did not match expected format.\nGot: {captured.err!r}"
        )

    def test_stderr_no_milliseconds(self, capfd):
        from loguru import logger

        configure_logging()
        logger.info("no ms check")
        captured = capfd.readouterr()
        assert not re.search(r"\d{2}:\d{2}:\d{2}\.\d{3}", captured.err), (
            f"Milliseconds found in output: {captured.err!r}"
        )

    def test_stderr_single_letter_level(self, capfd):
        from loguru import logger

        configure_logging()
        logger.info("level check")
        captured = capfd.readouterr()
        assert "| I |" in captured.err
        assert "INFO" not in captured.err

    def test_file_format_matches_spec(self, tmp_path, monkeypatch, capfd):
        log_file = tmp_path / "fmt_test.log"
        monkeypatch.setenv("LOG_FILE", str(log_file))

        from loguru import logger

        configure_logging()
        logger.info("file format check")
        _ = capfd.readouterr()

        content = log_file.read_text()
        assert LOG_LINE_RE.search(content), (
            f"File output did not match expected format.\nGot: {content!r}"
        )

    def test_multiple_levels_single_letter(self, capfd, monkeypatch):
        from loguru import logger

        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        configure_logging()

        logger.debug("d-msg")
        logger.info("i-msg")
        logger.warning("w-msg")
        logger.error("e-msg")

        captured = capfd.readouterr()
        assert "| D |" in captured.err
        assert "| I |" in captured.err
        assert "| W |" in captured.err
        assert "| E |" in captured.err


class TestMain:
    """Tests for the main() entrypoint."""

    def test_main_logs_greeting(self, capfd):
        main()
        captured = capfd.readouterr()
        assert "Hello from second_brain!" in captured.err

    def test_main_greeting_matches_format(self, capfd):
        main()
        captured = capfd.readouterr()
        assert LOG_LINE_RE.search(captured.err), (
            f"main() output did not match expected format.\nGot: {captured.err!r}"
        )
