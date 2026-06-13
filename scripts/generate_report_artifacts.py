#!/usr/bin/env python
"""Generate figures from saved backtest outputs."""

from __future__ import annotations

import pandas as pd

from equity_factor_research.config import load_config
from equity_factor_research.plotting.figures import plot_performance


def main() -> None:
    config = load_config()
    backtest = pd.read_csv(config["data"]["backtest_path"], parse_dates=["date"])
    plot_performance(backtest, config["output"]["figures_dir"] / "main_strategy.png")


if __name__ == "__main__":
    main()
