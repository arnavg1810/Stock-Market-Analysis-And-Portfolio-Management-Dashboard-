"""
Portfolio optimization (Monte Carlo) and rebalancing backtest.
"""
import numpy as np
import pandas as pd


def annualized_covariance(daily_returns, periods_per_year=252):
    """Annualized covariance matrix from daily returns."""
    return daily_returns.cov() * periods_per_year


def monte_carlo_optimization(
    daily_returns,
    risk_free_rate,
    n_portfolios=10000,
    seed=42,
):
    """
    Monte Carlo: random weights, expected return, vol, Sharpe.
    Returns (portfolios_df, max_sharpe_port, min_vol_port).
    """
    tickers = list(daily_returns.columns)
    n_assets = len(tickers)
    mean_ret = daily_returns.mean() * 252
    cov_matrix = daily_returns.cov() * 252
    if cov_matrix.isna().any().any():
        cov_matrix = cov_matrix.fillna(0.0)

    np.random.seed(seed)
    results = np.zeros((3 + n_assets, n_portfolios))
    for i in range(n_portfolios):
        w = np.random.random(n_assets)
        w /= w.sum()
        port_ret = np.dot(w, mean_ret)
        port_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        port_sharpe = (port_ret - risk_free_rate) / port_vol if port_vol > 0 else 0
        results[0, i] = port_ret
        results[1, i] = port_vol
        results[2, i] = port_sharpe
        results[3 : 3 + n_assets, i] = w

    cols = ["Return", "Volatility", "Sharpe"] + tickers
    portfolios_df = pd.DataFrame(results.T, columns=cols)
    max_sharpe_idx = portfolios_df["Sharpe"].idxmax()
    min_vol_idx = portfolios_df["Volatility"].idxmin()
    max_sharpe_port = portfolios_df.loc[max_sharpe_idx]
    min_vol_port = portfolios_df.loc[min_vol_idx]
    return portfolios_df, max_sharpe_port, min_vol_port


def _optimize_weights_once(daily_returns_window, risk_free_rate, n_trials=2000, seed=42):
    """One-shot max-Sharpe weights for a given returns window."""
    tickers = list(daily_returns_window.columns)
    n_assets = len(tickers)
    mean_ret = daily_returns_window.mean() * 252
    cov_matrix = daily_returns_window.cov() * 252
    if cov_matrix.isna().any().any():
        cov_matrix = cov_matrix.fillna(0.0)
    np.random.seed(seed)
    best_sharpe = -np.inf
    best_w = None
    for _ in range(n_trials):
        w = np.random.random(n_assets)
        w /= w.sum()
        r = np.dot(w, mean_ret)
        v = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        if v > 0 and (r - risk_free_rate) / v > best_sharpe:
            best_sharpe = (r - risk_free_rate) / v
            best_w = w
    return best_w, tickers


def rebalancing_backtest(
    daily_returns,
    risk_free_rate,
    rebalance_freq="M",
    n_trials_per_period=2000,
    seed=42,
):
    """
    Monthly (or other freq) rebalanced portfolio vs static (one-time) max-Sharpe.
    rebalance_freq: 'M' for month-end, or e.g. 'W' for week.
    Returns (rebalanced_curve, static_curve, rebalance_dates).
    """
    tickers = list(daily_returns.columns)
    n_assets = len(tickers)
    # Static: optimize on full sample
    static_w, _ = _optimize_weights_once(daily_returns, risk_free_rate, n_trials_per_period, seed)
    if static_w is None:
        static_w = np.ones(n_assets) / n_assets
    static_ret = (daily_returns * static_w).sum(axis=1)
    static_curve = (1 + static_ret).cumprod()
    static_curve.name = "Static (one-time) weights"

    # Rebalanced: at each month start, optimize on history up to previous month-end, then apply weights for the month
    dr = daily_returns.copy()
    dr["_period"] = dr.index.to_period(rebalance_freq)
    periods = sorted(dr["_period"].dropna().unique())
    if not periods:
        return static_curve, static_curve, []
    rebalance_dates = []
    # Build daily portfolio returns with rebalancing
    port_ret_rebal = pd.Series(index=dr.index, dtype=float)
    port_ret_rebal[:] = np.nan
    current_weights = np.ones(n_assets) / n_assets

    for i, per in enumerate(periods):
        mask = dr["_period"] == per
        period_dates = dr.loc[mask].index
        if len(period_dates) == 0:
            continue
        # Lookback: all data before this period
        lookback = dr.loc[dr.index < period_dates[0]].drop(columns=["_period"], errors="ignore")
        if len(lookback) >= 60:
            w, _ = _optimize_weights_once(lookback, risk_free_rate, n_trials_per_period, seed)
            if w is not None:
                current_weights = w
        rebalance_dates.append(period_dates[0])
        # Apply current weights to this period's returns
        period_returns = dr.loc[mask].drop(columns=["_period"])
        port_ret_rebal.loc[mask] = (period_returns * current_weights).sum(axis=1).values

    port_ret_rebal = port_ret_rebal.dropna()
    rebal_curve = (1 + port_ret_rebal).cumprod()
    rebal_curve.name = "Monthly rebalanced"
    # Align static to same index for comparison
    static_curve = static_curve.reindex(rebal_curve.index).ffill().bfill()
    return rebal_curve, static_curve, rebalance_dates
