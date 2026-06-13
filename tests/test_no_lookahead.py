import pandas as pd

from equity_factor_research.features.normalization import zscore_cross_section
from equity_factor_research.research.ic_analysis import add_returns


def test_forward_return_changes_do_not_change_current_return():
    dates = pd.date_range("2024-01-31", periods=4, freq="ME")
    panel = pd.DataFrame({"date": dates, "ticker": "A", "PX_LAST": [100.0, 110.0, 121.0, 133.1]})
    baseline = add_returns(panel)
    panel.loc[3, "PX_LAST"] = 10_000.0
    changed = add_returns(panel)
    assert baseline.loc[2, "return_1m"] == changed.loc[2, "return_1m"]


def test_cross_sectional_normalization_does_not_use_future_dates():
    panel = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-31", "2024-01-31", "2024-02-29", "2024-02-29"]),
            "ticker": ["A", "B", "A", "B"],
            "factor": [1.0, 3.0, 2.0, 4.0],
        }
    )
    baseline = zscore_cross_section(panel, ["factor"])
    panel.loc[panel["date"].eq(pd.Timestamp("2024-02-29")), "factor"] = [200.0, 900.0]
    changed = zscore_cross_section(panel, ["factor"])
    assert baseline.loc[:1, "factor_z"].equals(changed.loc[:1, "factor_z"])
