import pandas as pd

from equity_factor_research.portfolio.regime_filter import lagged_sma_regime


def test_regime_signal_is_lagged():
    dates = pd.date_range("2020-01-31", periods=6, freq="ME")
    returns = pd.Series([0.01, 0.02, -0.01, 0.03, 0.01, -0.50], index=dates)
    baseline = lagged_sma_regime(returns, sma_window_months=3)
    changed = returns.copy()
    changed.iloc[-1] = 5.0
    rerun = lagged_sma_regime(changed, sma_window_months=3)
    assert baseline.iloc[-1]["bull_regime"] == rerun.iloc[-1]["bull_regime"]
