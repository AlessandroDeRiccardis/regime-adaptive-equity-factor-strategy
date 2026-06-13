# Regime-Adaptive Equity Factor Strategy

[![CI](https://github.com/AlessandroDeRiccardis/regime-adaptive-equity-factor-strategy/actions/workflows/ci.yml/badge.svg)](https://github.com/AlessandroDeRiccardis/regime-adaptive-equity-factor-strategy/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> A reproducible S&P 500 cross-sectional factor research framework with
> IC-weighted signals, no-look-ahead controls, transaction-cost-aware backtesting,
> and regime-dependent hedge sizing.

This repository is a cleaned and reorganized research implementation based on
group coursework. The public-facing repository focuses on reproducibility,
implementation quality, and honest research presentation.

The MIT license covers the cleaned implementation. Preserved group-coursework
materials under `legacy/` remain subject to their original authors' rights.

## Research Question

Can a cross-sectional equity factor model combine value, quality, and momentum
signals with a lagged market-regime filter to improve risk-adjusted performance
relative to an equal-weight available-universe benchmark, after transaction costs?

## Why This Matters for Quantitative Trading

The project demonstrates the full research chain rather than advertising a
backtest result: provider-data validation, point-in-time signal design, frozen
burn-in IC weights, cross-sectional portfolio construction, execution lag,
turnover and costs, benchmark definition, and alpha/beta decomposition.

## Data Overview

The audited source is a Bloomberg-style monthly panel covering December 1999 to
December 2025. The main workbook contains 504 security labels and 13 repeated
equity fields after excluding an `ES1 Index` artifact. The original workflow uses
price, trailing EPS before extraordinary items, ROE, and EBITDA/EV yield.

Raw workbooks are not committed. See [data/README.md](data/README.md) for the
audited grid layout, tidy schemas, and local setup.

## Data Limitations

- The original notebook uses a current-constituent snapshot, creating material
  survivorship bias.
- Historical delistings and point-in-time S&P 500 membership are unavailable.
- Bloomberg field timing, adjustments, and licensing must be reviewed by an
  authorized data user.
- The strict four-factor completeness rule excludes many observations and can
  create selection bias.
- Public users can run the pipeline on synthetic data, but cannot reproduce the
  original empirical results without the licensed workbook.

## Feature Engineering

The audited factors are:

| Factor | Definition |
|---|---|
| Earnings yield | Lagged trailing EPS before extraordinary items / current price |
| ROE | Lagged Bloomberg `RETURN_COM_EQY` |
| EBITDA/EV yield | Lagged Bloomberg `EBITDA_EV_YIELD` |
| 12M-1M momentum | `P[t-1] / P[t-12] - 1` |

Signals are winsorized at monthly cross-sectional 1st/99th percentiles and
z-scored within month.

## No-Look-Ahead Protocol

- Fundamentals are shifted two months and forward-filled only within ticker,
  with a ten-month fill cap.
- Momentum excludes the current month.
- IC weights are estimated only on the declared 2010-2013 burn-in interval.
- Regime classification at month `t` uses benchmark information through `t-1`.
- Portfolio weights formed at `t` are applied to returns realized at `t+1`.
- Returns use `pct_change(fill_method=None)` to avoid implicit missing-price fills.
- Normalization is cross-sectional by month, never full-sample.

These assumptions are enforced by synthetic tests.

## IC Analysis and Signal Selection

Monthly Spearman rank ICs are estimated during the burn-in period. Negative mean
IC values are floored at zero, positive values are normalized, and the resulting
weights are frozen before OOS evaluation.

In the audited legacy run, earnings yield, ROE, and EBITDA/EV had negative burn-in
mean ICs; momentum received a frozen weight of 1.00. The resulting score is
therefore economically a momentum signal, while the other factors still restrict
the eligible universe through the completeness rule.

## Portfolio Construction

The main portfolio selects the top and bottom score deciles and uses
inverse-trailing-volatility weights within each leg. The long leg targets 100%
gross exposure. The short leg is disabled in bull regimes and targets 40% gross
exposure in bear regimes.

The 100/100 reference is **dollar-neutral**, not beta-neutral. Its audited OLS beta
is -0.347, which demonstrates why those terms must not be used interchangeably.

## Regime Filter and Hedge Sizing

The regime filter compares a lagged equal-weight universe cumulative index with a
lagged moving average. The audited main setting uses a ten-month SMA:

- Bull regime: 100/0, long-only.
- Bear regime: 100/40, partially hedged.

The original report labels the short scaling as a variance ratio, but its code
uses a weighted-volatility proxy rather than a covariance-based portfolio
variance estimate. The refactored code describes it as gross short exposure.

## Transaction Costs and Turnover

The linear cost model applies 3 bps one-way to half the absolute portfolio weight
change. Turnover includes entries, exits, and changes in existing positions.
Costs are aligned with the period after portfolio formation.

The audited legacy run reports average monthly turnover of 24.54% for the main
strategy. Capacity, market impact, borrow availability, and short rebates are not
modeled.

## Benchmark Definition

The original code computes the mean return of available securities every month.
The correct label is:

**Monthly rebalanced equal-weight available-universe benchmark.**

It is not a static buy-and-hold benchmark, despite the wording in the original
report. The refactored framework implements and saves both the monthly rebalanced
benchmark and a static equal-weight buy-and-hold reference.

## Performance Metrics

The performance module distinguishes:

- `sharpe_like_ratio = annualized_return / annualized_volatility`
- `active_return = strategy_return - benchmark_return`
- `tracking_error = annualized std(active_return)`
- `information_ratio = annualized_active_return / tracking_error`

It also computes cumulative return, max drawdown, positive-month ratio, skewness,
excess kurtosis, turnover, transaction-cost drag, benchmark correlation, market
beta, alpha, long/short contributions, and gross/net exposure.

## Main Empirical Results

The cleaned pipeline was verified against the authorized local 2026 workbook on
June 13, 2026. Its definitions differ from the original notebook where needed:
annualized return is geometric, transaction costs and turnover are execution
aligned, grouped fundamental fills cannot cross ticker boundaries, and the
Information Ratio is computed from active returns.

| Verified cleaned-pipeline result | Main strategy |
|---|---:|
| Cumulative return | 479.50% |
| Geometric annualized return | 16.13% |
| Annualized volatility | 16.08% |
| Sharpe-like return/volatility ratio | 1.003 |
| True Information Ratio vs monthly EW benchmark | 0.046 |
| Max drawdown | -20.06% |
| Positive months | 65.96% |
| Average monthly turnover | 24.83% |
| Annualized linear transaction-cost drag | 0.09% |
| OLS beta vs monthly EW benchmark | 0.799 |

The monthly rebalanced equal-weight benchmark returned 15.55% annualized, while
the static equal-weight buy-and-hold reference returned 17.08% annualized. The
strategy therefore outperformed the monthly rebalanced benchmark only modestly
and underperformed the static benchmark. This benchmark sensitivity is central
to the interpretation.

For traceability, the table below records results printed by the **original
notebook** under its legacy arithmetic-return and accounting definitions.

| Audited legacy result | Main strategy | Dollar-neutral reference | Monthly EW benchmark |
|---|---:|---:|---:|
| Annualized arithmetic return | 16.65% | 1.54% | 15.75% |
| Annualized volatility | 16.18% | 18.74% | 15.62% |
| Legacy return/volatility ratio | 1.029 | 0.082 | 1.009 |
| Max drawdown | -20.07% | -48.23% | -23.09% |
| Average monthly turnover | 24.54% | 42.88% | Not measured |

The main result is regime-adaptive and materially beta-exposed. Neither table
should be presented as evidence of robust live profitability.

## Alpha/Beta Decomposition

The cleaned main strategy has OLS beta 0.799 against the monthly rebalanced
equal-weight benchmark. Its 100/100 dollar-neutral reference has beta -0.347,
geometric annualized return of -0.25%, a Sharpe-like ratio of -0.013, and a
-48.23% max drawdown. The quality short-filter alternative returned 14.28%
annualized with a Sharpe-like ratio of 0.881 and beta of 0.726.

These results indicate that much of the main strategy's risk-adjusted improvement
comes from deliberate market exposure and regime timing rather than isolated
cross-sectional factor alpha.

## Robustness Checks

Implemented in the cleaned pipeline:

- Hedge-ratio sensitivity: 100/100, 100/70, 100/40, and 100/0.
- SMA-window sensitivity: 6, 10, 12, and 18 months.
- 100/100 dollar-neutral reference.
- Negative-ROE quality short-filter alternative.
- Transaction-cost sensitivity at 0, 3, and 10 bps.
- Benchmark sensitivity against monthly rebalanced and static equal-weight
  references.

Scaffolded as future extensions:

- Borrow-cost and nonlinear market-impact sensitivity.
- Benchmark sensitivity using point-in-time membership.
- Factor ablation.
- Momentum-only versus composite.
- Equal-weight versus IC-weighted composite.

## Repository Structure

```text
configs/                 Reproducible parameters
data/                    Data policy, synthetic sample, ignored local outputs
src/equity_factor_research/
  data/                  Load, reshape, validate, and build the master panel
  features/              Lagging, factors, winsorization, normalization, composite
  research/              IC, diagnostics, factor references, and benchmarks
  portfolio/             Ranking, sizing, regime, costs, and exposures
  backtest/              Engine, accounting, performance, risk, and attribution
  plotting/              Reusable figures and tables
scripts/                 High-level executable workflows
notebooks/               Thin research walkthroughs
reports/                 Generated public-facing figures and tables
tests/                   Synthetic no-look-ahead and accounting tests
legacy/                  Unchanged original notebook, report, and figures
PROJECT_AUDIT.md          Full audit and scientific findings
```

## Installation

```bash
conda env create -f environment.yml
conda activate equity-factor-research
make install
```

Or with an existing Python 3.11+ environment:

```bash
python -m pip install -e ".[dev]"
```

## Reproduction Instructions

Run all tests and reproduce the pipeline with the included synthetic sample:

```bash
make test
make reproduce
```

Run against the authorized workbook currently stored beside this repository:

```bash
EQUITY_FACTOR_RAW_DATA="../Data Assignment 3 2026.xlsx" make reproduce
```

Run individual stages:

```bash
make data
make research
make backtest
make figures
```

Generated outputs are written to `data/processed/`, `reports/tables/`, and
`reports/figures/`. These directories are ignored except for placeholders.

## Limitations

The largest unresolved risk is survivorship bias. Additional limitations include
monthly execution granularity, no borrow constraints, linear transaction costs,
no market-impact model, no sector or beta constraints, a single historical OOS
window, IC concentration in momentum, and uncertainty around provider field
publication timing. The framework is research code, not a production trading
system.

## Disclaimer

This repository is for educational and research purposes only. It is not
investment advice, a solicitation, or evidence that the strategy will be
profitable in live trading. Historical backtests are sensitive to data quality,
biases, costs, and implementation assumptions.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff).
