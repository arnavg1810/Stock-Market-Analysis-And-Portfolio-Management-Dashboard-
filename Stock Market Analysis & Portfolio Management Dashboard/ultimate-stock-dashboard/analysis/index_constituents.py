"""
Index constituents: Nifty 50, BSE Sensex, S&P 500, Nasdaq 100, Dow Jones.
Builds a single STOCK_OPTIONS dict (label -> ticker) for the app multiselect.
"""
import os
import pandas as pd

# Yahoo Finance uses BRK-B and BF-B; CSV may have BRK.B, BF.B
def _yahoo_symbol(s):
    if s == "BRK.B":
        return "BRK-B"
    if s == "BF.B":
        return "BF-B"
    return s


# --- Nifty 50 (NSE, .NS) - 50 stocks ---
NIFTY_50 = [
    ("Adani Enterprises (Nifty 50)", "ADANIENT.NS"),
    ("Adani Ports (Nifty 50)", "ADANIPORTS.NS"),
    ("Apollo Hospitals (Nifty 50)", "APOLLOHOSP.NS"),
    ("Asian Paints (Nifty 50)", "ASIANPAINT.NS"),
    ("Axis Bank (Nifty 50)", "AXISBANK.NS"),
    ("Bajaj Auto (Nifty 50)", "BAJAJ-AUTO.NS"),
    ("Bajaj Finance (Nifty 50)", "BAJFINANCE.NS"),
    ("Bajaj Finserv (Nifty 50)", "BAJAJFINSV.NS"),
    ("Bharat Electronics (Nifty 50)", "BEL.NS"),
    ("Bharti Airtel (Nifty 50)", "BHARTIARTL.NS"),
    ("Cipla (Nifty 50)", "CIPLA.NS"),
    ("Coal India (Nifty 50)", "COALINDIA.NS"),
    ("Dr. Reddy's (Nifty 50)", "DRREDDY.NS"),
    ("Eicher Motors (Nifty 50)", "EICHERMOT.NS"),
    ("Eternal (Nifty 50)", "ETERNAL.NS"),
    ("Grasim (Nifty 50)", "GRASIM.NS"),
    ("HCL Tech (Nifty 50)", "HCLTECH.NS"),
    ("HDFC Bank (Nifty 50)", "HDFCBANK.NS"),
    ("HDFC Life (Nifty 50)", "HDFCLIFE.NS"),
    ("Hindalco (Nifty 50)", "HINDALCO.NS"),
    ("Hindustan Unilever (Nifty 50)", "HINDUNILVR.NS"),
    ("ICICI Bank (Nifty 50)", "ICICIBANK.NS"),
    ("IndiGo (Nifty 50)", "INDIGO.NS"),
    ("Infosys (Nifty 50)", "INFY.NS"),
    ("ITC (Nifty 50)", "ITC.NS"),
    ("Jio Financial (Nifty 50)", "JIOFIN.NS"),
    ("JSW Steel (Nifty 50)", "JSWSTEEL.NS"),
    ("Kotak Mahindra (Nifty 50)", "KOTAKBANK.NS"),
    ("Larsen & Toubro (Nifty 50)", "LT.NS"),
    ("Mahindra & Mahindra (Nifty 50)", "M&M.NS"),
    ("Maruti Suzuki (Nifty 50)", "MARUTI.NS"),
    ("Max Healthcare (Nifty 50)", "MAXHEALTH.NS"),
    ("Nestlé India (Nifty 50)", "NESTLEIND.NS"),
    ("NTPC (Nifty 50)", "NTPC.NS"),
    ("ONGC (Nifty 50)", "ONGC.NS"),
    ("Power Grid (Nifty 50)", "POWERGRID.NS"),
    ("Reliance (Nifty 50)", "RELIANCE.NS"),
    ("SBI Life (Nifty 50)", "SBILIFE.NS"),
    ("Shriram Finance (Nifty 50)", "SHRIRAMFIN.NS"),
    ("State Bank of India (Nifty 50)", "SBIN.NS"),
    ("Sun Pharma (Nifty 50)", "SUNPHARMA.NS"),
    ("TCS (Nifty 50)", "TCS.NS"),
    ("Tata Consumer (Nifty 50)", "TATACONSUM.NS"),
    ("Tata Motors (Nifty 50)", "TATAMOTORS.NS"),
    ("Tata Steel (Nifty 50)", "TATASTEEL.NS"),
    ("Tech Mahindra (Nifty 50)", "TECHM.NS"),
    ("Titan (Nifty 50)", "TITAN.NS"),
    ("Trent (Nifty 50)", "TRENT.NS"),
    ("UltraTech Cement (Nifty 50)", "ULTRACEMCO.NS"),
    ("Wipro (Nifty 50)", "WIPRO.NS"),
]

