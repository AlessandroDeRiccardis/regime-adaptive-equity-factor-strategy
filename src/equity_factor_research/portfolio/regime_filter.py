"""Lagged benchmark trend regime and dynamic hedge sizing."""

from __future__ import annotations

import pandas as pd


def lagged_sma_regime(
    benchmark_returns: pd.Series,
    sma_window_months: int = 10,
    minimum_observations: int = 3,
) -> pd.DataFrame:
    """Classify date t from benchmark information available through t-1."""
    returns = benchmark_returns.sort_index().fillna(0.0)
    cumulative = (1.0 + returns).cumprod()
    sma = cumulative.rolling(sma_window_months, min_periods=minimum_observations).mean()
    return pd.DataFrame(
        {
            "benchmark_cumulative": cumulative,
            "benchmark_sma": sma,
            "bull_regime": cumulative.shift(1).ge(sma.shift(1)).fillna(False),
        }
    )


def dynamic_short_ratio(
    bull_regime: pd.Series,
    bear_short_ratio: float = 0.40,
) -> pd.Series:
    """Return zero short exposure in bull regimes and a partial hedge in bears."""
    return bull_regime.map({True: 0.0, False: bear_short_ratio}).astype(float)
