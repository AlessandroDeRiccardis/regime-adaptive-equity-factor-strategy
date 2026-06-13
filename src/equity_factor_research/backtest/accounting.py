"""NAV and drawdown accounting."""

from __future__ import annotations

import pandas as pd


def nav_from_returns(returns: pd.Series, initial_nav: float = 1.0) -> pd.Series:
    """Compound periodic returns into a NAV series."""
    return initial_nav * (1.0 + returns.fillna(0.0)).cumprod()


def drawdown_from_nav(nav: pd.Series) -> pd.Series:
    """Return percentage drawdown from the running NAV maximum."""
    return nav / nav.cummax() - 1.0