# --- BSE Sensex 30 (BSE, .BO) ---
BSE_SENSEX_30 = [
    ("Axis Bank (Sensex)", "AXISBANK.BO"),
    ("Bajaj Finance (Sensex)", "BAJFINANCE.BO"),
    ("Bajaj Finserv (Sensex)", "BAJAJFINSV.BO"),
    ("Bharti Airtel (Sensex)", "BHARTIARTL.BO"),
    ("HCL Tech (Sensex)", "HCLTECH.BO"),
    ("HDFC Bank (Sensex)", "HDFCBANK.BO"),
    ("ICICI Bank (Sensex)", "ICICIBANK.BO"),
    ("IndusInd Bank (Sensex)", "INDUSINDBK.BO"),
    ("Infosys (Sensex)", "INFY.BO"),
    ("ITC (Sensex)", "ITC.BO"),
    ("Kotak Mahindra (Sensex)", "KOTAKBANK.BO"),
    ("Larsen & Toubro (Sensex)", "LT.BO"),
    ("Maruti Suzuki (Sensex)", "MARUTI.BO"),
    ("Nestlé India (Sensex)", "NESTLEIND.BO"),
    ("NTPC (Sensex)", "NTPC.BO"),
    ("Power Grid (Sensex)", "POWERGRID.BO"),
    ("Reliance (Sensex)", "RELIANCE.BO"),
    ("SBI (Sensex)", "SBIN.BO"),
    ("Sun Pharma (Sensex)", "SUNPHARMA.BO"),
    ("TCS (Sensex)", "TCS.BO"),
    ("Tata Motors (Sensex)", "TATAMOTORS.BO"),
    ("Tata Steel (Sensex)", "TATASTEEL.BO"),
    ("Asian Paints (Sensex)", "ASIANPAINT.BO"),
    ("Hindustan Unilever (Sensex)", "HINDUNILVR.BO"),
    ("Adani Ports (Sensex)", "ADANIPORTS.BO"),
    ("JSW Steel (Sensex)", "JSWSTEEL.BO"),
    ("Hindalco (Sensex)", "HINDALCO.BO"),
    ("Wipro (Sensex)", "WIPRO.BO"),
    ("Titan (Sensex)", "TITAN.BO"),
]

# --- Dow Jones Industrial Average (30) ---
DOW_30 = [
    ("3M (Dow)", "MMM"),
    ("American Express (Dow)", "AXP"),
    ("Amgen (Dow)", "AMGN"),
    ("Apple (Dow)", "AAPL"),
    ("Boeing (Dow)", "BA"),
    ("Caterpillar (Dow)", "CAT"),
    ("Chevron (Dow)", "CVX"),
    ("Cisco (Dow)", "CSCO"),
    ("Coca-Cola (Dow)", "KO"),
    ("Disney (Dow)", "DIS"),
    ("Dow Inc. (Dow)", "DOW"),
    ("Goldman Sachs (Dow)", "GS"),
    ("Home Depot (Dow)", "HD"),
    ("Honeywell (Dow)", "HON"),
    ("IBM (Dow)", "IBM"),
    ("Intel (Dow)", "INTC"),
    ("Johnson & Johnson (Dow)", "JNJ"),
    ("JPMorgan Chase (Dow)", "JPM"),
    ("McDonald's (Dow)", "MCD"),
    ("Merck (Dow)", "MRK"),
    ("Microsoft (Dow)", "MSFT"),
    ("Nike (Dow)", "NKE"),
    ("Procter & Gamble (Dow)", "PG"),
    ("Salesforce (Dow)", "CRM"),
    ("Travelers (Dow)", "TRV"),
    ("UnitedHealth (Dow)", "UNH"),
    ("Visa (Dow)", "V"),
    ("Walgreens (Dow)", "WBA"),
    ("Walmart (Dow)", "WMT"),
]

