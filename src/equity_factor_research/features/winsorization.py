"""Cross-sectional winsorization."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def winsorize_cross_section(
    panel: pd.DataFrame,
    columns: Sequence[str],
    lower: float = 0.01,
    upper: float = 0.99,
) -> pd.DataFrame:
    """Clip each factor to date-specific quantile bounds."""
    result = panel.copy()
    for column in columns:
        lo = result.groupby("date")[column].transform(lambda x: x.quantile(lower))
        hi = result.groupby("date")[column].transform(lambda x: x.quantile(upper))
        result[f"{column}_winsorized"] = result[column].clip(lower=lo, upper=hi)
    return result
