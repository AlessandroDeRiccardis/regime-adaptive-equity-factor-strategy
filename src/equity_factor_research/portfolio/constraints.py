"""Portfolio exposure checks."""

from __future__ import annotations

import pandas as pd


def exposure_summary(weights: pd.DataFrame) -> pd.DataFrame:
    """Compute long, short, gross, and net exposure by formation date."""
    grouped = weights.groupby("date")["weight"]
    long = grouped.apply(lambda x: x.clip(lower=0).sum()).rename("long_exposure")
    short = grouped.apply(lambda x: -x.clip(upper=0).sum()).rename("short_exposure")
    result = pd.concat([long, short], axis=1)
    result["gross_exposure"] = result["long_exposure"] + result["short_exposure"]
    result["net_exposure"] = result["long_exposure"] - result["short_exposure"]
    return result
