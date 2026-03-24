"""
Stock Market Analysis & Portfolio Optimization Dashboard
Modular architecture: analysis package for data, risk, portfolio, visualization.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

from analysis.data_loader import load_prices, validate_tickers
from analysis.risk_metrics import (
    compute_returns,
    max_drawdown,
    drawdown_series,
    sharpe_ratio,
    sortino_ratio,
    rolling_sharpe,
    historical_var,
    parametric_var,
    beta_vs_benchmark,
    annualized_return,
    annualized_volatility,
)
from analysis.portfolio import (
    monte_carlo_optimization,
    rebalancing_backtest,
    annualized_covariance,
)
from analysis.visualization import (
    price_ma_chart_with_crossovers,
    correlation_heatmap,
    covariance_heatmap,
    drawdown_curve_chart,
    risk_return_scatter,
    efficient_frontier_chart,
    rolling_sharpe_chart,
)
from analysis.index_constituents import get_all_stock_options, NIFTY_50, BSE_SENSEX_30, DOW_30, NASDAQ_100
from analysis.sectors import get_sector_allocation
from analysis.forecast import simple_forecast

# -----------------------------------------------------------------------------
# Page config & custom theme (distinctive, production-grade frontend)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Portfolio Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Unified Plotly theme (institutional dark)
PLOT_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    font=dict(color="#e6edf3", family="DM Sans, sans-serif"),
    margin=dict(t=40, b=40, l=50, r=30),
)
PLOT_NO_GRID = dict(showgrid=False)

# Custom CSS: nav, section cards, KPI hover, sidebar sections
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');
  :root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --accent: #58a6ff;
    --accent-soft: #388bfd26;
    --text-primary: #e6edf3;
    --text-muted: #8b949e;
    --border: #30363d;
    --success: #3fb950;
    --danger: #f85149;
  }
  .stApp { background: var(--bg-primary); }
  .main .block-container { padding-top: 0; max-width: 1600px; }
  h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: var(--text-primary) !important; }
  p, label { font-family: 'DM Sans', sans-serif !important; color: var(--text-muted) !important; }
  .stMetric label { color: var(--text-muted) !important; font-size: 0.85rem !important; }
  .stMetric [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-family: 'JetBrains Mono', monospace !important; }
  div[data-testid="stSidebar"] { background: var(--bg-secondary); border-right: 1px solid var(--border); }
  div[data-testid="stSidebar"] .stMarkdown { color: var(--text-primary); }
  section[data-testid="stSidebar"] { font-family: 'DM Sans', sans-serif !important; }
  section[data-testid="stSidebar"] label { font-size: 0.85rem !important; }
  .nav-bar {
    background: #161b22;
    padding: 0.7rem 1.2rem;
    border-bottom: 1px solid #30363d;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -1rem -1rem 1rem -1rem;
  }
  .nav-bar span:first-child { font-weight: 600; color: #e6edf3; font-size: 1.1rem; }
  .nav-bar span:last-child { color: #8b949e; font-size: 0.9rem; }
  [data-testid="column"] .stMetric { transition: box-shadow 0.2s ease; border-radius: 8px; padding: 0.4rem; }
  [data-testid="column"] .stMetric:hover { box-shadow: 0 4px 12px rgba(88, 166, 255, 0.12); }
  .stSpinner > div { border-top-color: var(--accent) !important; }
  [data-testid="collapsedControl"] span { font-family: "Material Icons" !important; font-weight: normal !important; font-style: normal !important; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Top navigation bar
# -----------------------------------------------------------------------------
st.markdown("""
<div class="nav-bar">
  <span>📊 Portfolio Intelligence</span>
  <span>Live | Dynamic | Multi-Asset</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar — grouped into sections (settings panel)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Settings")

@st.cache_data(ttl=86400)
def _cached_stock_options():
    return get_all_stock_options()
STOCK_OPTIONS = _cached_stock_options()

# Build label groups for index/market selection
GROUP_LABELS = {
    "All markets": list(STOCK_OPTIONS.keys()),
    "Nifty 50": [label for label, _ in NIFTY_50],
    "BSE Sensex 30": [label for label, _ in BSE_SENSEX_30],
    "S&P 500": [label for label in STOCK_OPTIONS if "(S&P 500)" in label],
    "Nasdaq 100": [label for label, _ in NASDAQ_100],
    "Dow 30": [label for label, _ in DOW_30],
    "Indices only": [label for label in STOCK_OPTIONS if "Index (" in label],
}

