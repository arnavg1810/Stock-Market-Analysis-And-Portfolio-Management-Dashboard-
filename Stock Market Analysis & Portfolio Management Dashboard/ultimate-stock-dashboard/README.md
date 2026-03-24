# 📊 Stock Market Analysis & Portfolio Optimization Dashboard

A production-level financial analytics project that lets you **select any valid stock ticker** (Indian or global), download historical data, analyze trends and risk, compare multiple stocks, and optimize portfolio allocation using Modern Portfolio Theory.

---

## Why This Matters

This project demonstrates the **integration of financial theory (Modern Portfolio Theory, risk metrics, rebalancing)** with **real-world data engineering**, **production-grade UX**, and **interactive visualization**. It shows how to go from raw market data to actionable portfolio insights—the kind of workflow used in quantitative research and portfolio management. 

**Key highlights:**
- 🎨 **Production-ready UI**: Dark mode enforced, professional color scheme, institutional typography
- 📌 **Thoughtful UX**: Badge-style stock display auto-wraps for 10+ stocks, clean 3-column info layout
- 📊 **Quant-style metrics**: Sharpe, Sortino, VaR, Beta, drawdown, covariance—not just returns
- 🏗️ **Modular architecture**: Clean separation of data, risk, portfolio, and visualization layers
- 🚀 **Dual interfaces**: Streamlit app for monitoring + Jupyter notebook for research

---

## 🎯 Project Overview

This project provides:

- **Modular Python package** (`analysis/`) — Clean separation: data loading, risk metrics, portfolio optimization, visualization. Production-ready structure.
- **Structured Jupyter Notebook** — Full financial analysis with dynamic ticker selection: log returns, VaR, covariance, trend, Sharpe/Sortino, Monte Carlo optimization, rebalancing backtest.
- **Interactive Streamlit Web App** — Dashboard with price/MA (golden cross markers), performance summary table, risk–return scatter, rolling Sharpe, drawdown curve, correlation & covariance heatmaps, efficient frontier, sector allocation, optional 30-day forecast.
- **Advanced Risk & Portfolio** — Maximum Sharpe and minimum volatility portfolios; monthly rebalancing backtest vs static weights; Sortino ratio; Historical and Parametric VaR; drawdown visualization.

**Dynamic ticker input**: Use any valid Yahoo Finance symbol (e.g. `RELIANCE.NS`, `TCS.NS`, `^NSEI`, `AAPL`, `^GSPC`).

---

## ✨ Features

- **Dynamic stock selection** — Analyze any valid ticker (NSE, BSE, US, indices). Stocks displayed in **elegant badge-style layout** with automatic wrapping for easy viewing.
- **Configurable history** — 1–10 years; configurable date range (default 5 years).
- **Dark mode** — Production-grade dark theme locked & enforced for professional appearance.
- **Trend analysis** — 50- and 200-day moving averages; **Golden Cross / Death Cross** marked on chart.
- **Returns & risk** — Daily returns (simple or **log returns**), CAGR, annualized return, volatility, max drawdown, **Sortino ratio**, **rolling Sharpe (1Y / 6M)**, **drawdown curve**, Beta vs benchmark.
- **Value at Risk** — **Historical VaR (95%)** and **Parametric VaR (95%)**.
- **Correlation & covariance** — Correlation heatmap and **annualized covariance heatmap** with brief interpretation.
- **Risk–return scatter** — Volatility vs annual return per ticker.
- **Monte Carlo portfolio optimization** — 10,000 random portfolios, efficient frontier, max Sharpe and min volatility weights.
- **Rebalancing backtest** — **Monthly rebalanced** optimized portfolio vs **static (one-time) weights**.
- **Sector allocation** — Weight by sector (from optimized portfolio) when multiple stocks are selected.
- **Simple forecast** — Optional 30-day drift (or ARIMA) forecast for a selected ticker.
- **Streamlit dashboard** — Dark mode enforced, sidebar (tickers, dates, risk-free rate, investment amount, benchmark, log returns, optimization/rebalancing/forecast toggles). **Badge-style stock display** with count, **loading spinners**, **error handling** for invalid tickers, **performance summary table**, **caching** for fast reloads.

