"""Panel reshaping helpers."""

from __future__ import annotations

import pandas as pd


def assert_unique_panel(panel: pd.DataFrame) -> None:
    """Raise when date-ticker observations are duplicated."""
    duplicate_count = panel.duplicated(["date", "ticker"]).sum()
    if duplicate_count:
        raise ValueError(f"Panel contains {duplicate_count} duplicate date-ticker rows.")


def sort_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Return a consistently ordered panel."""
    assert_unique_panel(panel)
    return panel.sort_values(["ticker", "date"]).reset_index(drop=True)
