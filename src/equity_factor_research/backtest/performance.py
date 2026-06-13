"""Performance metrics with unambiguous terminology."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from equity_factor_research.backtest.accounting import drawdown_from_nav, nav_from_returns
from equity_factor_research.backtest.risk import alpha_beta_regression


def performance_metrics(
    returns: pd.Series,
    benchmark_returns: pd.Series | None = None,
    turnover: pd.Series | None = None,
    transaction_costs: pd.Series | None = None,
    periods_per_year: int = 12,
) -> dict[str, float]:
    """Compute strategy, active-risk, and market-regression metrics."""
    returns = pd.Series(returns, dtype=float).dropna()
    n = len(returns)
    if n == 0:
        raise ValueError("Cannot compute metrics for an empty return series.")

    cumulative_return = float((1.0 + returns).prod() - 1.0)
    annualized_return = float((1.0 + cumulative_return) ** (periods_per_year / n) - 1.0)
    annualized_volatility = float(returns.std(ddof=1) * np.sqrt(periods_per_year))
    nav = nav_from_returns(returns)
    metrics = {
        "cumulative_return": cumulative_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_like_ratio": (
            annualized_return / annualized_volatility if annualized_volatility > 0 else np.nan
        ),
        "max_drawdown": float(drawdown_from_nav(nav).min()),
        "positive_month_ratio": float(returns.gt(0).mean()),
        "skewness": float(stats.skew(returns, bias=False)),
        "excess_kurtosis": float(stats.kurtosis(returns, bias=False)),
        "average_turnover": float(pd.Series(turnover).mean()) if turnover is not None else np.nan,
        "transaction_cost_drag_annualized": (
            float(pd.Series(transaction_costs).mean() * periods_per_year)
            if transaction_costs is not None
            else np.nan
        ),
    }

    if benchmark_returns is not None:
        aligned = pd.concat(
            [returns.rename("strategy"), pd.Series(benchmark_returns).rename("benchmark")],
            axis=1,
        ).dropna()
        active = aligned["strategy"] - aligned["benchmark"]
        tracking_error = float(active.std(ddof=1) * np.sqrt(periods_per_year))
        annualized_active_return = float(active.mean() * periods_per_year)
        metrics.update(
            {
                "annualized_active_return": annualized_active_return,
                "tracking_error": tracking_error,
                "information_ratio": (
                    annualized_active_return / tracking_error if tracking_error > 0 else np.nan
                ),
                "benchmark_correlation": float(aligned["strategy"].corr(aligned["benchmark"])),
                **alpha_beta_regression(aligned["strategy"], aligned["benchmark"]),
            }
        )
    return metrics
