#!/usr/bin/env python
"""Build the processed monthly factor panel."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from equity_factor_research.config import load_config
from equity_factor_research.data.build_master_dataset import build_master_dataset
from equity_factor_research.data.load_data import load_panel
from equity_factor_research.logging_utils import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--input", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    configure_logging()
    logger = logging.getLogger(__name__)
    input_path = Path(args.input) if args.input else config["data"]["raw_path"]
    if not input_path.exists() and config["data"]["use_sample_if_raw_missing"]:
        input_path = config["data"]["sample_path"]
        logger.warning("Raw workbook unavailable; using synthetic sample: %s", input_path)

    panel = load_panel(input_path, sheet_name=config["data"]["sheet_name"])
    master = build_master_dataset(panel, config)
    output = config["data"]["processed_path"]
    output.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(output, index=False)
    logger.info("Wrote %s rows to %s", len(master), output)


if __name__ == "__main__":
    main()
