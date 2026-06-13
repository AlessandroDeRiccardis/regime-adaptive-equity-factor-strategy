"""Momentum signal definitions."""

from __future__ import annotations

import pandas as pd


def add_skip_month_momentum(
    panel: pd.DataFrame,
    price_column: str = "PX_LAST",
    lookback_months: int = 12,
    skip_months: int = 1,
    output_column: str = "factor_momentum",
) -> pd.DataFrame:
    """Add price momentum P[t-skip] / P[t-lookback] - 1."""
    if lookback_months <= skip_months:
        raise ValueError("lookback_months must exceed skip_months.")
    result = panel.sort_values(["ticker", "date"]).copy()
    grouped = result.groupby("ticker", sort=False)[price_column]
    result[output_column] = grouped.shift(skip_months) / grouped.shift(lookback_months) - 1.0
    return result
