#!/usr/bin/env python
"""Run dataset, factor research, backtest, and artifact generation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    scripts = Path(__file__).resolve().parent
    for name in (
        "build_dataset.py",
        "run_factor_research.py",
        "run_backtest.py",
        "generate_report_artifacts.py",
    ):
        subprocess.run([sys.executable, str(scripts / name)], check=True)


if __name__ == "__main__":
    main()
