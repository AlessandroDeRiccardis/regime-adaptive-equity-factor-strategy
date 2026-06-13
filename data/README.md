# Data Guide

## Policy

The original project uses Bloomberg-style exports. Those workbooks may be licensed,
proprietary, and unsuitable for a public repository. Raw workbooks are therefore
excluded from Git. Place an authorized workbook at:

`data/raw/bloomberg_panel.xlsx`

Alternatively, set `EQUITY_FACTOR_RAW_DATA=/absolute/path/to/workbook.xlsx`.

The included `data/sample/synthetic_panel.csv` is synthetic and exists only so the
pipeline and tests can run without proprietary data.

## Audited Raw Workbook Schema

The four source workbooks each contain a `Data` sheet. The main 2026 workbook has
506 rows and 6,581 columns. Dates run monthly from December 1999 through December
2025. The Bloomberg grid layout is:

| Excel location | Meaning |
|---|---|
| Row 2, columns E onward | Repeated security identifiers |
| Row 3, columns E onward | Repeated Bloomberg field names |
| Column D, row 4 onward | Monthly dates |
| Row 4 onward, columns E onward | Values |
| Column C | ES1 Index artifact, excluded from the equity panel |

Audited fields include `PX_LAST`, `TRAIL_12M_EPS_BEF_XO_ITEM`,
`RETURN_COM_EQY`, `PX_TO_BOOK_RATIO`, `TOT_DEBT_TO_TOT_EQY`, `PROF_MARGIN`,
`HIST_PUT_IMP_VOL`, `HIST_CALL_IMP_VOL`, `CASH_CONVERSION_CYCLE`,
`AVERAGE_DIVIDEND_YIELD`, `NET_DEBT`, `EBITDA_EV_YIELD`, and
`OPER_INC_GROWTH`.

## Tidy Input Schema

CSV and Parquet inputs may be supplied directly. Required columns are:

| Column | Type | Description |
|---|---|---|
| `date` | date | Month-end observation date |
| `ticker` | string | Stable security identifier |
| `PX_LAST` | float | Adjusted or consistently defined monthly price |
| `TRAIL_12M_EPS_BEF_XO_ITEM` | float | Trailing EPS before extraordinary items |
| `RETURN_COM_EQY` | float | Return on common equity |
| `EBITDA_EV_YIELD` | float | EBITDA to enterprise value yield |

Optional audited fields are preserved when available.

## Processed Panel Schema

`data/processed/master_panel.csv` contains the tidy raw fields, lagged
fundamentals, raw factors, winsorized factors, cross-sectional z-scores,
`return_1m`, and `forward_return_1m`.

## Backtest Output Schema

`data/processed/backtest_returns.csv` contains monthly gross and net returns,
long- and short-leg contributions, turnover, transaction costs, NAV, drawdown,
gross/net exposure, and both benchmark return series.

## Limitations

- The workbook used by the original notebook is a current-constituent snapshot,
  creating material survivorship bias.
- The 2000 and 2010 workbooks appear to be alternative constituent snapshots,
  but no point-in-time membership mapping is supplied.
- Bloomberg field timing and adjustment conventions require license-holder review.
- Processed results cannot be exactly reproduced publicly without an authorized
  copy of the original workbook.