---

## 🛠 Technical Concepts Used

- **Data**: `yfinance` for OHLCV; `pandas` for time series and cleaning.
- **Statistics**: Annualized return, volatility (σ√252), **log returns**, correlation, **covariance**, Beta, **VaR**, **Sortino**, **rolling Sharpe**.
- **Optimization**: Random portfolio weights, expected return and volatility from mean/covariance, Sharpe maximization; **monthly rebalancing backtest**.
- **Visualization**: Plotly (Streamlit), correlation and covariance heatmaps, efficient frontier, drawdown curve, risk–return scatter, golden cross markers.

---

## 📐 Financial Concepts Used

- **OHLC & Adjusted Close** — Price series adjusted for splits/dividends.
- **Moving averages** — 50- and 200-day MAs; Golden/Death Cross.
- **Log returns** — ln(P_t / P_{t-1}); mathematically correct for compounding.
- **CAGR & annualized return** — Compound growth and mean daily return scaled to annual.
- **Volatility, maximum drawdown, drawdown curve** — Risk measures.
- **Sharpe ratio** — (Return − risk-free rate) / volatility.
- **Sortino ratio** — (Return − risk-free rate) / downside deviation (only negative returns).
- **VaR (95%)** — Historical and parametric.
- **Beta** — Sensitivity to a chosen benchmark.
- **Modern Portfolio Theory (MPT)** — Efficient frontier, diversification, max Sharpe and min volatility; **rebalancing** (monthly) vs static.

---

## 📁 Project Structure

```
ultimate-stock-dashboard/
├── app.py                     # Streamlit web application (dark mode enforced)
├── .streamlit/
│   └── config.toml            # Streamlit config (dark theme locked, colors, fonts)
├── analysis/                  # Modular analysis package
│   ├── __init__.py
│   ├── data_loader.py         # Load & validate price data (yfinance)
│   ├── risk_metrics.py        # Returns, Sharpe, Sortino, rolling Sharpe, VaR, drawdown, Beta
│   ├── portfolio.py           # Monte Carlo optimization, rebalancing backtest, covariance
│   ├── visualization.py       # Price/MA + crossovers, heatmaps, drawdown, risk–return, efficient frontier
│   ├── sectors.py             # Sector allocation (yfinance info)
│   ├── index_constituents.py  # Pre-built stock catalogs (Nifty 50, S&P 500, etc.)
│   └── forecast.py            # Simple 30-day forecast (drift / ARIMA)
├── notebook_analysis.ipynb    # Full financial analysis (dynamic tickers, standalone)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LINKEDIN_PACKAGE.md        # Resume & LinkedIn content
├── data/                      # Data folder (for exports or local data)
└── assets/                    # Static assets & screenshots
```

---

## 📸 Screenshots

*(Add screenshots here for recruiters who skim visuals. Suggested:)*

| Dashboard overview | Efficient frontier | Growth & drawdown |
|--------------------|--------------------|-------------------|
| *[Screenshot: main dashboard with summary table and charts]* | *[Screenshot: efficient frontier + allocation pie]* | *[Screenshot: growth chart and drawdown curve]* |

To capture: run `streamlit run app.py`, then screenshot the main view, the optimization section, and the growth/drawdown section. Save under `assets/` and link in this table.

---

## 🚀 Installation

