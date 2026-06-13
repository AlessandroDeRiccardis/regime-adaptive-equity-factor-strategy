import pandas as pd
import pytest

from equity_factor_research.portfolio.transaction_costs import calculate_turnover, transaction_cost


def test_turnover_and_cost_on_synthetic_rebalance():
    dates = pd.to_datetime(["2024-01-31", "2024-02-29"])
    weights = pd.DataFrame(
        {
            "date": [dates[0], dates[0], dates[1], dates[1]],
            "ticker": ["A", "B", "A", "B"],
            "weight": [0.5, -0.5, 1.0, 0.0],
        }
    )
    turnover = calculate_turnover(weights)
    assert turnover.iloc[0] == pytest.approx(0.5)
    assert turnover.iloc[-1] == pytest.approx(0.5)
    assert transaction_cost(turnover, 3.0).iloc[-1] == pytest.approx(0.00015)
