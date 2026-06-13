"""Factor coverage and correlation diagnostics."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def factor_coverage(panel: pd.DataFrame, factor_columns: Sequence[str]) -> pd.DataFrame:
    """Return monthly non-missing coverage for each factor."""
    return panel.groupby("date")[list(factor_columns)].count()


def factor_rank_correlation(panel: pd.DataFrame, factor_columns: Sequence[str]) -> pd.DataFrame:
    """Return the average monthly Spearman factor correlation matrix."""
    correlations = [
        group[list(factor_columns)].corr(method="spearman") for _, group in panel.groupby("date")
    ]
    return sum(correlations) / len(correlations)
