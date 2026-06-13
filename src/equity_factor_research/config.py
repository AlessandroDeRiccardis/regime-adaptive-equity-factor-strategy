"""Configuration loading and project path helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def project_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load YAML configuration and resolve repository-relative paths."""
    config_path = Path(path) if path else project_root() / "configs" / "default.yaml"
    with config_path.open(encoding="utf-8") as stream:
        config: dict[str, Any] = yaml.safe_load(stream)

    root = project_root()
    raw_override = os.getenv("EQUITY_FACTOR_RAW_DATA")
    if raw_override:
        config["data"]["raw_path"] = raw_override

    for key in ("raw_path", "sample_path", "processed_path", "backtest_path"):
        value = Path(config["data"][key]).expanduser()
        config["data"][key] = value if value.is_absolute() else root / value

    for key in ("figures_dir", "tables_dir"):
        value = Path(config["output"][key]).expanduser()
        config["output"][key] = value if value.is_absolute() else root / value
    return config
