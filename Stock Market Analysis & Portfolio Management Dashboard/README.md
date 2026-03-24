# 📊 Stock Market Analysis & Portfolio Management Dashboard

A **production-level financial analytics project** that enables dynamic stock selection (Indian and global markets), comprehensive risk analysis, and portfolio optimization using Modern Portfolio Theory.

---

## 🎯 Project Highlights

✅ **Interactive Dashboard**: Streamlit web app with dark mode UI and real-time analytics  
✅ **Dynamic Stock Selection**: Support for any valid Yahoo Finance ticker (NSE, BSE, US indices, etc.)  
✅ **Advanced Risk Metrics**: Sharpe ratio, Sortino ratio, VaR, Beta, max drawdown, rolling metrics  
✅ **Portfolio Optimization**: Monte Carlo simulation (10,000 portfolios) with efficient frontier  
✅ **Rebalancing Strategy**: Monthly rebalanced vs static weights backtest comparison  
✅ **Technical Analysis**: 50/200-day moving averages with golden/death cross detection  
✅ **Comprehensive Visualizations**: Interactive Plotly charts for correlation, covariance, drawdown curves  
✅ **Research Notebook**: Full Jupyter notebook for end-to-end financial analysis  
✅ **Production Ready**: Clean modular architecture, error handling, caching, deployment-ready  

---

## 📁 Project Structure

```
Stock Market Analysis & Portfolio Management Dashboard/
│
└── ultimate-stock-dashboard/           # Main project directory
    ├── app.py                          # Streamlit web application
    ├── notebook_analysis.ipynb         # Jupyter notebook for research
    ├── requirements.txt                # Python dependencies
    ├── README.md                       # Detailed project documentation
    ├── LINKEDIN_PACKAGE.md             # LinkedIn/resume content
    │
    ├── analysis/                       # Core analysis modules (modular package)
    │   ├── __init__.py
    │   ├── data_loader.py              # Yahoo Finance data fetching
    │   ├── risk_metrics.py             # Risk calculations (Sharpe, Sortino, VaR, etc.)
    │   ├── portfolio.py                # Monte Carlo optimization & rebalancing
    │   ├── visualization.py            # Plotly chart generation
    │   ├── forecast.py                 # 30-day price forecasting
    │   ├── sectors.py                  # Sector allocation analysis
    │   └── index_constituents.py       # Pre-built stock catalogs
    │
    ├── .streamlit/
    │   └── config.toml                 # Dark mode theme configuration
    │
    ├── assets/                         # Static assets & screenshots
    └── data/                           # Data exports (optional)
```

---

## 🚀 Quick Start

### 1. **Clone or Download**
```bash
cd ultimate-stock-dashboard
```

### 2. **Set Up Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the Application**

**Option A: Streamlit Web App** (Interactive Dashboard)
```bash
streamlit run app.py
```
- Opens at `localhost:8501`
- Dark mode enforced
- Select any stock ticker, configure analysis parameters, visualize results

**Option B: Jupyter Notebook** (Research & Analysis)
```bash
jupyter notebook notebook_analysis.ipynb
```
- Run cells sequentially for full analysis workflow
- Modify tickers and parameters as needed

---

## 📊 Features Overview

### **Market Overview Tab**
- Real-time stock price with 50/200-day moving averages
- Golden Cross (buy signal) and Death Cross (sell signal) detection
- Key performance indicators (return, volatility, Sharpe ratio)
- Risk-return scatter plot for multi-stock comparison
- Performance summary table

### **Risk Analytics Tab**
- Rolling Sharpe ratio (1-year and 6-month windows)
- Drawdown curve analysis
- Correlation heatmap (color-coded relationships)
- Covariance matrix visualization
- Historical and parametric Value at Risk (VaR 95%)

### **Portfolio Optimization Tab**
- Monte Carlo simulation (10,000 random portfolios)
- Efficient frontier visualization
- Max Sharpe ratio portfolio allocation
- Min volatility portfolio allocation
- Sector allocation pie chart
- Monthly rebalancing backtest vs static weights

### **Investment Growth Tab**
- Growth comparison chart (multiple scenarios)
- Optional 30-day price forecast
- Scenario analysis with different investment amounts

---

## 🔧 Technical Architecture

### **Core Technologies**
- **Data**: `yfinance` (OHLCV data), `pandas`, `numpy`
- **Analysis**: `scipy`, `statsmodels` (ARIMA)
- **Visualization**: `plotly`, `matplotlib`, `seaborn`
- **Web Framework**: `streamlit`

### **Financial Concepts Implemented**
1. **Modern Portfolio Theory** — Random weight generation, mean-variance optimization
2. **Risk Metrics** — Volatility, max drawdown, Sharpe ratio, Sortino ratio, Beta
3. **Value at Risk** — Historical percentile and parametric (normal distribution) methods
4. **Technical Analysis** — Moving averages, crossover detection, trend following
5. **Covariance & Correlation** — Annualized matrices, diversification analysis
6. **Rebalancing Strategy** — Monthly re-optimization vs static allocation backtesting

