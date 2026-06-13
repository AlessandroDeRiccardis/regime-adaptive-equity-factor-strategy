import pandas as pd
import pytest

from equity_factor_research.backtest.engine import run_backtest


def test_weights_at_t_are_applied_to_returns_at_t_plus_1():
    dates = pd.date_range("2024-01-31", periods=3, freq="ME")
    panel = pd.DataFrame(
        {
            "date": dates,
            "ticker": "A",
            "weight": [1.0, 0.0, 0.0],
            "return_1m": [0.0, 0.10, -0.50],
        }
    )
    result = run_backtest(panel, transaction_cost_bps=0).set_index("date")
    assert result.loc[dates[1], "gross_return"] == pytest.approx(0.10)
    assert result.loc[dates[2], "gross_return"] == pytest.approx(0.0)


def test_backtest_output_columns_and_values():
    dates = pd.date_range("2024-01-31", periods=3, freq="ME")
    panel = pd.DataFrame(
        {
            "date": list(dates) * 2,
            "ticker": ["A"] * 3 + ["B"] * 3,
            "weight": [0.5, 0.5, 0.5, -0.5, -0.5, -0.5],
            "return_1m": [0.0, 0.02, 0.01, 0.0, -0.01, 0.03],
        }
    )
    result = run_backtest(panel)
    expected = {"net_return", "turnover", "transaction_cost", "nav", "drawdown"}
    assert expected.issubset(result.columns)
    assert result["net_return"].dropna().gt(-1).all()
    assert result["nav"].gt(0).all()


def test_transaction_costs_reduce_backtest_returns():
    dates = pd.date_range("2024-01-31", periods=3, freq="ME")
    panel = pd.DataFrame(
        {
            "date": dates,
            "ticker": "A",
            "weight": [0.0, 1.0, 0.0],
            "return_1m": [0.0, 0.0, 0.0],
        }
    )
    free = run_backtest(panel, transaction_cost_bps=0)
    costly = run_backtest(panel, transaction_cost_bps=10)
    assert costly["net_return"].sum() < free["net_return"].sum()