st.sidebar.subheader("📌 Market & Stock")
market_choice = st.sidebar.selectbox(
    "Index / Market",
    options=list(GROUP_LABELS.keys()),
    index=0,
    key="market_select",
)
available_labels = GROUP_LABELS.get(market_choice, GROUP_LABELS["All markets"])

selected_labels = st.sidebar.multiselect(
    "Select stocks",
    options=available_labels,
    default=[l for l in available_labels if l in ["Reliance (Nifty 50)", "TCS (Nifty 50)", "Nifty 50 Index (^NSEI)"]],
    key="stock_multiselect",
)

tickers_from_select = [STOCK_OPTIONS[l] for l in selected_labels]
custom_input = st.sidebar.text_input(
    "Or add custom tickers (comma-separated)",
    value="",
    placeholder="e.g. AXISBANK.NS, HCLTECH.NS",
    help="Any valid Yahoo Finance symbol.",
)
tickers_from_custom = [t.strip().upper() for t in custom_input.split(",") if t.strip()]
tickers_raw = list(dict.fromkeys(tickers_from_select + tickers_from_custom))
tickers, invalid = validate_tickers(tickers_raw)
if invalid:
    st.sidebar.warning(f"Skipped invalid/empty: {invalid}")
if not tickers:
    st.sidebar.error("Select at least one stock above or enter a custom ticker.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Time Range")
years_back = st.sidebar.slider("Years of history", 1, 10, 5)
_end = datetime.now()
_start = _end - timedelta(days=years_back * 365)
start_d = st.sidebar.date_input("Start date", _start.date(), max_value=_end.date())
end_d = st.sidebar.date_input("End date", _end.date(), min_value=start_d)
start_date = datetime.combine(start_d, datetime.min.time())
end_date = datetime.combine(end_d, datetime.min.time())

st.sidebar.markdown("---")
st.sidebar.subheader("⚖ Risk Configuration")
risk_free_rate = st.sidebar.number_input("Risk-free rate (annual %)", 0.0, 15.0, 6.0, 0.5) / 100
investment_amount = st.sidebar.number_input("Investment amount (₹ or $)", 1000, 10_000_000, 10_000, 1000)
benchmark_ticker = st.sidebar.text_input(
    "Benchmark ticker (optional, for Beta)",
    value=tickers[-1] if tickers else "",
    help="Leave blank to use last selected ticker.",
).strip().upper()
if not benchmark_ticker and tickers:
    benchmark_ticker = tickers[-1]

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Chart options")
use_log_scale = st.sidebar.checkbox("Use log scale for charts", value=False, key="log_scale")

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Advanced Options")
with st.sidebar.expander("Options", expanded=False):
    use_log_returns = st.checkbox("Use log returns (quant-style)", value=False, key="log_ret")
    run_optimization = st.checkbox("Run portfolio optimization (Monte Carlo)", value=True, key="opt")
    show_rebalancing = st.checkbox("Show rebalancing backtest (monthly)", value=True, key="rebal")
    show_forecast = st.checkbox("Show 30-day simple forecast", value=False, key="forecast")
    show_sector_allocation = st.checkbox("Show sector allocation", value=True, key="sector")

# Display selected stocks in a neat badge-style layout
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns([2, 2, 1.5])
with col_info1:
    st.markdown(f"**📌 Selected Stocks ({len(tickers)})**")
    # Create badge-style display with text wrapping
    badge_html = ""
    for i, t in enumerate(tickers):
        badge_html += f'<span style="display:inline-block;background:#388bfd26;border:1px solid #58a6ff;border-radius:6px;padding:4px 10px;margin:4px 4px 4px 0;font-size:0.85rem;color:#e6edf3;font-family:monospace">{t}</span>'
    st.markdown(badge_html, unsafe_allow_html=True)
with col_info2:
    st.markdown("**📅 Time Range**")
    st.caption(f"{start_date.date()} → {end_date.date()}")
