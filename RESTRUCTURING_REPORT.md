# Restructuring Report

Completed: 2026-06-13

## Outcome

Created `regime-adaptive-equity-factor-strategy/` as a professional research
repository. Every original source file remains untouched in the parent workspace.
The original notebook, PDF, DOCX, and figures were copied into `legacy/` for
traceability.

## Final Repository Tree

```text
README.md                  Public research narrative and verified results
PROJECT_AUDIT.md           Original-file and scientific audit
RESTRUCTURING_REPORT.md    This delivery report
pyproject.toml             Package and tooling configuration
requirements.txt           Pip dependency list
environment.yml            Conda environment
Makefile                   Install, test, lint, format, and reproduction commands
configs/default.yaml       Research parameters
data/README.md             Proprietary-data policy and schemas
data/sample/               Synthetic public sample
src/equity_factor_research/
  data/                    Loading, validation, reshaping, master panel
  features/                Lagging, factors, winsorization, z-scores, composite
  research/                IC, diagnostics, factor references, benchmarks
  portfolio/               Ranking, weighting, regime, costs, constraints
  backtest/                Engine, accounting, performance, risk, attribution
  plotting/                Reusable figures and tables
scripts/                   High-level executable workflows
notebooks/                 Six thin research walkthroughs
reports/                   Ignored generated public-facing outputs
tests/                     Synthetic bias, weighting, cost, and accounting tests
legacy/                    Unchanged original notebook, report, DOCX, and figures
```

## Files Created, Copied, and Modified

- Created the complete package, configuration, scripts, notebooks, tests,
  documentation, environment files, and synthetic sample.
- Copied the original notebook to `legacy/original_notebooks/`.
- Copied the original PDF, DOCX, and twelve figures to
  `legacy/original_reports/`.
- Did not move, modify, or delete any original parent-workspace file.
- Did not copy the four large source workbooks into the repository.

## Git Exclusions

The repository excludes proprietary Excel/Parquet files, raw data, processed
panels, generated report figures/tables, caches, virtual environments, and
machine metadata. Synthetic sample data and placeholders remain trackable.

## Verified Commands

```bash
make install
make test
make lint
make reproduce
```

Verified real-workbook reproduction:

```bash
EQUITY_FACTOR_RAW_DATA="../Data Assignment 3 2026.xlsx" make reproduce
```

Individual stages:

```bash
make data
make research
make backtest
make figures
```

## Verification Results

- Python compilation: passed.
- Ruff lint: passed.
- Black format check: passed.
- Pytest: 12 tests passed.
- Synthetic full pipeline: passed.
- Authorized local 2026-workbook full pipeline: passed, producing 157,752
  processed observations and 142 OOS monthly rows.

## Key Assumptions

- The 2026 workbook is the intended main source because the original notebook
  explicitly reads it.
- The 2000 and 2010 workbooks are alternative constituent snapshots; this is an
  inference, not confirmed metadata.
- The public benchmark is correctly labeled as monthly rebalanced equal-weight
  available-universe.
- The 100/100 reference is dollar-neutral, not beta-neutral.
- Fundamental values require a two-month lag and ten-month within-ticker fill cap.

## Missing Inputs and Future Extensions

- Point-in-time S&P 500 membership and delisted securities.
- Borrow availability, borrow fees, rebates, and nonlinear market impact.
- Confirmed Bloomberg field publication timestamps and adjustment conventions.
- Factor ablation, momentum-only versus composite, and equal-weight versus
  IC-weighted composite are documented future extensions.

## Manual Review Items and Remaining Risks

- Confirm that all contributors agree with the public coursework statement and
  licensing choice.
- Review whether any legacy coursework material should be published at all.
- Survivorship bias remains material.
- The strategy has substantial market beta.
- Benchmark choice materially changes the performance conclusion.
- The selected IC composite is fully concentrated in momentum.
- Linear transaction costs likely understate live implementation costs.
