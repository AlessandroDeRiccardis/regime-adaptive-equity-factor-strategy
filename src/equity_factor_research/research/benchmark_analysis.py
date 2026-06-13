"""Transparent benchmark definitions."""

from __future__ import annotations

import pandas as pd


def monthly_rebalanced_equal_weight_benchmark(
    panel: pd.DataFrame,
    return_column: str = "return_1m",
) -> pd.Series:
    """Average the available-universe stock returns each month."""
    return panel.groupby("date")[return_column].mean().rename("benchmark_return")


def static_equal_weight_buy_and_hold_benchmark(
    panel: pd.DataFrame,
    start_date: str | pd.Timestamp | None = None,
    return_column: str = "return_1m",
) -> pd.Series:
    """Track a fixed equal-weight basket selected at the first eligible date."""
    eligible = panel.dropna(subset=[return_column]).copy()
    first_date = pd.Timestamp(start_date) if start_date else eligible["date"].min()
    tickers = eligible.loc[eligible["date"].eq(first_date), "ticker"].unique()
    basket = eligible[eligible["ticker"].isin(tickers)]
    wealth = (
        basket.pivot(index="date", columns="ticker", values=return_column)
        .fillna(0.0)
        .add(1.0)
        .cumprod()
    )
    nav = wealth.mean(axis=1)
    return nav.pct_change(fill_method=None).rename("benchmark_return").dropna()
