"""Build the reusable monthly research panel."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd

from equity_factor_research.data.reshape_data import sort_panel
from equity_factor_research.data.validate_data import validate_panel
from equity_factor_research.features.factor_definitions import (
    FACTOR_COLUMNS,
    add_factor_definitions,
)
from equity_factor_research.features.lagging import lag_and_fill_fundamentals
from equity_factor_research.features.normalization import zscore_cross_section
from equity_factor_research.features.winsorization import winsorize_cross_section
from equity_factor_research.research.ic_analysis import add_returns

FUNDAMENTAL_COLUMNS = (
    "TRAIL_12M_EPS_BEF_XO_ITEM",
    "RETURN_COM_EQY",
    "PX_TO_BOOK_RATIO",
    "TOT_DEBT_TO_TOT_EQY",
    "PROF_MARGIN",
    "CASH_CONVERSION_CYCLE",
    "AVERAGE_DIVIDEND_YIELD",
    "NET_DEBT",
    "EBITDA_EV_YIELD",
    "OPER_INC_GROWTH",
)


def build_master_dataset(panel: pd.DataFrame, config: Mapping[str, object]) -> pd.DataFrame:
    """Validate, lag, engineer, winsorize, normalize, and add returns."""
    validate_panel(panel)
    result = sort_panel(panel)
    feature_config = config["features"]
    result = lag_and_fill_fundamentals(
        result,
        FUNDAMENTAL_COLUMNS,
        lag_months=int(feature_config["fundamental_lag_months"]),
        fill_limit_months=int(feature_config["fundamental_fill_limit_months"]),
    )
    result = add_factor_definitions(
        result,
        momentum_lookback_months=int(feature_config["momentum_lookback_months"]),
        momentum_skip_months=int(feature_config["momentum_skip_months"]),
    )
    result = winsorize_cross_section(
        result,
        FACTOR_COLUMNS,
        lower=float(feature_config["winsor_lower"]),
        upper=float(feature_config["winsor_upper"]),
    )
    winsorized = [f"{column}_winsorized" for column in FACTOR_COLUMNS]
    result = zscore_cross_section(result, winsorized)
    return add_returns(result)
