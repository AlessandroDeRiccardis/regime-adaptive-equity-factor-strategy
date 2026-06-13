"""Individual factor backtest helpers."""

from __future__ import annotations

import pandas as pd

from equity_factor_research.backtest.engine import run_backtest
from equity_factor_research.portfolio.ranking import add_decile_selection


def equal_weight_factor_backtest(
    panel: pd.DataFrame,
    factor_column: str,
    transaction_cost_bps: float = 3.0,
) -> pd.DataFrame:
    """Run an equal-weight top-minus-bottom decile factor reference."""
    selected = add_decile_selection(panel, score_column=factor_column)
    selected["weight"] = 0.0
    long_count = selected.groupby("date")["is_long"].transform("sum")
    short_count = selected.groupby("date")["is_short"].transform("sum")
    selected.loc[selected["is_long"], "weight"] = 1.0 / long_count[selected["is_long"]]
    selected.loc[selected["is_short"], "weight"] = -1.0 / short_count[selected["is_short"]]
    return run_backtest(selected, transaction_cost_bps=transaction_cost_bps)
