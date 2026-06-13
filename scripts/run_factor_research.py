#!/usr/bin/env python
"""Estimate burn-in ICs and frozen composite weights."""

from __future__ import annotations

import logging

import pandas as pd

from equity_factor_research.config import load_config
from equity_factor_research.logging_utils import configure_logging
from equity_factor_research.plotting.figures import plot_ic_weights
from equity_factor_research.research.ic_analysis import estimate_frozen_ic_weights


def main() -> None:
    config = load_config()
    configure_logging()
    logger = logging.getLogger(__name__)
    panel = pd.read_csv(config["data"]["processed_path"], parse_dates=["date"])
    factors = [column for column in panel if column.startswith("factor_") and column.endswith("_z")]
    research = config["research"]
    weights, monthly_ic = estimate_frozen_ic_weights(
        panel,
        factors,
        research["burn_in_start"],
        research["burn_in_end"],
        int(research["minimum_ic_observations"]),
        bool(research["zero_floor_negative_ic"]),
    )
    tables = config["output"]["tables_dir"]
    tables.mkdir(parents=True, exist_ok=True)
    weights.to_csv(tables / "ic_weights.csv")
    monthly_ic.to_csv(tables / "monthly_ic.csv")
    plot_ic_weights(weights, config["output"]["figures_dir"] / "ic_weights.png")
    logger.info("Wrote IC diagnostics and frozen weights.")


if __name__ == "__main__":
    main()
