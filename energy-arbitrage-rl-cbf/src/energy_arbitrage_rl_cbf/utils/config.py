"""Configuration loading helpers."""

from pathlib import Path


def read_config_text(path: Path) -> str:
    """Read a config file without choosing a parser yet."""

    return path.read_text(encoding="utf-8")
