"""Turnover and linear transaction-cost model."""

from __future__ import annotations

import pandas as pd


def calculate_turnover(weights: pd.DataFrame) -> pd.Series:
    """Calculate one-way turnover, including initial formation from zero holdings."""
    wide = weights.pivot(index="date", columns="ticker", values="weight").fillna(0.0).sort_index()
    changes = wide.diff()
    changes.iloc[0] = wide.iloc[0]
    return changes.abs().sum(axis=1).div(2.0).rename("turnover")


def transaction_cost(turnover: pd.Series, cost_bps: float) -> pd.Series:
    """Apply a linear one-way cost in basis points."""
    return turnover * cost_bps / 10_000.0
