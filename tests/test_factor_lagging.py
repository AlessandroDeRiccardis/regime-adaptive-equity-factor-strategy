import numpy as np
import pandas as pd

from equity_factor_research.features.lagging import lag_and_fill_fundamentals


def test_fundamentals_are_lagged_and_filled_only_within_ticker():
    dates = pd.date_range("2020-01-31", periods=3, freq="ME")
    panel = pd.DataFrame(
        {
            "date": list(dates) * 2,
            "ticker": ["A"] * 3 + ["B"] * 3,
            "fundamental": [1.0, np.nan, 3.0, 100.0, np.nan, 300.0],
        }
    )
    result = lag_and_fill_fundamentals(panel, ["fundamental"], lag_months=1, fill_limit_months=2)

    assert np.isnan(result.loc[0, "fundamental"])
    assert result.loc[1, "fundamental"] == 1.0
    assert result.loc[2, "fundamental"] == 1.0
    assert np.isnan(result.loc[3, "fundamental"])
    assert result.loc[4, "fundamental"] == 100.0
