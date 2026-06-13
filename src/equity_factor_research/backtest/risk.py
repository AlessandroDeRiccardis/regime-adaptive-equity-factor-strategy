"""Market beta and alpha regression."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def alpha_beta_regression(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = 12,
) -> dict[str, float]:
    """Run OLS of strategy returns on benchmark returns."""
    aligned = pd.concat(
        [strategy_returns.rename("strategy"), benchmark_returns.rename("benchmark")],
        axis=1,
    ).dropna()
    if len(aligned) < 3:
        return {"alpha_monthly": np.nan, "alpha_annualized": np.nan, "beta": np.nan}
    model = sm.OLS(aligned["strategy"], sm.add_constant(aligned["benchmark"])).fit()
    alpha_monthly = float(model.params["const"])
    return {
        "alpha_monthly": alpha_monthly,
        "alpha_annualized": alpha_monthly * periods_per_year,
        "beta": float(model.params["benchmark"]),
        "r_squared": float(model.rsquared),
    }
