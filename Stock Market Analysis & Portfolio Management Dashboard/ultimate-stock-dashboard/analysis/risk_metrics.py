"""
Risk and return metrics: Sharpe, Sortino, rolling Sharpe, drawdown, VaR, Beta.
Supports both simple and log returns.
"""
import numpy as np
import pandas as pd


def compute_returns(prices_df, use_log_returns=False):
    """
    Compute daily returns from price DataFrame.
    use_log_returns: if True, log returns ln(P_t / P_{t-1}); else simple pct_change().
    """
    if use_log_returns:
        return np.log(prices_df / prices_df.shift(1)).dropna()
    return prices_df.pct_change().dropna()


def max_drawdown(returns_series):
    """Largest peak-to-trough decline (single number)."""
    cum = (1 + returns_series).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    return drawdown.min()


def drawdown_series(returns_series):
    """Full drawdown curve (series)."""
    cum = (1 + returns_series).cumprod()
    running_max = cum.cummax()
    return (cum - running_max) / running_max


def sharpe_ratio(annual_return, annual_vol, risk_free_rate):
    """Sharpe = (R - Rf) / sigma."""
    if annual_vol == 0 or np.isnan(annual_vol):
        return np.nan
    return (annual_return - risk_free_rate) / annual_vol


def sortino_ratio(returns_series, risk_free_rate_annual, periods_per_year=252):
    """
    Sortino = (Return - Rf) / DownsideDeviation.
    Only negative returns are used in the denominator.
    """
    excess = returns_series - (risk_free_rate_annual / periods_per_year)
    downside = returns_series[returns_series < 0]
    if len(downside) == 0:
        return np.nan
    downside_std = np.sqrt((downside ** 2).mean()) * np.sqrt(periods_per_year)
    if downside_std == 0:
        return np.nan
    ann_return = returns_series.mean() * periods_per_year
    return (ann_return - risk_free_rate_annual) / downside_std


def rolling_sharpe(returns_df, window_days, risk_free_rate_annual, periods_per_year=252):
    """
    Rolling Sharpe ratio per column.
    Returns DataFrame with same index/columns as aligned returns.
    """
    rf_daily = risk_free_rate_annual / periods_per_year
    mean_roll = returns_df.rolling(window_days).mean() * periods_per_year
    vol_roll = returns_df.rolling(window_days).std() * np.sqrt(periods_per_year)
    sharpe_roll = (mean_roll - risk_free_rate_annual) / vol_roll.replace(0, np.nan)
    return sharpe_roll


def historical_var(returns_series, confidence=0.95):
    """Historical VaR: (1-confidence) quantile of daily returns (e.g. 0.95 -> 95% VaR)."""
    return np.percentile(returns_series.dropna(), (1 - confidence) * 100)


def _norm_ppf(p):
    """Standard normal quantile. Uses scipy if available; else rough approximation for common p."""
    try:
        from scipy import stats
        return float(stats.norm.ppf(p))
    except ImportError:
        # Approximations for common VaR levels (1-p = 0.05, 0.01, 0.025)
        if abs(p - 0.05) < 0.001:
            return -1.6448536269514722
        if abs(p - 0.01) < 0.001:
            return -2.3263478740408408
        if abs(p - 0.025) < 0.001:
            return -1.9599639845400545
        return np.nan


def parametric_var(returns_series, confidence=0.95):
    """Parametric (normal) VaR: mu + z * sigma for the (1-confidence) quantile. Works without scipy (uses approximation)."""
    z = _norm_ppf(1 - confidence)
    if np.isnan(z):
        return np.nan
    mu = returns_series.mean()
    sigma = returns_series.std()
    if np.isnan(sigma) or sigma == 0:
        return np.nan
    return mu + z * sigma


def beta_vs_benchmark(returns_df, benchmark_col):
    """Beta of each column vs benchmark (column name)."""
    if benchmark_col not in returns_df.columns:
        return pd.Series(0.0, index=returns_df.columns)
    var_bench = returns_df[benchmark_col].var()
    if var_bench == 0:
        return pd.Series(0.0, index=returns_df.columns)
    cov = returns_df.cov()[benchmark_col]
    return cov / var_bench


def annualized_return(returns_series, periods_per_year=252):
    """Annualized return from daily (or other frequency) returns."""
    return returns_series.mean() * periods_per_year


def annualized_volatility(returns_series, periods_per_year=252):
    """Annualized volatility."""
    return returns_series.std() * np.sqrt(periods_per_year)