1. **Clone or download** the project and go to the folder:

   ```bash
   cd ultimate-stock-dashboard
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶ How to Run

### Jupyter Notebook

1. Open `notebook_analysis.ipynb` in Jupyter or VS Code.
2. Set your tickers at the top (e.g. `tickers = ['RELIANCE.NS', 'TCS.NS', '^NSEI']`).
3. Run all cells. Analysis (data, EDA, trend, returns, log returns, volatility, VaR, covariance, Sharpe, Monte Carlo, growth, interpretation) updates for your selection.

### Streamlit App

```bash
streamlit run app.py
```

The app opens at `localhost:8501` with:

- **Dark theme pre-configured** (enforced in `.streamlit/config.toml` — no manual setup needed)
- **Badge-style stock selection** in sidebar — add any valid Yahoo Finance ticker
- **Four analysis tabs**:
  - 📈 **Market Overview**: KPIs, price/MA chart, risk-return scatter
  - 📊 **Risk Analytics**: Rolling Sharpe, drawdown, correlation, covariance, VaR
  - 📐 **Portfolio Optimization**: Efficient frontier, allocation pie chart, rebalancing backtest
  - 💰 **Investment Growth**: Growth comparison chart, optional 30-day forecast
- Adjust date range, risk-free rate, investment amount, and benchmark in sidebar
- Optionally enable **log returns**, **monthly rebalancing**, **sector allocation**, **30-day forecast**

---

## � UI/UX Features

### Dark Mode (Enforced)

The entire application uses a **production-grade dark theme** locked via `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#58a6ff"         # Accent blue
backgroundColor = "#0d1117"      # GitHub dark background
secondaryBackgroundColor = "#161b22"
textColor = "#e6edf3"            # Light text
```

This ensures a consistent, professional appearance across all views. **No theme switcher** — dark mode only.

### Stock Selection UI

Stocks are displayed in an **elegant badge-style layout** with automatic text wrapping:

```
📌 Selected Stocks (5)
[RELIANCE.NS] [TCS.NS] [INFY.NS] [HDFCBANK.NS] [WIPRO.NS]
```

This scales gracefully from 1 to 50+ stocks without cluttering the UI.

---

## �🌐 Deployment (Live Demo)

You can deploy the Streamlit app for free to:

- **[Streamlit Community Cloud](https://share.streamlit.io/)** — Connect your GitHub repo and deploy.
- **Render / Railway** — Use a `Dockerfile` or buildpack for Python and run `streamlit run app.py`.

After deployment, add your live link here:

- **Live Demo:** `https://your-app-name.streamlit.app` *(replace with your URL)*

This gives recruiters and reviewers a one-click way to try the dashboard without running it locally.

---

## 📌 Example Tickers

| Market   | Examples                          |
|----------|-----------------------------------|
| Indian   | `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS`, `^NSEI`, `^BSESN` |
| US       | `AAPL`, `MSFT`, `GOOGL`, `AMZN`, `^GSPC`, `^IXIC` |
| Benchmark| `^NSEI` (Nifty 50), `^GSPC` (S&P 500) |

Default demo tickers: **RELIANCE.NS**, **TCS.NS**, **^NSEI**.

---

## 📌 Skills Demonstrated

- Financial data ingestion and cleaning (yfinance, pandas).
- Time series analysis: **log returns**, returns, volatility, drawdown, Beta, **VaR**, **Sortino**, **rolling Sharpe**.
- Modern Portfolio Theory, Monte Carlo simulation, **rebalancing backtest**.
- Risk-adjusted metrics and efficient frontier.
- **Modular, production-style code** (analysis package).
- Interactive dashboards (Streamlit) with **caching**, **error handling**, **loading spinners**.
- Reproducible analysis (Jupyter).

---

## 🔮 Future Enhancements

- Factor exposure analysis (market, momentum, size).
- Export of optimized weights and reports (PDF/Excel).
- Authentication and saved user portfolios.

---

## ⚠ Disclaimer

This project is for **educational and research purposes only**. It is not investment advice. Past performance does not guarantee future results. Always do your own research and consider consulting a financial advisor.

---

## 📄 License

Use and modify freely for learning and portfolio projects.
