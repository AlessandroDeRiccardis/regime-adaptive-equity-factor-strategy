"""Load proprietary Bloomberg-style exports or tidy sample panels."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_bloomberg_wide(path: str | Path, sheet_name: str = "Data") -> pd.DataFrame:
    """Read the audited Bloomberg export and return a tidy monthly panel.

    The expected grid has tickers in row 2, field names in row 3, dates in
    column D, and observations starting in row 4 (one-indexed Excel labels).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Raw Bloomberg workbook not found: {path}. "
            "Place it at data/raw/bloomberg_panel.xlsx or set EQUITY_FACTOR_RAW_DATA."
        )

    raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    if raw.shape[0] < 4 or raw.shape[1] < 5:
        raise ValueError("Workbook is too small to match the expected Bloomberg export.")

    dates = pd.to_datetime(raw.iloc[3:, 3], errors="coerce").dropna().reset_index(drop=True)
    core = raw.iloc[:, 4:].copy()
    tickers = core.iloc[1].astype("string")
    fields = core.iloc[2].astype("string")
    values = core.iloc[3 : 3 + len(dates)].reset_index(drop=True)

    panel_wide = pd.DataFrame(values.to_numpy(), index=dates)
    panel_wide.columns = pd.MultiIndex.from_arrays([tickers, fields], names=["ticker", "field"])
    valid = (
        panel_wide.columns.get_level_values("ticker").notna()
        & panel_wide.columns.get_level_values("field").notna()
    )
    panel_wide = panel_wide.loc[:, valid]
    panel_wide = panel_wide.loc[:, ~panel_wide.columns.duplicated(keep="first")]
    panel_wide = panel_wide.apply(pd.to_numeric, errors="coerce")
    panel_wide.index.name = "date"

    panel = (
        panel_wide.stack(level="ticker", future_stack=True)
        .rename_axis(index=["date", "ticker"])
        .reset_index()
    )
    panel.columns.name = None
    panel["ticker"] = panel["ticker"].astype(str).str.strip()
    return panel.sort_values(["ticker", "date"]).reset_index(drop=True)


def read_tidy_panel(path: str | Path) -> pd.DataFrame:
    """Read a tidy CSV or Parquet panel with date and ticker columns."""
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        panel = pd.read_parquet(path)
    elif path.suffix.lower() == ".csv":
        panel = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported tidy panel format: {path.suffix}")
    panel["date"] = pd.to_datetime(panel["date"])
    return panel.sort_values(["ticker", "date"]).reset_index(drop=True)


def load_panel(path: str | Path, sheet_name: str = "Data") -> pd.DataFrame:
    """Load either the Bloomberg workbook or a tidy CSV/Parquet panel."""
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return read_bloomberg_wide(path, sheet_name=sheet_name)
    return read_tidy_panel(path)
