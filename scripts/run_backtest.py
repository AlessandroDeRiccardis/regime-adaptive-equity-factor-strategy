#!/usr/bin/env python
"""Run the main regime-adaptive strategy and transparent benchmarks."""

from __future__ import annotations

import logging

import pandas as pd

from equity_factor_research.backtest.engine import run_backtest
from equity_factor_research.backtest.performance import performance_metrics
from equity_factor_research.config import load_config
from equity_factor_research.features.composite import build_composite_score
from equity_factor_research.logging_utils import configure_logging
from equity_factor_research.plotting.tables import write_metrics
from equity_factor_research.portfolio.ranking import add_decile_selection
from equity_factor_research.portfolio.regime_filter import dynamic_short_ratio, lagged_sma_regime
from equity_factor_research.portfolio.weighting import (
    add_rolling_volatility,
    construct_decile_weights,
)
from equity_factor_research.research.benchmark_analysis import (
    monthly_rebalanced_equal_weight_benchmark,
    static_equal_weight_buy_and_hold_benchmark,
)
from equity_factor_research.research.ic_analysis import estimate_frozen_ic_weights


def build_weighted_variant(
    work: pd.DataFrame,
    short_ratio_by_date: pd.Series,
    quality_short_column: str | None = None,
) -> pd.DataFrame:
    """Build one portfolio variant from a date-indexed short-ratio series."""
    variant = work.copy()
    variant["short_ratio"] = variant["date"].map(short_ratio_by_date)
    return pd.concat(
        [
            construct_decile_weights(
                group,
                float(group["short_ratio"].iloc[0]),
                quality_short_column=quality_short_column,
            )
            for _, group in variant.groupby("date", sort=True)
        ],
        ignore_index=True,
    )


