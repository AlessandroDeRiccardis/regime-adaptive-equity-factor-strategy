"""Audited factor definitions used by the original research."""

from __future__ import annotations

import numpy as np
import pandas as pd

from equity_factor_research.features.momentum import add_skip_month_momentum

FACTOR_COLUMNS = (
    "factor_earnings_yield",
    "factor_roe",
    "factor_ebitda_ev",
    "factor_momentum",
)


def add_factor_definitions(
    panel: pd.DataFrame,
    momentum_lookback_months: int = 12,
    momentum_skip_months: int = 1,
) -> pd.DataFrame:
    """Create earnings yield, ROE, EBITDA/EV yield, and 12M-1M momentum."""
    required = {
        "PX_LAST",
        "TRAIL_12M_EPS_BEF_XO_ITEM",
        "RETURN_COM_EQY",
        "EBITDA_EV_YIELD",
    }
    missing = sorted(required - set(panel.columns))
    if missing:
        raise ValueError(f"Cannot construct factors; missing fields: {missing}")

    result = panel.copy()
    result["factor_earnings_yield"] = np.where(
        result["PX_LAST"] > 0.01,
        result["TRAIL_12M_EPS_BEF_XO_ITEM"] / result["PX_LAST"],
        np.nan,
    )
    result["factor_roe"] = result["RETURN_COM_EQY"]
    result["factor_ebitda_ev"] = result["EBITDA_EV_YIELD"]
    result = add_skip_month_momentum(
        result,
        lookback_months=momentum_lookback_months,
        skip_months=momentum_skip_months,
    )
    result.replace([np.inf, -np.inf], np.nan, inplace=True)
    return result
