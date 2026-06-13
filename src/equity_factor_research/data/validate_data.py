"""Validation checks for raw and processed equity panels."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ValidationReport:
    rows: int
    dates: int
    tickers: int
    duplicate_rows: int
    negative_prices: int
    zero_prices: int
    infinite_values: int
    missing_fraction: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        """Return a serializable representation."""
        return asdict(self)


def validate_panel(
    panel: pd.DataFrame,
    price_column: str = "PX_LAST",
    required_columns: tuple[str, ...] = ("date", "ticker", "PX_LAST"),
) -> ValidationReport:
    """Validate structure and common provider-data failure modes."""
    missing_required = sorted(set(required_columns) - set(panel.columns))
    if missing_required:
        raise ValueError(f"Panel is missing required columns: {missing_required}")

    numeric = panel.select_dtypes(include="number")
    report = ValidationReport(
        rows=len(panel),
        dates=panel["date"].nunique(),
        tickers=panel["ticker"].nunique(),
        duplicate_rows=int(panel.duplicated(["date", "ticker"]).sum()),
        negative_prices=int((panel[price_column] < 0).sum()),
        zero_prices=int((panel[price_column] == 0).sum()),
        infinite_values=int(np.isinf(numeric.to_numpy()).sum()),
        missing_fraction={
            column: float(panel[column].isna().mean())
            for column in panel.columns
            if column not in {"date", "ticker"}
        },
    )
    if report.duplicate_rows:
        raise ValueError("Panel contains duplicate date-ticker observations.")
    if report.negative_prices or report.zero_prices:
        raise ValueError("Panel contains non-positive prices.")
    return report
