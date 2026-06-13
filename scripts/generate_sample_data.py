#!/usr/bin/env python
"""Generate a deterministic, non-investable synthetic monthly equity panel."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2008-01-31", "2025-12-31", freq="ME")
    tickers = [f"SYN{i:02d}" for i in range(30)]
    rows: list[dict[str, object]] = []
    for index, ticker in enumerate(tickers):
        quality = rng.normal()
        value = rng.normal()
        shocks = rng.normal(0.006 + index * 0.00005, 0.055, len(dates))
        price = 25.0 * np.exp(np.cumsum(shocks))
        eps = np.maximum(0.1, price * (0.04 + 0.01 * value) + rng.normal(0, 0.2, len(dates)))
        roe = 12.0 + 6.0 * quality + rng.normal(0, 2.0, len(dates))
        ebitda_ev = 7.0 + 1.5 * value + rng.normal(0, 0.8, len(dates))
        for i, date in enumerate(dates):
            rows.append(
                {
                    "date": date,
                    "ticker": ticker,
                    "PX_LAST": price[i],
                    "TRAIL_12M_EPS_BEF_XO_ITEM": eps[i],
                    "RETURN_COM_EQY": roe[i],
                    "EBITDA_EV_YIELD": ebitda_ev[i],
                }
            )
    output = Path(__file__).resolve().parents[1] / "data" / "sample" / "synthetic_panel.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)


if __name__ == "__main__":
    main()
