# Original Project Audit

Audit date: 2026-06-13. No original file was deleted or modified.

## Source Files

| Original file | Classification | Purpose and audit decision |
|---|---|---|
| `Equity Systematic Long-Short Factor Strategy.ipynb` | Code, narrative, outputs | The only executable workflow. Reads the 2026 workbook, creates factors, IC weights, portfolios, metrics, and figures. Archived unchanged under `legacy/original_notebooks/`. |
| `Group_N_Assignment_3_Report.pdf` | Final report | Ten-page assignment report with results and figures. Contains assignment/group wording and some misleading benchmark and neutrality claims. Archived under `legacy/original_reports/`. |
| `methodology_assignment3.docx` | Methodology documentation | Detailed assignment walkthrough and reported results. Archived under `legacy/original_reports/`. |
| `Data Assignment 3 2026.xlsx` | Raw proprietary data | Current-constituent Bloomberg-style panel used by the notebook. Kept outside the new repository and excluded from Git. |
| `Data Assignment 3 2000.xlsx` | Raw proprietary data | Appears to be a constituent snapshot anchored to 2000; not used by the notebook. Kept outside the repository. |
| `Data Assignment 3 2010.xlsx` | Raw proprietary data | Appears to be a constituent snapshot anchored to 2010; not used by the notebook. Kept outside the repository. |
| `Data Assignment 3 Retriever.xlsx` | Raw proprietary data | Reduced-field retriever workbook containing prices, EPS, and P/B. Not used by the notebook. Kept outside the repository. |
| `.DS_Store` | Machine metadata | Excluded from Git. |

The snapshot interpretation of the 2000 and 2010 workbooks is an inference from
their filenames and security lists. No explicit membership documentation was found.

## Workbook Profiles

| Workbook | Shape | Fields | Security labels | Date range |
|---|---:|---:|---:|---|
| 2000 | 503 x 6,581 | 13 repeated equity fields | 501 non-null labels per repeated field | 1999-12 to 2025-12 |
| 2010 | 503 x 6,581 | 13 repeated equity fields | 501 non-null labels per repeated field | 1999-12 to 2025-12 |
| 2026 | 506 x 6,581 | 13 repeated equity fields | 504 labels, 503-504 unique depending on field | 1999-12 to 2025-12 |
| Retriever | 506 x 1,521 | 3 repeated equity fields | 503-504 labels | 1999-12 to 2025-12 |

The notebook unpivots the 2026 workbook into 157,752 date-ticker rows. It reports
13.41% missing prices, 14.42% missing trailing EPS, 15.03% missing ROE, and
23.00% missing EBITDA/EV yield.

## Generated Figures

All original plots were inspected and archived unchanged under
`legacy/original_reports/figures/`.

| Figure | Purpose |
|---|---|
| `data_integrity_check_1.png` | Monthly missingness by target field |
| `data_integrity_check_2.png` | EBITDA/EV missingness distribution by ticker |
| `data_integrity_check_3.png` | Sample missing-data heatmap |
| `ic_weights.png` | Burn-in IC means and frozen weights |
| `cum_returns.png` | Isolated factor long-short cumulative returns |
| `factors_risk_return.png` | Isolated factor return and volatility comparison |
| `main_strategy.png` | Main strategy NAV and drawdown |
| `pure_alpha.png` | 100/100 dollar-neutral reference NAV and drawdown |
| `quality_filter.png` | Quality short-filter alternative |
| `rolling_performance.png` | Rolling return-to-volatility ratio and returns |
| `sensitivity.png` | Hedge-ratio and SMA sensitivity |
| `heatmap_comparison.png` | Cross-strategy metric comparison |

## Recovered Execution Order

1. Read `Data Assignment 3 2026.xlsx`.
2. Unpivot the Bloomberg grid.
3. Validate missingness and prices.
4. Lag fundamentals, engineer four factors, winsorize, and z-score.
5. Estimate 2010-2013 monthly Spearman IC and freeze non-negative IC weights.
6. Build a composite that receives 100% momentum weight in the audited run.
7. Construct individual factor references and the March 2014 to December 2025 OOS universe.
8. Build inverse-volatility portfolios and a lagged 10-month SMA regime filter.
9. Run the main, dollar-neutral, quality-filter, and sensitivity backtests.
10. Compute metrics and generate figures/report.

## Dependency and Path Audit

- The original notebook depends on pandas, NumPy, SciPy, Matplotlib, Seaborn, and
  an Excel reader. It contains all implementation logic and has no automated tests.
- It hardcodes the relative filename `Data Assignment 3 2026.xlsx`, but contains no
  absolute machine path.
- Figure saves target the current working directory; the separate `Plots/` folder
  appears to have been populated after execution.
- The PDF and DOCX are presentation artifacts dependent on notebook outputs. They
  are not executable inputs.
- No original Python scripts, Markdown files, package configuration, environment
  file, or automated test configuration were present.

## Scientific and Implementation Findings

- The main strategy is regime-adaptive and usually long-only, not continuously
  long-short. The short book is off in bull regimes and partially active in bears.
- The original "Info Sharpe" is annualized return divided by annualized
  volatility. It is not an Information Ratio.
- The original benchmark is the monthly average return of the available universe.
  It is a monthly rebalanced equal-weight available-universe benchmark, not a
  static buy-and-hold benchmark.
- The original 100/100 reference is dollar-neutral, but its reported beta is
  -0.347. Dollar neutrality does not imply beta neutrality.
- The original grouped fundamental shift is followed by an ungrouped forward-fill.
  This can copy values across ticker boundaries. The refactored implementation
  fixes this and tests it.
- The original individual-factor backtest combines lagged weights with an already
  forward-shifted return, introducing an additional period mismatch.
- The original workbook reflects current constituents and therefore creates
  material survivorship bias.
- The reported main-strategy improvement is partly beta-driven. The audited OLS
  beta is 0.810 and the dollar-neutral reference has a weak return-to-volatility
  ratio of 0.082.
- The original report calls the short sizing a variance ratio, but the code uses a
  weighted-volatility proxy rather than a full covariance-based variance estimate.

## Personal and Assignment Material

No personal email or student ID was found. Assignment, group, and course-style
wording appears throughout the original notebook, PDF, and DOCX. Those materials
remain only in `legacy/`.
