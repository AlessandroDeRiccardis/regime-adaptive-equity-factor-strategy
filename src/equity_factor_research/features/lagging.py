"""No-look-ahead lagging helpers."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def lag_and_fill_fundamentals(
    panel: pd.DataFrame,
    columns: Sequence[str],
    lag_months: int = 2,
    fill_limit_months: int = 10,
) -> pd.DataFrame:
    """Lag and forward-fill fundamentals strictly within each ticker.

    The grouped forward-fill is deliberate. A plain ``ffill`` after a grouped
    shift can leak the last value of one ticker into the first rows of another.
    """
    result = panel.sort_values(["ticker", "date"]).copy()
    available = [column for column in columns if column in result.columns]
    shifted = result.groupby("ticker", sort=False)[available].shift(lag_months)
    result[available] = shifted.groupby(result["ticker"], sort=False).ffill(limit=fill_limit_months)
    return result
