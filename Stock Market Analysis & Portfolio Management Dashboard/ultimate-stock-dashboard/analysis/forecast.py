"""
Simple forecast: next 30-day projection using ARIMA or drift model.
"""
import numpy as np
import pandas as pd


def simple_forecast(price_series, horizon_days=30, method="drift"):
    """
    Simple forecast of log-prices (or prices) for next horizon_days.
    method: 'drift' (random walk with drift) or 'arima' (if statsmodels available).
    Returns: (forecast_dates, forecast_values) for plotting.
    """
    try:
        log_prices = np.log(price_series.dropna())
    except Exception:
        return None, None
    if len(log_prices) < 30:
        return None, None
    if method == "arima":
        try:
            from statsmodels.tsa.arima.model import ARIMA
            model = ARIMA(log_prices, order=(1, 0, 1))
            fitted = model.fit()
            f = fitted.forecast(steps=horizon_days)
            last_date = log_prices.index[-1]
            freq = log_prices.index.freq or pd.infer_freq(log_prices.index) or "B"
            f_dates = pd.date_range(start=last_date, periods=horizon_days + 1, freq=freq)[1:]
            return f_dates, np.exp(f.values)
        except Exception:
            method = "drift"
    # Drift: mean daily log-return * horizon
    log_ret = log_prices.diff().dropna()
    mu = log_ret.mean()
    last = log_prices.iloc[-1]
    last_date = log_prices.index[-1]
    freq = log_prices.index.freq or pd.infer_freq(log_prices.index) or "B"
    f_dates = pd.date_range(start=last_date, periods=horizon_days + 1, freq=freq)[1:]
    forecast_log = last + np.arange(1, horizon_days + 1) * mu
    forecast_values = np.exp(forecast_log)
    return f_dates, forecast_values