def evaluate_variant(
    weighted: pd.DataFrame,
    monthly_benchmark: pd.Series,
    static_benchmark: pd.Series,
    transaction_cost_bps: float,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Run one strategy variant and calculate monthly-benchmark metrics."""
    backtest = run_backtest(
        weighted,
        transaction_cost_bps=transaction_cost_bps,
    ).set_index("date")
    backtest = backtest.join(monthly_benchmark).join(
        static_benchmark.rename("static_benchmark_return")
    )
    metrics = performance_metrics(
        backtest["net_return"],
        backtest["benchmark_return"],
        backtest["turnover"],
        backtest["transaction_cost"],
    )
    return backtest, metrics


def main() -> None:
    config = load_config()
    configure_logging()
    logger = logging.getLogger(__name__)
    panel = pd.read_csv(config["data"]["processed_path"], parse_dates=["date"])
    factors = [column for column in panel if column.startswith("factor_") and column.endswith("_z")]
    research = config["research"]
    portfolio = config["portfolio"]

    weights, _ = estimate_frozen_ic_weights(
        panel,
        factors,
        research["burn_in_start"],
        research["burn_in_end"],
        int(research["minimum_ic_observations"]),
        bool(research["zero_floor_negative_ic"]),
    )
    panel = build_composite_score(panel, weights.to_dict())
    panel = panel.sort_values(["ticker", "date"])
    panel["smoothed_score"] = panel.groupby("ticker")["composite_score"].transform(
        lambda x: x.rolling(int(portfolio["score_smoothing_months"]), min_periods=1).mean()
    )
    panel = add_rolling_volatility(
        panel,
        lookback_months=int(portfolio["volatility_lookback_months"]),
        minimum_observations=int(portfolio["minimum_volatility_observations"]),
    )
    work = panel[panel["date"].between(research["oos_start"], research["oos_end"])].copy()
    work = work.dropna(subset=["smoothed_score", "volatility_12m", "return_1m"])

    monthly_benchmark = monthly_rebalanced_equal_weight_benchmark(work)
    static_benchmark = static_equal_weight_buy_and_hold_benchmark(
        work, start_date=research["oos_start"]
    )
    regime = lagged_sma_regime(monthly_benchmark, int(portfolio["regime_sma_months"]))
    main_short_ratio = dynamic_short_ratio(
        regime["bull_regime"], float(portfolio["bear_short_ratio"])
    )
    work = add_decile_selection(
        work,
        score_column="smoothed_score",
        top_quantile=float(portfolio["top_quantile"]),
        bottom_quantile=float(portfolio["bottom_quantile"]),
    )
    weighted = build_weighted_variant(work, main_short_ratio)
    backtest, metrics = evaluate_variant(
        weighted,
        monthly_benchmark,
        static_benchmark,
        float(portfolio["transaction_cost_bps"]),
    )
    output = config["data"]["backtest_path"]
    output.parent.mkdir(parents=True, exist_ok=True)
    backtest.reset_index().to_csv(output, index=False)

    write_metrics(metrics, config["output"]["tables_dir"] / "main_strategy_metrics.csv")

    variant_rows = [{"variant": "main_regime_adaptive", **metrics}]
    neutral = build_weighted_variant(
        work, pd.Series(1.0, index=monthly_benchmark.index, dtype=float)
    )
    _, neutral_metrics = evaluate_variant(
        neutral,
        monthly_benchmark,
        static_benchmark,
        float(portfolio["transaction_cost_bps"]),
    )
    variant_rows.append({"variant": "100_100_dollar_neutral", **neutral_metrics})

    quality = build_weighted_variant(
        work,
        main_short_ratio,
        quality_short_column="factor_roe",
    )
    _, quality_metrics = evaluate_variant(
        quality,
        monthly_benchmark,
        static_benchmark,
        float(portfolio["transaction_cost_bps"]),
    )
    variant_rows.append({"variant": "quality_short_filter", **quality_metrics})
    pd.DataFrame(variant_rows).to_csv(
        config["output"]["tables_dir"] / "strategy_comparison.csv", index=False
    )

    hedge_rows = []
    for ratio in (1.0, 0.7, 0.4, 0.0):
        ratio_series = dynamic_short_ratio(regime["bull_regime"], ratio)
        variant = build_weighted_variant(work, ratio_series)
        _, variant_metrics = evaluate_variant(
            variant,
            monthly_benchmark,
            static_benchmark,
            float(portfolio["transaction_cost_bps"]),
        )
        hedge_rows.append({"bear_short_ratio": ratio, **variant_metrics})
    pd.DataFrame(hedge_rows).to_csv(
        config["output"]["tables_dir"] / "hedge_ratio_sensitivity.csv", index=False
    )

    sma_rows = []
    for window in (6, 10, 12, 18):
        window_regime = lagged_sma_regime(monthly_benchmark, window)
        ratio_series = dynamic_short_ratio(
            window_regime["bull_regime"], float(portfolio["bear_short_ratio"])
        )
        variant = build_weighted_variant(work, ratio_series)
        _, variant_metrics = evaluate_variant(
            variant,
            monthly_benchmark,
            static_benchmark,
            float(portfolio["transaction_cost_bps"]),
        )
        sma_rows.append({"sma_window_months": window, **variant_metrics})
    pd.DataFrame(sma_rows).to_csv(
        config["output"]["tables_dir"] / "sma_sensitivity.csv", index=False
    )

    cost_rows = []
    for cost_bps in (0.0, 3.0, 10.0):
        _, cost_metrics = evaluate_variant(weighted, monthly_benchmark, static_benchmark, cost_bps)
        cost_rows.append({"transaction_cost_bps": cost_bps, **cost_metrics})
    pd.DataFrame(cost_rows).to_csv(
        config["output"]["tables_dir"] / "transaction_cost_sensitivity.csv", index=False
    )

    benchmark_rows = [
        {
            "benchmark": "monthly_rebalanced_equal_weight",
            **metrics,
        },
        {
            "benchmark": "static_equal_weight_buy_and_hold",
            **performance_metrics(
                backtest["net_return"],
                backtest["static_benchmark_return"],
                backtest["turnover"],
                backtest["transaction_cost"],
            ),
        },
    ]
    pd.DataFrame(benchmark_rows).to_csv(
        config["output"]["tables_dir"] / "benchmark_sensitivity.csv", index=False
    )
    logger.info("Wrote backtest and metrics. Beta: %.3f", metrics["beta"])


if __name__ == "__main__":
    main()
