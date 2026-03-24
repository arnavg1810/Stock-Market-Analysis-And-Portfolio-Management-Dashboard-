"""
Data loading and cleaning for stock price data.
Uses yfinance; normalizes single/multi-ticker response to a clean price DataFrame.
Fetches missing tickers individually; uses Ticker().history() fallback when download fails.
"""
import pandas as pd
import yfinance as yf


def _series_from_raw(raw, ticker):
    """Extract price Series from a single-ticker download/history DataFrame."""
    if raw.empty or len(raw) < 2:
        return None
    col = raw["Adj Close"] if "Adj Close" in raw.columns else raw["Close"]
    return col.rename(ticker)


def _fetch_single_ticker(ticker, start, end):
    """Download one ticker; return Series of Adj Close (or Close), or None if failed.
    Tries yf.download() first, then yf.Ticker().history() as fallback (often works for indices).
    """
    # Try download() first
    raw = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
        group_by="ticker",
        threads=False,
    )
    s = _series_from_raw(raw, ticker)
    if s is not None:
        return s
    # Fallback: Ticker().history() (often works when download fails for indices)
    try:
        obj = yf.Ticker(ticker)
        hist = obj.history(start=start, end=end, auto_adjust=False)
        s = _series_from_raw(hist, ticker)
        if s is not None:
            return s
    except Exception:
        pass
    return None


def load_prices(ticker_list, start, end):
    """
    Download OHLCV for tickers and return a DataFrame of (Adjusted) Close prices.
    Handles single-ticker and multi-ticker yfinance response shapes.
    For any ticker missing from the batch result, fetches it individually so all stocks get data.
    """
    if not ticker_list:
        return pd.DataFrame()

    raw = yf.download(
        ticker_list,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
        group_by="ticker",
        threads=True,
    )

    if raw.empty:
        # Try fetching each ticker individually (often works for indices like ^BSESN)
        series_list = []
        for t in ticker_list:
            s = _fetch_single_ticker(t, start, end)
            if s is not None:
                series_list.append(s)
        if not series_list:
            return pd.DataFrame()
        out = pd.concat(series_list, axis=1)
        out = out.ffill().bfill().dropna(how="all")
        out = out.reindex(columns=[t for t in ticker_list if t in out.columns])
        return out

    # Single ticker: yfinance returns flat columns
    if len(ticker_list) == 1:
        raw.columns = pd.MultiIndex.from_product([[ticker_list[0]], raw.columns])

    out = pd.DataFrame(index=raw.index)
    if isinstance(raw.columns, pd.MultiIndex):
        col_pairs = set(raw.columns)
    for t in ticker_list:
        if isinstance(raw.columns, pd.MultiIndex):
            if (t, "Adj Close") in raw.columns:
                out[t] = raw[(t, "Adj Close")]
            elif (t, "Close") in raw.columns:
                out[t] = raw[(t, "Close")]
            else:
                # Try case-insensitive or alternate level0 match (yfinance sometimes returns different format)
                matched = False
                for (c0, c1) in col_pairs:
                    if c1 in ("Adj Close", "Close") and (str(c0).upper() == str(t).upper() or c0 == t):
                        out[t] = raw[(c0, c1)]
                        matched = True
                        break
                if not matched:
                    continue
        else:
            out[t] = raw["Adj Close"] if "Adj Close" in raw.columns else raw["Close"]

    # Fill any tickers missing from batch by fetching them individually (e.g. ^BSESN)
    missing = [t for t in ticker_list if t not in out.columns]
    for t in missing:
        s = _fetch_single_ticker(t, start, end)
        if s is not None:
            out = out.join(s, how="outer")
            out = out.ffill().bfill()

    out = out.ffill().bfill().dropna(how="all")
    # If we still have no columns (batch structure didn't match), fetch every ticker one-by-one
    if out.columns.empty:
        series_list = []
        for t in ticker_list:
            s = _fetch_single_ticker(t, start, end)
            if s is not None:
                series_list.append(s)
        if series_list:
            out = pd.concat(series_list, axis=1)
            out = out.ffill().bfill().dropna(how="all")

    # Return columns in requested order, only tickers we got data for
    out = out.reindex(columns=[t for t in ticker_list if t in out.columns])
    return out


def validate_tickers(ticker_list):
    """
    Basic validation: non-empty symbols. Does not verify existence on Yahoo.
    Returns (valid_list, invalid_list).
    """
    valid = []
    invalid = []
    for t in ticker_list:
        s = (t or "").strip().upper()
        if s:
            valid.append(s)
        else:
            invalid.append(t)
    return valid, invalid
