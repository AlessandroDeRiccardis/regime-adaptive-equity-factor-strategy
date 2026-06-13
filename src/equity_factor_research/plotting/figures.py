"""Minimal report-ready figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_performance(
    backtest: pd.DataFrame,
    output_path: str | Path,
    benchmark_column: str = "benchmark_return",
) -> None:
    """Plot strategy/benchmark NAV and strategy drawdown."""
    data = backtest.set_index("date").copy()
    data["benchmark_nav"] = (1.0 + data[benchmark_column].fillna(0.0)).cumprod()
    data["benchmark_drawdown"] = data["benchmark_nav"] / data["benchmark_nav"].cummax() - 1

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(data.index, data["nav"], label="Regime-adaptive strategy")
    axes[0].plot(data.index, data["benchmark_nav"], linestyle="--", label="Monthly EW benchmark")
    axes[0].set_ylabel("NAV")
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].fill_between(data.index, data["drawdown"], 0, alpha=0.3, label="Strategy")
    axes[1].plot(data.index, data["benchmark_drawdown"], linestyle="--", label="Benchmark")
    axes[1].set_ylabel("Drawdown")
    axes[1].legend()
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_ic_weights(weights: pd.Series, output_path: str | Path) -> None:
    """Plot frozen burn-in IC weights."""
    fig, ax = plt.subplots(figsize=(8, 4))
    weights.plot.bar(ax=ax, color="#315f8c")
    ax.set_title("Frozen burn-in IC weights")
    ax.set_ylabel("Weight")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
