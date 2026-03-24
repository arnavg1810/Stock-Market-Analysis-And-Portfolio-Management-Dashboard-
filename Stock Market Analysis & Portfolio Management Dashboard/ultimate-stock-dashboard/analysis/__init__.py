"""
Stock analysis package: data loading, risk metrics, portfolio optimization, and visualization.
"""
from .data_loader import load_prices
from .risk_metrics import (
    compute_returns,
    max_drawdown,
    drawdown_series,
    sharpe_ratio,
    sortino_ratio,
    rolling_sharpe,
    historical_var,
    parametric_var,
    beta_vs_benchmark,
)
from .portfolio import (
    monte_carlo_optimization,
    rebalancing_backtest,
    annualized_covariance,
)
from .visualization import (
    price_ma_chart_with_crossovers,
    correlation_heatmap,
    covariance_heatmap,
    drawdown_curve_chart,
    risk_return_scatter,
    efficient_frontier_chart,
    rolling_sharpe_chart,
)

__all__ = [
    "load_prices",
    "compute_returns",
    "max_drawdown",
    "drawdown_series",
    "sharpe_ratio",
    "sortino_ratio",
    "rolling_sharpe",
    "historical_var",
    "parametric_var",
    "beta_vs_benchmark",
    "monte_carlo_optimization",
    "rebalancing_backtest",
    "annualized_covariance",
    "price_ma_chart_with_crossovers",
    "correlation_heatmap",
    "covariance_heatmap",
    "drawdown_curve_chart",
    "risk_return_scatter",
    "efficient_frontier_chart",
    "rolling_sharpe_chart",
]