# --- Nasdaq 100 (top constituents, US tickers) ---
NASDAQ_100 = [
    ("Adobe (Nasdaq 100)", "ADBE"),
    ("Advanced Micro Devices (Nasdaq 100)", "AMD"),
    ("Airbnb (Nasdaq 100)", "ABNB"),
    ("Alphabet Class A (Nasdaq 100)", "GOOGL"),
    ("Alphabet Class C (Nasdaq 100)", "GOOG"),
    ("Amazon (Nasdaq 100)", "AMZN"),
    ("Amgen (Nasdaq 100)", "AMGN"),
    ("Analog Devices (Nasdaq 100)", "ADI"),
    ("Apple (Nasdaq 100)", "AAPL"),
    ("Applied Materials (Nasdaq 100)", "AMAT"),
    ("ASML (Nasdaq 100)", "ASML"),
    ("AstraZeneca (Nasdaq 100)", "AZN"),
    ("Autodesk (Nasdaq 100)", "ADSK"),
    ("Broadcom (Nasdaq 100)", "AVGO"),
    ("Cadence (Nasdaq 100)", "CDNS"),
    ("Charter Communications (Nasdaq 100)", "CHTR"),
    ("Cintas (Nasdaq 100)", "CTAS"),
    ("Cisco (Nasdaq 100)", "CSCO"),
    ("Cognizant (Nasdaq 100)", "CTSH"),
    ("Comcast (Nasdaq 100)", "CMCSA"),
    ("Costco (Nasdaq 100)", "COST"),
    ("CrowdStrike (Nasdaq 100)", "CRWD"),
    ("Datadog (Nasdaq 100)", "DDOG"),
    ("Dexcom (Nasdaq 100)", "DXCM"),
    ("Electronic Arts (Nasdaq 100)", "EA"),
    ("Enphase Energy (Nasdaq 100)", "ENPH"),
    ("Exelon (Nasdaq 100)", "EXC"),
    ("Fastenal (Nasdaq 100)", "FAST"),
    ("Fiserv (Nasdaq 100)", "FI"),
    ("Fortinet (Nasdaq 100)", "FTNT"),
    ("Garmin (Nasdaq 100)", "GRMN"),
    ("Gilead (Nasdaq 100)", "GILD"),
    ("Global Payments (Nasdaq 100)", "GPN"),
    ("IDEXX (Nasdaq 100)", "IDXX"),
    ("Illumina (Nasdaq 100)", "ILMN"),
    ("Intuit (Nasdaq 100)", "INTU"),
    ("Intuitive Surgical (Nasdaq 100)", "ISRG"),
    ("Keurig Dr Pepper (Nasdaq 100)", "KDP"),
    ("KLA (Nasdaq 100)", "KLAC"),
    ("Kraft Heinz (Nasdaq 100)", "KHC"),
    ("Lam Research (Nasdaq 100)", "LRCX"),
    ("Lululemon (Nasdaq 100)", "LULU"),
    ("Marriott (Nasdaq 100)", "MAR"),
    ("Marvell (Nasdaq 100)", "MRVL"),
    ("Meta (Nasdaq 100)", "META"),
    ("Microchip (Nasdaq 100)", "MCHP"),
    ("Micron (Nasdaq 100)", "MU"),
    ("Microsoft (Nasdaq 100)", "MSFT"),
    ("Moderna (Nasdaq 100)", "MRNA"),
    ("Mondelēz (Nasdaq 100)", "MDLZ"),
    ("Monster Beverage (Nasdaq 100)", "MNST"),
    ("Netflix (Nasdaq 100)", "NFLX"),
    ("Nvidia (Nasdaq 100)", "NVDA"),
    ("NXP Semiconductors (Nasdaq 100)", "NXPI"),
    ("O'Reilly (Nasdaq 100)", "ORLY"),
    ("Old Dominion (Nasdaq 100)", "ODFL"),
    ("Paccar (Nasdaq 100)", "PCAR"),
    ("Palo Alto Networks (Nasdaq 100)", "PANW"),
    ("Paychex (Nasdaq 100)", "PAYX"),
    ("PepsiCo (Nasdaq 100)", "PEP"),
    ("Pinduoduo (Nasdaq 100)", "PDD"),
    ("Qualcomm (Nasdaq 100)", "QCOM"),
    ("Regeneron (Nasdaq 100)", "REGN"),
    ("Ross Stores (Nasdaq 100)", "ROST"),
    ("Sirius XM (Nasdaq 100)", "SIRI"),
    ("Starbucks (Nasdaq 100)", "SBUX"),
    ("Synopsys (Nasdaq 100)", "SNPS"),
    ("T-Mobile (Nasdaq 100)", "TMUS"),
    ("Tesla (Nasdaq 100)", "TSLA"),
    ("Texas Instruments (Nasdaq 100)", "TXN"),
    ("Vertex (Nasdaq 100)", "VRTX"),
    ("Walgreens (Nasdaq 100)", "WBA"),
    ("Walmart (Nasdaq 100)", "WMT"),
    ("Workday (Nasdaq 100)", "WDAY"),
    ("Xcel Energy (Nasdaq 100)", "XEL"),
    ("Zoom (Nasdaq 100)", "ZM"),
]


def _load_sp500():
    """Load S&P 500 constituents; return list of (label, ticker)."""
    out = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "constituents_sp500.csv")
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.read_csv(url)
        for _, row in df.iterrows():
            sym = _yahoo_symbol(str(row["Symbol"]).strip())
            name = str(row["Security"]).strip()
            out.append((f"{name} (S&P 500)", sym))
    except Exception:
        pass
    return out


def get_all_stock_options():
    """Build full STOCK_OPTIONS dict: label -> ticker. Includes indices as single entries."""
    opts = {}
    # Index ETFs first (so they appear at top when sorted)
    opts["Nifty 50 Index (^NSEI)"] = "^NSEI"
    opts["BSE Sensex Index (^BSESN)"] = "^BSESN"
    opts["S&P 500 Index (^GSPC)"] = "^GSPC"
    opts["Nasdaq Composite (^IXIC)"] = "^IXIC"
    opts["Dow Jones Industrial (^DJI)"] = "^DJI"
    # Nifty 50 stocks
    for label, ticker in NIFTY_50:
        opts[label] = ticker
    # BSE Sensex
    for label, ticker in BSE_SENSEX_30:
        opts[label] = ticker
    # Dow 30
    for label, ticker in DOW_30:
        opts[label] = ticker
    # Nasdaq 100
    for label, ticker in NASDAQ_100:
        opts[label] = ticker
    # S&P 500 (may overwrite same ticker from Dow/Nasdaq with S&P label)
    for label, ticker in _load_sp500():
        opts[label] = ticker
    return opts
