import pandas as pd

from equity_factor_research.research.ic_analysis import estimate_frozen_ic_weights


def _ic_panel() -> pd.DataFrame:
    rows = []
    for date in pd.to_datetime(["2010-01-31", "2010-02-28", "2014-01-31"]):
        for rank in range(5):
            burn_in = date.year == 2010
            rows.append(
                {
                    "date": date,
                    "ticker": str(rank),
                    "factor_good": rank,
                    "factor_bad": -rank,
                    "forward_return_1m": rank if burn_in else -rank,
                }
            )
    return pd.DataFrame(rows)


def test_ic_weights_use_only_burn_in_data():
    weights, _ = estimate_frozen_ic_weights(
        _ic_panel(),
        ["factor_good", "factor_bad"],
        "2010-01-01",
        "2010-12-31",
        minimum_observations=3,
    )
    assert weights["factor_good"] == 1.0
    assert weights["factor_bad"] == 0.0


def test_negative_ic_factors_receive_zero_weight():
    weights, _ = estimate_frozen_ic_weights(
        _ic_panel(),
        ["factor_good", "factor_bad"],
        "2010-01-01",
        "2010-12-31",
        minimum_observations=3,
        zero_floor_negative=True,
    )
    assert weights["factor_bad"] == 0.0
