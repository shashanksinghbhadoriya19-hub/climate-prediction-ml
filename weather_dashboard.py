# weather_dashboard.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date, timedelta
import math
import matplotlib.pyplot as plt


st.markdown("""
<style>
.highlight {
    background-color: #112b3c;
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Weather Dashboard", layout="wide")

# ------------- Utility functions ----------------
def fetch_forecast(lat, lon, timezone="Asia/Kolkata"):
    """
    Fetch forecast from Open-Meteo (hourly + daily + current).
    Returns dict with 'hourly' and 'daily' DataFrames and 'current' dict if available.
    """
    base = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,weathercode,windspeed_10m",
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "current_weather": "true",
        "timezone": timezone,
        "forecast_days": 7
    }
    resp = requests.get(base, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    # Hourly
    hourly = pd.DataFrame(data.get("hourly", {}))
    if not hourly.empty:
        hourly["time"] = pd.to_datetime(hourly["time"])
        hourly = hourly.set_index("time")
    # Daily
    daily = pd.DataFrame(data.get("daily", {}))
    if not daily.empty:
        daily["time"] = pd.to_datetime(daily["time"])
        daily = daily.set_index("time")
    current = data.get("current_weather", None)
    return {"hourly": hourly, "daily": daily, "current": current, "raw": data}

# map Open-Meteo weathercode to emoji + text (simplified)
WEATHER_CODE_MAP = {
    0: ("☀️", "Clear"),
    1: ("🌤️", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),
    48: ("🌫️", "Depositing rime fog"),
    51: ("🌦️", "Drizzle light"),
    53: ("🌧️", "Drizzle moderate"),
    55: ("🌧️", "Drizzle dense"),
    61: ("🌧️", "Rain light"),
    63: ("🌧️", "Rain moderate"),
    65: ("🌧️", "Rain heavy"),
    71: ("❄️", "Snow light"),
    73: ("❄️", "Snow moderate"),
    75: ("❄️", "Snow heavy"),
    80: ("🌦️", "Rain showers"),
    81: ("🌧️", "Heavy showers"),
    95: ("⛈️", "Thunderstorm"),
}
def wc_to_label(code):
    return WEATHER_CODE_MAP.get(code, ("🌈", "Unknown"))

# ---------------- UI: sidebar ----------------
st.sidebar.header("Settings")
city = st.sidebar.selectbox(
    "Choose city",
    ["Mumbai", "Delhi", "Kolkata", "Chennai", "Bengaluru", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Other (lat/lon)"]
)

coords_map = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
}
if city == "Other (lat/lon)":
    lat = st.sidebar.number_input("Latitude", value=20.0, format="%.6f")
    lon = st.sidebar.number_input("Longitude", value=78.0, format="%.6f")
else:
    lat, lon = coords_map[city]

st.sidebar.write(f"Using coordinates: {lat:.4f}, {lon:.4f}")
days_to_fetch = st.sidebar.slider("Forecast days", min_value=3, max_value=10, value=7)

# Small caching to avoid frequent API calls during dev
@st.cache_data(ttl=900)
def fetch_cached(lat, lon, days):
    return fetch_forecast(lat, lon)

# ------------- Fetch data ----------------
with st.spinner("Fetching forecast…"):
    try:
        bundle = fetch_cached(lat, lon, days_to_fetch)
        hourly = bundle["hourly"]
        daily = bundle["daily"]
        current = bundle["current"]
    except Exception as e:
        st.error(f"Failed to fetch forecast: {e}")
        st.stop()

# ------------- Top header / main card ----------------
col1, col2 = st.columns([2, 1])
with col1:
    # large card
    st.markdown("<div style='background:#0b2239; padding:20px; border-radius:12px; color:white'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:white; margin:0'>{city}</h1>", unsafe_allow_html=True)

    if current:
        temp = current.get("temperature")
        wc = current.get("weathercode")
        emoji, desc = wc_to_label(wc)
        st.markdown(f"<h2 style='font-size:64px; margin:5px 0'>{temp:.1f}°</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:18px'>{emoji}  {desc} · Wind {current.get('windspeed',0)} m/s</div>", unsafe_allow_html=True)
    else:
        # fallback to hourly now
        now = hourly.index[0] if not hourly.empty else None
        st.markdown("<h2 style='font-size:48px; margin:5px 0'>-°</h2>", unsafe_allow_html=True)

    # small hourly strip (next 8 hours)
    st.markdown("<div style='margin-top:12px; display:flex; gap:8px; overflow:auto'>", unsafe_allow_html=True)
    # next 8 hourly points
        # next 8 hourly points
    if not hourly.empty:
        now = pd.Timestamp.now(tz=hourly.index.tz) if hourly.index.tz else pd.Timestamp.now()
        next_hours = hourly[hourly.index >= now].iloc[:8]

        for t, row in next_hours.iterrows():
            temp_h = row.get("temperature_2m", float("nan"))
            wc_h = int(row.get("weathercode", 0))
            emoji_h, _ = wc_to_label(wc_h)

            # Windows-safe time format (e.g., "3 PM")
            hour_str = t.strftime("%I %p").lstrip("0")

            st.markdown(
                f"""
                <div style='background:#0e3046; color:white; padding:8px; border-radius:8px;
                            min-width:80px; text-align:center; display:inline-block; margin:5px'>
                    <div style='font-weight:bold'>{hour_str}</div>
                    <div style='font-size:20px; margin:6px 0'>{emoji_h}</div>
                    <div style='font-size:16px'>{temp_h:.0f}°</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            


    



with col2:
    # 7-day forecast column (compact)
    st.markdown("<div style='background:#071a2a; padding:12px; border-radius:12px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; margin:0'>7-Day Forecast</h3>", unsafe_allow_html=True)
    if not daily.empty:
        # show each day
        for t, row in daily.iloc[:7].iterrows():
            date_str = t.strftime("%a %d")
            tmax = row.get("temperature_2m_max", float("nan"))
            tmin = row.get("temperature_2m_min", float("nan"))
            wc_d = int(row.get("weathercode", 0))
            emoji_d, desc_d = wc_to_label(wc_d)
            st.markdown(
                f"<div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; color:white'>"
                f"<div>{date_str}</div>"
                f"<div>{emoji_d} {desc_d}</div>"
                f"<div>{int(tmax)}/{int(tmin)}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------- Middle: air conditions + charts ----------------
st.markdown("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Hourly temperature (24h)")
    if not hourly.empty:
        # build 24h window
        now = pd.Timestamp.now(tz=hourly.index.tz) if hourly.index.tz else pd.Timestamp.now()
        window = hourly[(hourly.index >= now) & (hourly.index < now + pd.Timedelta(hours=24))]
        if window.empty:
            window = hourly.iloc[:24]
        # plot simple line chart with matplotlib to control style
        plt.figure(figsize=(10, 2.6))
        plt.plot(window.index, window["temperature_2m"], marker="o")
        plt.fill_between(window.index, window["temperature_2m"], alpha=0.1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()
    else:
        st.write("No hourly data")

with c2:
    st.subheader("Air conditions")
    # Real feel: none available, show current vs feels-like if present (open-meteo doesn't give feels-like in this endpoint)
    if current:
        wind = current.get("windspeed", 0)
        st.metric("Wind (m/s)", f"{wind}")
    # show today's precipitation from daily
    if not daily.empty:
        today = daily.iloc[0]
        precip = today.get("precipitation", 0)
        st.metric("Precipitation (today)", f"{precip} mm")
    # small extra tiles
    col_a, col_b = st.columns(2)
    with col_a:
        if current:
            st.metric("Now (°C)", f"{current.get('temperature')}°")
    with col_b:
        # show timezone or updated time if present
        st.write("Updated:", datetime.now().strftime("%Y-%m-%d %H:%M"))

# ------------- Footer / tips ----------------
st.markdown("---")
st.write("Tip: change city in left settings. Data from Open-Meteo (free). This is a demo layout — customize styles and icons as you like.")