with col_info3:
    st.markdown("**⚙️ Returns Mode**")
    st.caption("Log returns" if use_log_returns else "Simple returns")

# -----------------------------------------------------------------------------
# Cached heavy computations (hashable args for cache keys)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def cached_load_prices(ticker_list, start, end):
    """Price download — cache by (tickers, start, end)."""
    return load_prices(list(ticker_list), start, end)


@st.cache_data(ttl=3600)
def cached_rolling_sharpe(_daily_returns, window_days, risk_free_rate, periods_per_year=252):
    """Rolling Sharpe — cache by (returns, window, rf)."""
    return rolling_sharpe(_daily_returns, window_days, risk_free_rate, periods_per_year)


def cached_monte_carlo(_ret_data, risk_free_rate, seed=42):
    """Portfolio optimization — fresh run each time for current selection."""
    return monte_carlo_optimization(_ret_data, risk_free_rate, n_portfolios=10000, seed=seed)


def cached_rebalancing_backtest(_ret_data, risk_free_rate, rebalance_freq="M", n_trials_per_period=2000, seed=42):
    """Rebalancing backtest — fresh run each time for current selection."""
    return rebalancing_backtest(_ret_data, risk_free_rate, rebalance_freq, n_trials_per_period, seed)


# -----------------------------------------------------------------------------
# Data loading (cached, with error handling)
# -----------------------------------------------------------------------------
with st.spinner("Fetching market data…"):
    try:
        df = cached_load_prices(tuple(tickers), start_date, end_date)
    except Exception as e:
        st.error(f"Could not load data for the given tickers. Please check symbols and date range. Error: {e}")
        st.stop()

if df.empty or len(df) < 30:
    st.error("Not enough data for the selected tickers/range. Check ticker symbols and dates.")
    st.stop()

# -----------------------------------------------------------------------------
# Session state: reuse computed data when inputs unchanged (fewer re-renders)
# -----------------------------------------------------------------------------
_data_key = (tuple(tickers), start_date, end_date, use_log_returns, risk_free_rate)
if "_data_key" not in st.session_state or st.session_state._data_key != _data_key:
    st.session_state._data_key = _data_key

# -----------------------------------------------------------------------------
# Returns & risk metrics (compute returns from current df so columns always match)
# -----------------------------------------------------------------------------
daily_returns = compute_returns(df, use_log_returns=use_log_returns)
# Use only columns present in both (avoids KeyError; with non-cached returns they match df)
valid_cols = [c for c in df.columns if c in daily_returns.columns]
if not valid_cols:
    st.error("No valid return data for the selected tickers/range. Try fewer tickers, a shorter range, or check your connection.")
    st.stop()
df = df[valid_cols]
daily_returns = daily_returns[valid_cols]
_skipped = [t for t in tickers if t not in valid_cols]
if _skipped:
    st.sidebar.warning(f"No data for: {', '.join(_skipped)}. Showing the rest.")

n_years = (df.index[-1] - df.index[0]).days / 365.0
periods_per_year = 252

ann_ret = daily_returns.apply(annualized_return, periods_per_year=periods_per_year)
vol_annual = daily_returns.apply(annualized_volatility, periods_per_year=periods_per_year)
cagr = (df.iloc[-1] / df.iloc[0]) ** (1 / n_years) - 1

max_dd = {t: max_drawdown(daily_returns[t]) for t in valid_cols}
sharpe = pd.Series({t: sharpe_ratio(ann_ret[t], vol_annual[t], risk_free_rate) for t in valid_cols})
sortino = pd.Series({t: sortino_ratio(daily_returns[t], risk_free_rate, periods_per_year) for t in valid_cols})

beta = beta_vs_benchmark(daily_returns, benchmark_ticker)

# Rolling Sharpe (252 = 1Y, 126 = 6M) — cached
rolling_sharpe_1y = cached_rolling_sharpe(daily_returns, 252, risk_free_rate, periods_per_year)
rolling_sharpe_6m = cached_rolling_sharpe(daily_returns, 126, risk_free_rate, periods_per_year)

# VaR 95%
var_hist = pd.Series({t: historical_var(daily_returns[t], 0.95) for t in valid_cols})
var_param = pd.Series({t: parametric_var(daily_returns[t], 0.95) for t in valid_cols})

