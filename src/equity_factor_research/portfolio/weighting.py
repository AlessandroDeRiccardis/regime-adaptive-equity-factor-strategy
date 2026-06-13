"""Inverse-volatility portfolio weighting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_rolling_volatility(
    panel: pd.DataFrame,
    return_column: str = "return_1m",
    lookback_months: int = 12,
    minimum_observations: int = 6,
    output_column: str = "volatility_12m",
) -> pd.DataFrame:
    """Add ticker-level trailing volatility using only current and past returns."""
    result = panel.sort_values(["ticker", "date"]).copy()
    result[output_column] = result.groupby("ticker", sort=False)[return_column].transform(
        lambda x: x.rolling(lookback_months, min_periods=minimum_observations).std()
    )
    return result


def inverse_volatility_weights(volatility: pd.Series) -> pd.Series:
    """Return positive weights normalized to one."""
    inverse = 1.0 / volatility.replace(0.0, np.nan)
    total = inverse.sum()
    return inverse / total if total > 0 else inverse.fillna(0.0)


def construct_decile_weights(
    group: pd.DataFrame,
    short_ratio: float,
    volatility_column: str = "volatility_12m",
    quality_short_column: str | None = None,
) -> pd.DataFrame:
    """Construct +1 long and configurable short gross exposure for one date."""
    result = group.copy()
    result["weight"] = 0.0
    long_mask = result["is_long"] & result[volatility_column].notna()
    short_mask = result["is_short"] & result[volatility_column].notna()
    if quality_short_column:
        short_mask &= result[quality_short_column].lt(0)

    if long_mask.any():
        result.loc[long_mask, "weight"] = inverse_volatility_weights(
            result.loc[long_mask, volatility_column]
        )
    if short_ratio > 0 and short_mask.any():
        result.loc[short_mask, "weight"] = -short_ratio * inverse_volatility_weights(
            result.loc[short_mask, volatility_column]
        )
    return result
