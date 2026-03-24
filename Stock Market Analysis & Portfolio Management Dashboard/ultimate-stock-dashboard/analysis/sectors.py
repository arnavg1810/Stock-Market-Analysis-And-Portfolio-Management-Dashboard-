"""
Sector/industry info for tickers (via yfinance). Used for sector allocation view.
"""
import pandas as pd
import yfinance as yf


def get_sector_allocation(ticker_list, weights_series):
    """
    Get sector for each ticker and aggregate weights by sector.
    ticker_list: list of ticker strings
    weights_series: pd.Series index = ticker, value = weight (e.g. from optimization)
    Returns: pd.Series index=sector, value=sum of weights (or counts if weights not provided).
    """
    sector_map = {}
    for t in ticker_list:
        if t.startswith("^"):
            sector_map[t] = "Index"
            continue
        try:
            info = yf.Ticker(t).info
            sector = info.get("sector") or info.get("industry") or "Unknown"
            sector_map[t] = sector
        except Exception:
            sector_map[t] = "Unknown"
    if weights_series is not None and not weights_series.empty:
        by_sector = {}
        for t, w in weights_series.items():
            if t in sector_map:
                s = sector_map[t]
                by_sector[s] = by_sector.get(s, 0.0) + float(w)
        return pd.Series(by_sector).sort_values(ascending=False) if by_sector else pd.Series(dtype=float)
    # Count by sector
    from collections import Counter
    cnt = Counter(sector_map.values())
    return pd.Series(cnt).sort_values(ascending=False)
