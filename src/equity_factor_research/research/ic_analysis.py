"""Information-coefficient analysis with frozen burn-in weights."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def add_returns(
    panel: pd.DataFrame,
    price_column: str = "PX_LAST",
) -> pd.DataFrame:
    """Add contemporaneous and next-month returns without implicit price fills."""
    result = panel.sort_values(["ticker", "date"]).copy()
    result["return_1m"] = result.groupby("ticker", sort=False)[price_column].pct_change(
        fill_method=None
    )
    result["forward_return_1m"] = result.groupby("ticker", sort=False)["return_1m"].shift(-1)
    return result


def monthly_information_coefficients(
    panel: pd.DataFrame,
    factor_columns: Sequence[str],
    forward_return_column: str = "forward_return_1m",
    minimum_observations: int = 20,
) -> pd.DataFrame:
    """Compute monthly Spearman rank IC for each factor."""
    rows: list[dict[str, object]] = []
    for date, group in panel.groupby("date", sort=True):
        row: dict[str, object] = {"date": date}
        for factor in factor_columns:
            valid = group[[factor, forward_return_column]].dropna()
            row[factor] = (
                valid[factor].corr(valid[forward_return_column], method="spearman")
                if len(valid) >= minimum_observations
                else float("nan")
            )
        rows.append(row)
    return pd.DataFrame(rows).set_index("date")


def estimate_frozen_ic_weights(
    panel: pd.DataFrame,
    factor_columns: Sequence[str],
    burn_in_start: str | pd.Timestamp,
    burn_in_end: str | pd.Timestamp,
    minimum_observations: int = 20,
    zero_floor_negative: bool = True,
) -> tuple[pd.Series, pd.DataFrame]:
    """Estimate factor weights using only the declared burn-in interval."""
    start = pd.Timestamp(burn_in_start)
    end = pd.Timestamp(burn_in_end)
    burn_in = panel.loc[panel["date"].between(start, end)]
    ic = monthly_information_coefficients(
        burn_in,
        factor_columns,
        minimum_observations=minimum_observations,
    )
    means = ic.mean()
    raw = means.clip(lower=0) if zero_floor_negative else means
    if raw.abs().sum() == 0:
        weights = pd.Series(1 / len(factor_columns), index=factor_columns, dtype=float)
    else:
        weights = raw / raw.abs().sum()
    weights.name = "weight"
    return weights, ic