# Drawdown series for chart
drawdown_df = pd.DataFrame({t: drawdown_series(daily_returns[t]) for t in valid_cols})

# Build summary dataframe for expander
summary_df = pd.DataFrame({
    "CAGR": cagr,
    "Ann. Return": ann_ret,
    "Volatility": vol_annual,
    "Sharpe": sharpe,
    "Sortino": sortino,
    "Max Drawdown": pd.Series(max_dd),
    "VaR (95%, Hist.)": var_hist,
    "VaR (95%, Param.)": var_param,
})
if benchmark_ticker and benchmark_ticker in beta.index:
    summary_df["Beta"] = beta
fmt_dict = {
    "CAGR": "{:.2%}", "Ann. Return": "{:.2%}", "Volatility": "{:.2%}",
    "Sharpe": "{:.2f}", "Sortino": "{:.2f}", "Max Drawdown": "{:.2%}",
    "VaR (95%, Hist.)": "{:.2%}", "VaR (95%, Param.)": "{:.2%}",
}
if "Beta" in summary_df.columns:
    fmt_dict["Beta"] = "{:.2f}"

# Precompute for optimization tab — Monte Carlo only when tickers/date/rf change (cached)
# Use all available tickers (whatever the user selected) for optimization
opt_tickers = list(valid_cols)
ret_data = daily_returns[opt_tickers].dropna()
max_sharpe_port = min_vol_port = portfolios_df = None
opt_tickers_used = []  # tickers actually present in optimization result (avoids KeyError if cache/columns differ)
if run_optimization and len(opt_tickers) >= 2:
    with st.spinner("Running Monte Carlo optimization…"):
        portfolios_df, max_sharpe_port, min_vol_port = cached_monte_carlo(ret_data, risk_free_rate, seed=42)
    if max_sharpe_port is not None:
        opt_tickers_used = [c for c in max_sharpe_port.index if c not in ("Return", "Volatility", "Sharpe")]

rolling_vol = daily_returns.rolling(30).std() * np.sqrt(252)
corr = daily_returns.corr()
cov_ann = annualized_covariance(daily_returns, periods_per_year)
mom_12m = (df / df.shift(252) - 1).iloc[-1] if len(df) >= 252 else pd.Series(dtype=float)
factor_df = pd.DataFrame({"Beta (vs benchmark)": beta, "12M Momentum": mom_12m}).dropna(how="all")

# -----------------------------------------------------------------------------
# Main content: Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Market Overview",
    "📊 Risk Analytics",
    "📐 Portfolio Optimization",
    "💰 Investment Growth",
])

