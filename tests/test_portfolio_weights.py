import pandas as pd
import pytest

from equity_factor_research.portfolio.constraints import exposure_summary
from equity_factor_research.portfolio.weighting import construct_decile_weights


def test_portfolio_weights_match_intended_gross_and_net_exposure():
    panel = pd.DataFrame(
        {
            "date": pd.Timestamp("2024-01-31"),
            "ticker": ["A", "B", "C", "D"],
            "is_long": [True, True, False, False],
            "is_short": [False, False, True, True],
            "volatility_12m": [0.1, 0.2, 0.1, 0.2],
        }
    )
    weighted = construct_decile_weights(panel, short_ratio=0.4)
    exposure = exposure_summary(weighted).iloc[0]
    assert exposure["long_exposure"] == pytest.approx(1.0)
    assert exposure["short_exposure"] == pytest.approx(0.4)
    assert exposure["gross_exposure"] == pytest.approx(1.4)
    assert exposure["net_exposure"] == pytest.approx(0.6)
