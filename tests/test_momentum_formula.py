import numpy as np
import pandas as pd

from equity_factor_research.features.momentum import add_skip_month_momentum


def test_momentum_uses_t_minus_1_to_t_minus_12_not_current_price():
    dates = pd.date_range("2020-01-31", periods=13, freq="ME")
    panel = pd.DataFrame({"date": dates, "ticker": "A", "PX_LAST": np.arange(1.0, 14.0)})
    result = add_skip_month_momentum(panel)

    expected = panel.loc[11, "PX_LAST"] / panel.loc[0, "PX_LAST"] - 1.0
    assert result.loc[12, "factor_momentum"] == expected

    panel.loc[12, "PX_LAST"] = 10_000.0
    changed = add_skip_month_momentum(panel)
    assert changed.loc[12, "factor_momentum"] == expected
