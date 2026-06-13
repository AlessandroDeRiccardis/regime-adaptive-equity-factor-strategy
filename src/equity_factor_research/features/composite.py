"""Composite factor score construction."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd


def build_composite_score(
    panel: pd.DataFrame,
    weights: Mapping[str, float],
    output_column: str = "composite_score",
    require_all_factors: bool = True,
) -> pd.DataFrame:
    """Build a weighted factor score using frozen externally estimated weights."""
    result = panel.copy()
    columns = list(weights)
    missing = sorted(set(columns) - set(result.columns))
    if missing:
        raise ValueError(f"Composite columns missing from panel: {missing}")
    result[output_column] = sum(result[column] * weight for column, weight in weights.items())
    if require_all_factors:
        result.loc[result[columns].isna().any(axis=1), output_column] = pd.NA
    return result
