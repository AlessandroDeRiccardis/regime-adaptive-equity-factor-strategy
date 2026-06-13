"""Simple return and exposure attribution."""

from __future__ import annotations

import pandas as pd


def summarize_legs(backtest: pd.DataFrame) -> pd.Series:
    """Summarize annualized long, short, gross, and cost contributions."""
    return pd.Series(
        {
            "long_leg_return_annualized": backtest["long_leg_return"].mean() * 12,
            "short_leg_return_annualized": backtest["short_leg_return"].mean() * 12,
            "gross_return_annualized": backtest["gross_return"].mean() * 12,
            "transaction_cost_drag_annualized": backtest["transaction_cost"].mean() * 12,
            "average_gross_exposure": backtest["gross_exposure"].mean(),
            "average_net_exposure": backtest["net_exposure"].mean(),
        }
    )
