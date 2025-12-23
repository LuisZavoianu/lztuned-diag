import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(
    page_title="LZTuned Architect Ultimate v20.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# UI / UX – PROFESSIONAL MOTORSPORT THEME
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap');

/* ---------- GLOBAL ---------- */
html, body {
    background-color: #111827;
    color: #e5e7eb;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #111827;
}

/* ---------- HEADER ---------- */
.header-box {
    background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 36px;
    margin-bottom: 40px;
    text-align: center;
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 40px;
    letter-spacing: 2px;
    color: #38bdf8;
    margin-bottom: 10px;
}

.header-box p {
    font-size: 14px;
    letter-spacing: 1px;
    color: #cbd5f5;
}

/* ---------- SECTION TITLES ---------- */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px;
    letter-spacing: 1.4px;
    color: #7dd3fc;
    margin: 30px 0 20px 0;
}

/* ---------- METRICS ---------- */
[data-testid="stMetric"] {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #f8fafc;
    font-size: 26px;
}

/* ---------- STATUS CARDS ---------- */
.status-card {
    background-color: #020617;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
    border: 1px solid #1e293b;
}

.status-card h3 {
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
    margin-bottom: 8px;
    color: #e5e7eb;
}

.status-card p {
    font-size: 14px;
    color: #cbd5f5;
}

.ok { border-left: 6px solid #22c55e; }
.warn { border-left: 6px solid #eab308; }
.crit { border-left: 6px solid #ef4444; }

/* ---------- SENSOR CARDS ---------- */
.sensor-card {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px;
    font-size: 13px;
    color: #cbd5f5;
}

/* ---------- EXPANDERS ---------- */
details {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 8px;
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', sans-serif;
    font-size: 13px;
    letter-spacing: 1px;
    color: #cbd5f5;
}

/* ---------- PLOTS ---------- */
.js-plotly-plot {
    background-color: #020617;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA DICTIONARY (UNCHANGED)
# ======================================================
SENSOR_DESCRIPTIONS = {
    "Motor RPM": "Viteza de rotație a arborelui cotit. Axă principală de analiză.",
    "Engine load": "Gradul de încărcare al motorului.",
    "Air mass": "Debit aer admis – bază pentru calcul combustibil.",
    "Ignition angle": "Avans aprindere. Valori scăzute indică retard.",
    "Injection time": "Durata injecției (ms).",
    "Knock sensor #1": "Detecție vibrații detonație.",
    "Motor temp.": "Temperatura lichid răcire.",
    "Oil temp.": "Temperatura ulei.",
    "Battery voltage": "Stare sistem electric."
}

# ======================================================
# ENGINE (UNCHANGED)
# ======================================================
def safe_col(df, name):
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

def compute_channels(df):
    rpm = safe_col(df, 'Motor RPM').replace(0, np.nan)
    df['Inj_Duty'] = (safe_col(df, 'Injection time') * rpm) / 1200
    df['Lambda_Avg'] = (safe_col(df, 'Lambda #1 integrator ') + safe_col(df, 'Lambda #2 integrator')) / 2
    df['VE_Calculated'] = (safe_col(df, 'Air mass') * 100) / (rpm * 0.16 + 1)
    df['Knock_Peak'] = df[['Knock sensor #1', 'Knock sensor #2']].max(axis=1)
    df['WOT'] = (safe_col(df, 'Engine load') > 70) & (rpm > 3000)
    return df

def get_diagnostics(df):
    wot = df[df['WOT']]
    reports = []

    if df['Inj_Duty'].max() > 90:
        reports.append(("FUEL SYSTEM", "HARD LIMIT", "Injector duty exceeded", "Upgrade injectors"))
    elif wot['Lambda_Avg'].mean() > 0.88:
        reports.append(("FUEL SYSTEM", "CRITICAL", "Lean mixture at WOT", "Enrich fueling maps"))
    else:
        reports.append(("FUEL SYSTEM", "OK", "Fueling within target", "No action required"))

    if df['Knock_Peak'].max() > 2.2:
        reports.append(("IGNITION SYSTEM", "CRITICAL", "Detonation detected", "Reduce ignition advance"))
    else:
        reports.append(("IGNITION SYSTEM", "OK", "Ignition stable", "Safe operation"))

    if df['Oil temp.'].max() > 112:
        reports.append(("THERMAL MANAGEMENT", "WARNING", "High oil temperature", "Improve cooling"))
    else:
        reports.append(("THERMAL MANAGEMENT", "OK", "Thermal conditions stable", "Nominal operation"))

    return reports

# ======================================================
# APP
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTuned Architect Ultimate</h1>
        <p>MOTORSPORT ECU DIAGNOSTIC PLATFORM<br>
        Engineered by <b>Luis Zavoianu</b> · Application Engineer</p>
    </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader("Load ECU Log (CSV)", type="csv")
    if not file:
        return

    df = compute_channels(pd.read_csv(file, sep=';'))

    st.markdown("<div class='section-title'>ENGINE PERFORMANCE OVERVIEW</div>", unsafe_allow_html=True)
    c = st.columns(4)
    c[0].metric("MAX RPM", int(df['Motor RPM'].max()))
    c[1].metric("AIR MASS PEAK", f"{df['Air mass'].max():.1f}")
    c[2].metric("INJ DUTY MAX", f"{df['Inj_Duty'].max():.1f}%")
    c[3].metric("MIN IGNITION", f"{df['Ignition angle'].min():.1f}°")

    st.markdown("<div class='section-title'>SYSTEM VERDICT</div>", unsafe_allow_html=True)
    for title, level, obs, act in get_diagnostics(df):
        cls = {"OK": "ok", "WARNING": "warn", "CRITICAL": "crit", "HARD LIMIT": "crit"}[level]
        st.markdown(f"""
        <div class="status-card {cls}">
            <h3>{title} — {level}</h3>
            <p><b>Observation:</b> {obs}</p>
            <p><b>Recommended Action:</b> {act}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
