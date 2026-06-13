"""Cross-sectional portfolio selection."""

from __future__ import annotations

import pandas as pd


def add_decile_selection(
    panel: pd.DataFrame,
    score_column: str = "composite_score",
    top_quantile: float = 0.90,
    bottom_quantile: float = 0.10,
) -> pd.DataFrame:
    """Mark top and bottom score tails within each date."""
    result = panel.copy()
    top = result.groupby("date")[score_column].transform(lambda x: x.quantile(top_quantile))
    bottom = result.groupby("date")[score_column].transform(lambda x: x.quantile(bottom_quantile))
    result["is_long"] = result[score_column].ge(top)
    result["is_short"] = result[score_column].le(bottom)
    return result