with tab1:
    # Executive KPI row (5 premium cards)
    st.subheader("Executive summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        best_cagr = cagr.max()
        st.metric("Best CAGR", f"{best_cagr:.2%}", delta=f"vs Rf {risk_free_rate:.1%}", delta_color="off")
    with c2:
        best_sharpe_val = sharpe.max()
        st.metric("Highest Sharpe", f"{best_sharpe_val:.2f}", delta=f"vs 1.0: {best_sharpe_val - 1.0:+.2f}" if not np.isnan(best_sharpe_val) else None, delta_color="normal")
    with c3:
        min_vol_ticker = vol_annual.idxmin()
        st.metric("Lowest Volatility", min_vol_ticker, delta=f"{vol_annual.min():.2%}", delta_color="inverse")
    with c4:
        deepest_dd = min(max_dd.values())
        st.metric("Deepest Drawdown", f"{deepest_dd:.2%}", delta="worst peak-to-trough", delta_color="inverse")
    with c5:
        top_ticker = cagr.idxmax()
        st.metric("Top Performer", top_ticker, delta=f"{cagr.max():.2%}", delta_color="off")
    st.markdown("---")
    st.subheader("📊 Full performance table (all tickers)")
    st.dataframe(summary_df.style.format({k: v for k, v in fmt_dict.items() if k in summary_df.columns}), use_container_width=True)

    st.subheader("📈 Price & Moving Averages (50 & 200 MA)")
    selected_ticker = st.selectbox("Select ticker for price chart", df.columns.tolist(), key="price_ticker")
    ma50 = df[selected_ticker].rolling(50).mean()
    ma200 = df[selected_ticker].rolling(200).mean()
    fig_price = price_ma_chart_with_crossovers(df[selected_ticker], ma50, ma200, selected_ticker)
    fig_price.update_layout(**PLOT_THEME, height=400)
    fig_price.update_xaxes(**PLOT_NO_GRID)
    # Price is strictly positive, so log scale is always meaningful when enabled
    if use_log_scale:
        fig_price.update_yaxes(**PLOT_NO_GRID, type="log")
    else:
        fig_price.update_yaxes(**PLOT_NO_GRID)
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("📉 Risk vs Return")
    fig_rr = risk_return_scatter(ann_ret, vol_annual, list(df.columns), title="Annual Return vs Volatility")
    fig_rr.update_layout(**PLOT_THEME, height=400)
    fig_rr.update_xaxes(**PLOT_NO_GRID)
    # Use log scale on volatility axis (x); returns may be negative
    if use_log_scale:
        fig_rr.update_xaxes(**PLOT_NO_GRID, type="log")
    else:
        fig_rr.update_yaxes(**PLOT_NO_GRID)
    st.plotly_chart(fig_rr, use_container_width=True)

with tab2:
    st.subheader("📈 Rolling Sharpe Ratio")
    rs_window = st.radio("Rolling window", ["1 year (252d)", "6 months (126d)"], horizontal=True, key="rs_window")
    window = 252 if "1 year" in rs_window else 126
    rs_df = rolling_sharpe_1y if window == 252 else rolling_sharpe_6m
    fig_rs = rolling_sharpe_chart(rs_df, title=f"Rolling {window}-Day Sharpe Ratio")
    fig_rs.update_layout(**PLOT_THEME, height=350)
    fig_rs.update_xaxes(**PLOT_NO_GRID)
    fig_rs.update_yaxes(**PLOT_NO_GRID)
    # Rolling Sharpe can be negative — keep linear scale
    st.plotly_chart(fig_rs, use_container_width=True)

    st.subheader("📉 Drawdown over time")
    fig_dd = drawdown_curve_chart(drawdown_df, title="Drawdown curve")
    fig_dd.update_layout(**PLOT_THEME, height=350)
    fig_dd.update_xaxes(**PLOT_NO_GRID)
    fig_dd.update_yaxes(**PLOT_NO_GRID)
    # Drawdown is negative — log scale not meaningful; keep linear
    st.plotly_chart(fig_dd, use_container_width=True)

    st.subheader("📉 Rolling 30-Day Volatility (Annualized)")
    fig_vol = go.Figure()
    for t in df.columns:
        fig_vol.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol[t], name=t, mode="lines"))
    fig_vol.update_layout(**PLOT_THEME, height=350, xaxis_title="Date", yaxis_title="Volatility (ann.)", legend=dict(orientation="h"))
    fig_vol.update_xaxes(**PLOT_NO_GRID)
    # Volatility is non‑negative; log scale is safe when enabled
    if use_log_scale:
        fig_vol.update_yaxes(**PLOT_NO_GRID, type="log")
    else:
        fig_vol.update_yaxes(**PLOT_NO_GRID)
    st.plotly_chart(fig_vol, use_container_width=True)

    # VaR as small metrics
    st.subheader("Value at Risk (95%)")
    v1, v2, v3 = st.columns(3)
    with v1:
        st.metric("Worst Historical VaR", f"{var_hist.min():.2%}", delta="across tickers", delta_color="inverse")
    with v2:
        st.metric("Worst Parametric VaR", f"{var_param.min():.2%}", delta="normal assumption", delta_color="inverse")
    with v3:
        st.caption("Daily loss level not exceeded with 95% probability.")

    st.subheader("📊 Correlation heatmap")
    fig_corr = correlation_heatmap(corr, title="Correlation of daily returns")
    fig_corr.update_layout(**PLOT_THEME, height=400)
    fig_corr.update_xaxes(**PLOT_NO_GRID)
    fig_corr.update_yaxes(**PLOT_NO_GRID)
    st.plotly_chart(fig_corr, use_container_width=True)

    with st.expander("📊 Advanced statistical details"):
        st.write("**Covariance matrix (annualized)**")
        fig_cov = covariance_heatmap(cov_ann, title="Covariance × 252")
        fig_cov.update_layout(**PLOT_THEME, height=400)
        fig_cov.update_xaxes(**PLOT_NO_GRID)
        fig_cov.update_yaxes(**PLOT_NO_GRID)
        st.plotly_chart(fig_cov, use_container_width=True)
        st.caption("Diagonal = variances; off-diagonal = covariances.")
        if not factor_df.empty:
            st.write("**Factor-style: Beta & 12M Momentum**")
            st.dataframe(factor_df.style.format("{:.2f}"), use_container_width=True)