---

## 📈 Financial Metrics Explained

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **Sharpe Ratio** | (Return - Risk-Free Rate) / Volatility | Higher = better risk-adjusted return |
| **Sortino Ratio** | (Return - Risk-Free Rate) / Downside Dev | Focuses on downside risk only |
| **Beta** | Portfolio sensitivity to benchmark | 1.0 = moves with market, <1 = less volatile |
| **Max Drawdown** | Largest peak-to-trough decline | Lower (closer to 0) = less risky |
| **VaR (95%)** | 5% probability of daily loss exceeding this | Risk exposure quantification |
| **Rolling Sharpe** | Sharpe ratio over rolling window | Tracks changing risk-adjusted performance |

---

## 🎨 UI/UX Design

### **Dark Mode (Enforced)**
- Production-grade GitHub dark theme
- Professional color palette (#0d1117, #161b22, #58a6ff)
- Consistent across all views

### **Responsive Layout**
- Badge-style stock display (auto-wraps for 50+ tickers)
- 3-column KPI layout
- Sidebar with grouped configuration sections
- Tab-based navigation for different analyses

### **Interactive Charts**
- Hover tooltips with detailed information
- Plotly-based interactive visualizations
- Crossover markers on price charts
- Color-coded heatmaps

---

## 📝 Usage Examples

### **Example 1: Analyze Indian Stocks**
1. Select "Nifty 50" from the market dropdown
2. Choose: Reliance, TCS, HDFC Bank, Infosys
3. Set date range: 5 years
4. Click "Run portfolio optimization"
5. View efficient frontier and optimal allocation

### **Example 2: Multi-Market Portfolio**
1. Use "All markets" option
2. Add custom tickers: `AAPL, MSFT, INFY.NS, TCS.NS, ^NSEI`
3. Configure risk-free rate: 6% (India) or 4% (US)
4. Enable "Monthly rebalancing" to see backtest
5. Compare rebalancing vs static strategy

### **Example 3: Risk Analysis Deep Dive**
1. Select 3-5 stocks
2. Go to "Risk Analytics" tab
3. Examine correlation heatmap (identify diversification)
4. Check rolling Sharpe ratio (performance stability)
5. Review drawdown curve (worst-case scenarios)

---

## 🔐 Deployment Options

### **Streamlit Cloud** (Free)
```bash
streamlit run app.py
# Deploy via: https://share.streamlit.io
```

### **Local Hosting**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### **Docker** (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 📊 Sample Output

### **Key Metrics (Example)**
```
Portfolio Analysis (5 stocks over 5 years):
├── Annualized Return: 15.2%
├── Annualized Volatility: 18.5%
├── Sharpe Ratio: 0.82
├── Sortino Ratio: 1.15
├── Max Drawdown: -32.4%
├── Beta vs Nifty 50: 0.92
└── VaR (95%): -2.8% daily
```

### **Efficient Frontier**
- Scatter plot of 10,000 random portfolios
- Red marker: Max Sharpe ratio portfolio
- Yellow marker: Min volatility portfolio
- Curved line: Efficient frontier

---

## 🛠️ Customization & Extension

### **Add New Stocks**
Edit `analysis/index_constituents.py`:
```python
CUSTOM_STOCKS = [
    ("My Stock (Custom)", "TICKER.NS"),
]
```

### **Change Risk-Free Rate**
In Streamlit sidebar → "Risk Configuration" → adjust percentage

### **Extend Metrics**
Add new functions in `analysis/risk_metrics.py` and call from `app.py`

### **Modify Theme**
Edit `.streamlit/config.toml` color values

---

## 🤝 Contributing

Improvements welcome! Ideas:
- Additional risk metrics (Calmar ratio, Omega ratio)
- Real-time data updates
- Multi-portfolio comparison
- Advanced forecasting (GARCH, ML models)
- Mobile-responsive design

---

## 📚 Resources & References

- **Modern Portfolio Theory**: Markowitz, H. (1952)
- **Sharpe Ratio**: Sharpe, W. F. (1966)
- **Value at Risk**: Jorion, P. (2006)
- **Python Finance**: `yfinance` docs, `pandas` documentation
- **Streamlit**: Official documentation & community

---

## 📄 License

This project is open source and available for educational and commercial use.

---

## 👤 Author

**Arnav** — Financial Analytics & Quantitative Research  
📧 Email: arnav@github.com  
🔗 GitHub: https://github.com/arnavg1810  

---

## 🎓 Project Demonstrates

- ✅ **Financial Theory**: Modern Portfolio Theory, risk metrics, optimization
- ✅ **Data Engineering**: yfinance API, pandas data manipulation, time series analysis
- ✅ **Software Engineering**: Modular design, error handling, caching, clean code
- ✅ **Visualization**: Interactive dashboards, professional UX, dark mode
- ✅ **Production Readiness**: Deployment-ready, scalable architecture

---

**Happy analyzing! 📈 Start the app and explore your portfolio today.**
