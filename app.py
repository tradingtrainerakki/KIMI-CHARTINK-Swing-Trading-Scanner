import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# ─── Page Config ───
st.set_page_config(page_title="SMC Swing Screener", layout="wide")

# ─── AUTH ───
USERS = {"akki": "Ca@1809"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("## 📊 SMC Swing Screener — Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(u) == p:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Galat username/password")
    st.stop()

st.title("📊 SMC Swing Screener — Nifty 200")
st.caption("RSI 30-45 | Pullback in Uptrend | Volume Spike | Market Cap > 10K Cr")
if st.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# ─── Full Nifty 200 Stock List (Yahoo Finance Tickers) ───
NIFTY_200 = [
    # ─── Nifty 100 (Large Cap) ───
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
    "BHARTIARTL.NS", "ITC.NS", "SBIN.NS", "LICI.NS", "HINDUNILVR.NS",
    "LT.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "AXISBANK.NS", "ASIANPAINT.NS",
    "MARUTI.NS", "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "NESTLEIND.NS",
    "WIPRO.NS", "ADANIENT.NS", "COALINDIA.NS", "POWERGRID.NS", "NTPC.NS",
    "TATAMOTORS.NS", "M&M.NS", "HCLTECH.NS", "TECHM.NS", "BAJAJFINSV.NS",
    "INDUSINDBK.NS", "JSWSTEEL.NS", "ONGC.NS", "GRASIM.NS", "CIPLA.NS",
    "DRREDDY.NS", "BRITANNIA.NS", "TATACONSUM.NS", "EICHERMOT.NS", "APOLLOHOSP.NS",
    "DIVISLAB.NS", "SBILIFE.NS", "HDFCLIFE.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS",
    "TATASTEEL.NS", "HINDALCO.NS", "VEDL.NS", "ADANIPORTS.NS", "DMART.NS",
    "BPCL.NS", "IOC.NS", "GAIL.NS", "PIDILITIND.NS", "HAVELLS.NS",
    "DABUR.NS", "MARICO.NS", "COLPAL.NS", "GODREJCP.NS", "GODREJPROP.NS",
    "DLF.NS", "OBEROIRLTY.NS", "ABB.NS", "SIEMENS.NS", "HAL.NS",
    "BEL.NS", "BHEL.NS", "ABBOTINDIA.NS", "ALKEM.NS", "AUROPHARMA.NS",
    "BIOCON.NS", "LUPIN.NS", "TORNTPHARM.NS", "ZYDUSLIFE.NS", "JINDALSTEL.NS",
    "APLAPOLLO.NS", "AUBANK.NS", "BANDHANBNK.NS", "CANBK.NS", "FEDERALBNK.NS",
    "IDFCFIRSTB.NS", "PNB.NS", "UNIONBANK.NS", "BANKBARODA.NS", "CHOLAFIN.NS",
    "MUTHOOTFIN.NS", "PFC.NS", "RECLTD.NS", "SHRIRAMFIN.NS", "BAJAJHLDNG.NS",
    "LICHSGFIN.NS", "MANAPPURAM.NS", "ABCAPITAL.NS", "SRF.NS", "DEEPAKNTR.NS",
    "ATUL.NS", "UPL.NS", "TATACHEM.NS", "COROMANDEL.NS", "PIIND.NS",

    # ─── Nifty Midcap 100 (Remaining for Nifty 200) ───
    "ADANIGREEN.NS", "TRENT.NS", "BOSCHLTD.NS", "MRF.NS", "PAGEIND.NS",
    "SHREECEM.NS", "3MINDIA.NS", "GLAND.NS", "SANOFI.NS", "PFIZER.NS",
    "ASTRAZEN.NS", "MERCK.NS", "BLUEDART.NS", "CASTROLIND.NS", "EXIDEIND.NS",
    "AMARAJABAT.NS", "MOTHERSON.NS", "BHARATFORG.NS", "APLTYRE.NS", "CEATLTD.NS",
    "BALKRISIND.NS", "SKFINDIA.NS", "SCHAEFFLER.NS", "TIMKEN.NS", "CARBORUNIV.NS",
    "GRINDWELL.NS", "SUPREMEIND.NS", "ASTRAL.NS", "PRINCEPIPE.NS", "FINPIPE.NS",
    "KEI.NS", "POLYCAB.NS", "HONEYWELL.NS", "L&TTS.NS", "BSOFT.NS",
    "CYIENT.NS", "INTELLECT.NS", "ZENSARTECH.NS", "SONATSOFTW.NS", "FIRSTSOURCE.NS",
    "FSL.NS", "KPITTECH.NS", "TATAELXSI.NS", "ORACLEFIN.NS", "IIFL.NS",
    "MOTILALOFS.NS", "ANGELONE.NS", "ICICISEC.NS", "HDFCAMC.NS", "NAM-INDIA.NS",
    "UTIAMC.NS", "CAMS.NS", "CDSL.NS", "MCX.NS", "IEX.NS",
    "BSE.NS", "IRB.NS", "KNRCON.NS", "PNCINFRA.NS", "GMRINFRA.NS",
    "SUZLON.NS", "CGPOWER.NS", "THERMAX.NS", "KIRLOSENG.NS", "CUMMINSIND.NS",
    "GREAVESCOT.NS", "KECINT.NS", "VGUARD.NS", "FINOLEXIND.NS", "BATAINDIA.NS",
    "RELAXO.NS", "RAJESHEXPO.NS", "TITAGARH.NS", "BEML.NS", "COCHINSHIP.NS",
    "MAZDOCK.NS", "GRSE.NS", "PARADEEP.NS", "FACT.NS", "NLCINDIA.NS",
    "NMDC.NS", "MOIL.NS", "HINDCOPPER.NS", "NATIONALUM.NS", "ELGIEQUIP.NS",
    "PHOENIXLTD.NS", "PRESTIGE.NS", "SOBHA.NS", "BRIGADE.NS", "MAHLIFE.NS",
    "ANANTRAJ.NS", "ASHIANA.NS", "SUNTECK.NS", "NCC.NS", "ASHOKLEY.NS",
    "TIINDIA.NS", "SUNDARMFIN.NS", "RAMCOCEM.NS", "INDIGOPNTS.NS", "JUBLFOOD.NS",
    "ZOMATO.NS", "NYKAA.NS", "POLICYBZR.NS", "PAYTM.NS", "DEVYANI.NS",
    "WESTLIFE.NS", "KPRMILL.NS", "WELSPUNIND.NS", "TRIDENT.NS", "RAYMOND.NS",
    "GESHIP.NS", "SCI.NS", "KALYANKJIL.NS", "TANLA.NS", "ROUTE.NS",
    "AFFLE.NS", "INDIAMART.NS", "JUSTDIAL.NS", "CARTRADE.NS", "EASEMYTRIP.NS",
    "COCHINSHIP.NS", "RBLBANK.NS", "CANFINHOME.NS", "REPCOHOME.NS", "PEL.NS",
    "IDBI.NS", "BANKINDIA.NS", "INDIANB.NS", "MAHABANK.NS", "IOB.NS",
    "UCOBANK.NS", "CENTRALBK.NS", "KARURVYSYA.NS", "SOUTHBANK.NS", "TMB.NS",
    "CUB.NS", "DCBBANK.NS", "J&KBANK.NS", "CSBBANK.NS", "EQUITASBNK.NS",
    "UJJIVANSFB.NS", "MIDHANI.NS", "MSTC.NS", "NBCC.NS", "RAILTEL.NS",
    "RVNL.NS", "IRCON.NS", "SJVN.NS", "PTCINDIA.NS",
    "JSWENERGY.NS", "TORRENTPOWER.NS", "CESC.NS", "LAXMIMACH.NS", "TTKPRESTIG.NS",
    "HAWKINS.NS", "STOVEKRAFT.NS", "NAVA.NS", "RCF.NS", "GSFC.NS",
    "MFL.NS", "SUMICHEM.NS", "BAYERCROP.NS", "RALLIS.NS", "DHANUKA.NS",
    "INSECTICID.NS", "SHARDACROP.NS", "BASF.NS", "TATVA.NS", "CLEAN.NS",
    "NAVINFLUOR.NS", "VINATIORGA.NS", "ALKYLAMINE.NS", "BALAMINES.NS"
]

# ─── Manual Indicator Calculations (pandas_ta hata diya — purana/unmaintained
# library hai jo naye Python versions par install hi fail ho jaati hai.
# RSI aur SMA seedhe pandas se calculate karna zyada bharosemand hai) ──
def calc_rsi(close, length=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calc_sma(close, length):
    return close.rolling(length).mean()

# ─── Sidebar Filters ───
st.sidebar.header("⚙️ Filters")

rsi_min = st.sidebar.slider("RSI Min", 20, 40, 30)
rsi_max = st.sidebar.slider("RSI Max", 35, 60, 45)
mcap_min = st.sidebar.number_input("Market Cap Min (Cr)", value=10000, step=1000)
price_min = st.sidebar.number_input("Min Price (₹)", value=100, step=10)
volume_mult = st.sidebar.slider("Volume Multiplier", 1.0, 3.0, 1.5, 0.1)
lookback_days = st.sidebar.slider("Volume Lookback (days)", 10, 30, 20)

run_btn = st.sidebar.button("🚀 Run Screener", type="primary")

# ─── Caching for performance ───
@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period="1y"):
    """period 6mo se 1y kiya — 200-day SMA ke liye kam se kam ~250
    trading days ka data chahiye, 6mo mein sirf ~125 din milte the
    jisse SMA200 hamesha NaN aata."""
    try:
        df = yf.download(symbol, period=period, interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 210:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return None

@st.cache_data(ttl=3600)
def get_market_cap(symbol):
    try:
        info = yf.Ticker(symbol).info
        mcap = info.get("marketCap", 0)
        return mcap / 1e7  # Convert to Crores
    except Exception:
        return 0

def check_filters(df, mcap_cr, symbol):
    try:
        if df is None or len(df) < 210:
            return None

        close = df["Close"]
        volume = df["Volume"]

        latest_close = float(close.iloc[-1])
        latest_vol = float(volume.iloc[-1])

        # Early filters
        if latest_close < price_min:
            return None
        if mcap_cr < mcap_min:
            return None

        # Indicators — ab manually calculate ho rahe hain
        rsi_series = calc_rsi(close, length=14)
        rsi = float(rsi_series.iloc[-1])

        sma50_series = calc_sma(close, length=50)
        sma50 = float(sma50_series.iloc[-1])

        sma200_series = calc_sma(close, length=200)
        sma200 = float(sma200_series.iloc[-1])

        # Volume: last 3 days avg vs previous lookback days avg
        vol_3d = float(volume.iloc[-3:].mean())
        vol_prev = float(volume.iloc[-(lookback_days + 3):-3].mean())

        if pd.isna(rsi) or pd.isna(sma50) or pd.isna(sma200):
            return None

        if not (rsi_min < rsi < rsi_max):
            return None
        if not (latest_close < sma50):
            return None
        if not (latest_close > sma200):
            return None
        if not (vol_3d > vol_prev * volume_mult):
            return None

        return {
            "Symbol": symbol.replace(".NS", ""),
            "Close": round(latest_close, 2),
            "RSI": round(rsi, 1),
            "SMA50": round(sma50, 2),
            "SMA200": round(sma200, 2),
            "Volume_3D": int(vol_3d),
            "Volume_Avg": int(vol_prev),
            "MarketCap_Cr": round(mcap_cr, 0),
            "Dist_from_52W_High_%": round(((close.max() - latest_close) / close.max()) * 100, 1)
        }

    except Exception:
        return None

# ─── Main Logic ───
if run_btn:
    progress = st.progress(0, text="Scanning Nifty 200... Please wait")
    results = []
    total = len(NIFTY_200)

    for i, symbol in enumerate(NIFTY_200):
        progress.progress((i + 1) / total, text=f"Checking {symbol.replace('.NS', '')}... ({i+1}/{total})")

        df = fetch_stock_data(symbol)
        mcap = get_market_cap(symbol)

        result = check_filters(df, mcap, symbol)
        if result:
            results.append(result)

    progress.empty()

    # Results ko session_state mein save karo — warna page par kahin aur
    # click karte hi (koi bhi rerun trigger hote hi) ye data gayab ho
    # jaata tha, kyunki 'results' sirf ek local variable tha
    st.session_state["smc_results"] = results
    st.session_state["smc_total"] = total
    st.session_state["smc_scan_time"] = datetime.now().strftime("%d %b %Y, %H:%M")

# ─── Display results (session_state se — persist rehta hai) ───
if "smc_results" in st.session_state:
    results = st.session_state["smc_results"]
    total = st.session_state["smc_total"]
    scan_time = st.session_state.get("smc_scan_time", "")

    if results:
        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values(by="RSI", ascending=False)

        st.success(f"✅ {len(results)} stocks found out of {total}! (Scan: {scan_time})")
        st.dataframe(df_results, use_container_width=True, height=500)

        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"smc_screener_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("🎯 Next Steps")
        st.markdown("""
        1. **Copy symbols** from above
        2. **Open TradingView** → Weekly chart
        3. **Mark OB/FVG** manually
        4. **Wait for price** to reach zone + 75m bullish displacement
        5. **Trade** with proper SL (OB/FVG low ke neeche)
        """)
    else:
        st.warning("⚠️ No stocks found today. Try relaxing filters or check tomorrow.")

else:
    st.info("👈 Adjust filters in sidebar and click **Run Screener**")

    st.markdown("---")
    st.subheader("📋 Default Filter Logic")
    st.markdown(f"""
    | Filter | Value |
    |--------|-------|
    | RSI | {rsi_min} - {rsi_max} |
    | Close vs SMA 50 | **Below** (pullback) |
    | Close vs SMA 200 | **Above** (uptrend) |
    | Volume | Last 3 days > {volume_mult}x of previous {lookback_days} days avg |
    | Market Cap | > {mcap_min:,} Cr |
    | Price | > ₹{price_min} |
    | Universe | **Nifty 200** |
    """)

st.markdown("---")
st.caption("Built for SMC Swing Trading | Data: Yahoo Finance | Universe: Nifty 200")