with tab3:
    if run_optimization and len(opt_tickers) >= 2 and max_sharpe_port is not None and opt_tickers_used:
        st.markdown("### Recommended allocation based on maximum risk-adjusted return")
        # 3 large metric cards before the pie
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Portfolio Sharpe", f"{max_sharpe_port['Sharpe']:.2f}", delta="risk-adjusted return", delta_color="normal")
        with m2:
            st.metric("Expected return", f"{max_sharpe_port['Return']:.2%}", delta="annualized", delta_color="off")
        with m3:
            st.metric("Portfolio volatility", f"{max_sharpe_port['Volatility']:.2%}", delta="annualized", delta_color="inverse")
        st.markdown("---")
        col_ef, col_pie = st.columns(2)
        with col_ef:
            st.subheader("Efficient frontier")
            fig_ef = efficient_frontier_chart(portfolios_df, max_sharpe_port, min_vol_port, opt_tickers_used)
            fig_ef.update_layout(**PLOT_THEME, height=400)
            # Log scale on x (volatility); returns may be negative
            if use_log_scale:
                fig_ef.update_xaxes(**PLOT_NO_GRID, type="log")
            else:
                fig_ef.update_xaxes(**PLOT_NO_GRID)
            st.plotly_chart(fig_ef, use_container_width=True)
        with col_pie:
            st.subheader("Optimal allocation (Max Sharpe)")
            weights = max_sharpe_port[opt_tickers_used]
            fig_pie = go.Figure(data=[go.Pie(labels=opt_tickers_used, values=weights, hole=0.4)])
            fig_pie.update_layout(**PLOT_THEME, height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

        w_col1, w_col2 = st.columns(2)
        with w_col1:
            st.subheader("Max Sharpe portfolio")
            for t in opt_tickers_used:
                st.write(f"- **{t}**: {max_sharpe_port[t]:.1%}")
        with w_col2:
            st.subheader("Min volatility portfolio")
            for t in opt_tickers_used:
                st.write(f"- **{t}**: {min_vol_port[t]:.1%}")

        if show_rebalancing and len(ret_data) >= 252:
            st.subheader("📅 Rebalancing backtest: monthly vs static")
            try:
                rebal_curve, static_curve, _ = cached_rebalancing_backtest(
                    ret_data, risk_free_rate, rebalance_freq="M", n_trials_per_period=2000, seed=42
                )
                reb_df = pd.DataFrame({"Monthly rebalanced": rebal_curve, "Static (one-time)": static_curve})
                fig_reb = go.Figure()
                for col in reb_df.columns:
                    fig_reb.add_trace(go.Scatter(x=reb_df.index, y=reb_df[col], name=col, mode="lines"))
                fig_reb.update_layout(**PLOT_THEME, height=400, xaxis_title="Date", yaxis_title="Cumulative growth (1 = 100%)")
                fig_reb.update_xaxes(**PLOT_NO_GRID)
                _reb_min = reb_df.min().min()
                if use_log_scale and pd.notna(_reb_min) and _reb_min > 1e-10:
                    fig_reb.update_yaxes(**PLOT_NO_GRID, type="log")
                else:
                    fig_reb.update_yaxes(**PLOT_NO_GRID)
                st.plotly_chart(fig_reb, use_container_width=True)
            except Exception as ex:
                st.warning(f"Rebalancing backtest skipped: {ex}")

        if show_sector_allocation:
            try:
                weights_series = max_sharpe_port[opt_tickers_used]
                sector_alloc = get_sector_allocation(opt_tickers_used, weights_series)
                if not sector_alloc.empty:
                    fig_sec = go.Figure(data=[go.Pie(labels=sector_alloc.index, values=sector_alloc.values, hole=0.4)])
                    fig_sec.update_layout(**PLOT_THEME, height=350, title="Weight by sector")
                    st.plotly_chart(fig_sec, use_container_width=True)
            except Exception:
                pass
    else:
        st.info("Enable **Run portfolio optimization** in Advanced Options and select at least 2 tickers to see this tab.")

with tab4:
    # Growth comparison
    if run_optimization and len(opt_tickers) >= 2:
        ret_data_g = daily_returns[opt_tickers].dropna()
        mean_ret_g = ret_data_g.mean() * 252
        cov_g = ret_data_g.cov() * 252
        best_sharpe = -np.inf
        best_w = None
        np.random.seed(42)
        for _ in range(5000):
            w = np.random.random(len(opt_tickers))
            w /= w.sum()
            r = np.dot(w, mean_ret_g)
            v = np.sqrt(np.dot(w.T, np.dot(cov_g, w)))
            if v > 0 and (r - risk_free_rate) / v > best_sharpe:
                best_sharpe = (r - risk_free_rate) / v
                best_w = w
        if best_w is not None:
            port_ret_series = (daily_returns[opt_tickers] * best_w).sum(axis=1)
            growth_port = investment_amount * (1 + port_ret_series).cumprod()
            growth_port.name = "Optimized Portfolio"
        else:
            growth_port = None
    else:
        growth_port = None

    cum = (1 + daily_returns).cumprod()
    growth_df = investment_amount * cum
    if growth_port is not None:
        growth_df = growth_df.copy()
        growth_df["Optimized Portfolio"] = growth_port
    st.subheader("💰 Investment growth comparison")
    fig_growth = go.Figure()
    for col in growth_df.columns:
        fig_growth.add_trace(go.Scatter(x=growth_df.index, y=growth_df[col], name=col, mode="lines"))
    fig_growth.add_hline(y=investment_amount, line_dash="dash", line_color="gray")
    fig_growth.update_layout(
        **PLOT_THEME,
        height=450,
        xaxis_title="Date",
        yaxis_title="Portfolio value",
        title=f"Growth of {investment_amount:,} invested at start",
        legend=dict(orientation="h"),
    )
    fig_growth.update_xaxes(**PLOT_NO_GRID)
    # Portfolio values are positive; log scale is meaningful when enabled
    if use_log_scale:
        fig_growth.update_yaxes(**PLOT_NO_GRID, type="log")
    else:
        fig_growth.update_yaxes(**PLOT_NO_GRID)
    st.plotly_chart(fig_growth, use_container_width=True)

    if show_forecast:
        st.subheader("🔮 30-day simple forecast")
        fc_ticker = st.selectbox("Select ticker for forecast", df.columns.tolist(), key="fc_ticker")
        f_dates, f_values = simple_forecast(df[fc_ticker], horizon_days=30, method="drift")
        if f_dates is not None and f_values is not None:
            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(x=df.index, y=df[fc_ticker], name="History", mode="lines"))
            fig_fc.add_trace(go.Scatter(x=f_dates, y=f_values, name="Forecast (drift)", mode="lines+markers", line=dict(dash="dash")))
            fig_fc.update_layout(**PLOT_THEME, height=400, xaxis_title="Date", yaxis_title="Price", title=f"Price & 30-day forecast — {fc_ticker}")
            fig_fc.update_xaxes(**PLOT_NO_GRID)
            if use_log_scale:
                fig_fc.update_yaxes(**PLOT_NO_GRID, type="log")
            else:
                fig_fc.update_yaxes(**PLOT_NO_GRID)
            st.plotly_chart(fig_fc, use_container_width=True)
        else:
            st.caption("Forecast not available (need enough history).")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<small style="color:#8b949e">
Built by Arnav Gupta • Modern Portfolio Theory • Monte Carlo Simulation • Python • Streamlit  
Data source: Yahoo Finance  
For educational and analytical use only.
</small>
""", unsafe_allow_html=True)

st.sidebar.success("Dashboard ready. Change tickers or settings to refresh.")
