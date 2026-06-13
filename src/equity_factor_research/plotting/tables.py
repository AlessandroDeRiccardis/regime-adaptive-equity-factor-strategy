"""Table output helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pandas as pd


def write_metrics(metrics: Mapping[str, float], path: str | Path) -> None:
    """Write a one-row metric table."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([metrics]).to_csv(output, index=False)
