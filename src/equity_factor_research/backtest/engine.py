"""Monthly cross-sectional backtest engine."""

from __future__ import annotations

import pandas as pd

from equity_factor_research.backtest.accounting import drawdown_from_nav, nav_from_returns
from equity_factor_research.portfolio.constraints import exposure_summary
from equity_factor_research.portfolio.transaction_costs import (
    calculate_turnover,
    transaction_cost,
)


def run_backtest(
    weighted_panel: pd.DataFrame,
    return_column: str = "return_1m",
    transaction_cost_bps: float = 3.0,
) -> pd.DataFrame:
    """Apply weights formed at t to stock returns realized at t+1."""
    required = {"date", "ticker", "weight", return_column}
    missing = sorted(required - set(weighted_panel.columns))
    if missing:
        raise ValueError(f"Backtest input missing columns: {missing}")

    panel = weighted_panel.sort_values(["ticker", "date"]).copy()
    panel["applied_weight"] = panel.groupby("ticker", sort=False)["weight"].shift(1)
    panel["contribution"] = panel["applied_weight"] * panel[return_column]
    panel["long_contribution"] = panel["applied_weight"].clip(lower=0) * panel[return_column]
    panel["short_contribution"] = panel["applied_weight"].clip(upper=0) * panel[return_column]

    returns = panel.groupby("date")[
        ["contribution", "long_contribution", "short_contribution"]
    ].sum(min_count=1)
    returns.columns = ["gross_return", "long_leg_return", "short_leg_return"]

    formation_turnover = calculate_turnover(panel[["date", "ticker", "weight"]])
    returns["turnover"] = formation_turnover.shift(1).reindex(returns.index).fillna(0.0)
    returns["transaction_cost"] = transaction_cost(returns["turnover"], transaction_cost_bps)
    returns["net_return"] = returns["gross_return"] - returns["transaction_cost"]

    exposures = exposure_summary(panel[["date", "weight"]]).shift(1)
    returns = returns.join(exposures)
    returns["nav"] = nav_from_returns(returns["net_return"])
    returns["drawdown"] = drawdown_from_nav(returns["nav"])
    return returns.reset_index()
