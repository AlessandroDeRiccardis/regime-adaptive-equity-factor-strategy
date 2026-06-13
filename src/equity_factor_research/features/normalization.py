"""Cross-sectional signal normalization."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def zscore_cross_section(
    panel: pd.DataFrame,
    columns: Sequence[str],
    suffix: str = "_z",
) -> pd.DataFrame:
    """Z-score columns independently within each date."""
    result = panel.copy()
    for column in columns:
        grouped = result.groupby("date")[column]
        mean = grouped.transform("mean")
        std = grouped.transform("std")
        result[f"{column}{suffix}"] = (result[column] - mean) / std.where(std > 0)
    return result
