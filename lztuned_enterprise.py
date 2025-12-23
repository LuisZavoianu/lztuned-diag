import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== CONFIG =====================
st.set_page_config(
    page_title="LZTuned Universal v15.5",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== STYLE =====================
st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #c9d1d9; }
.header-box {
    background: linear-gradient(90deg, #001529 0%, #003a8c 100%);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.status-card {
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #30363d;
}
.ok { background-color: #161b22; border-left: 6px solid #238636; }
.warn { background-color: #2a2200; border-left: 6px solid #d29922; }
.crit { background-color: #2d1616; border-left: 6px solid #da3633; }
h1, h2, h3 { color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ===================== UTILS =====================
def safe_col(df, name):
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

# ===================== DATA ENGINE =====================
def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
    rpm = safe_col(df, 'Motor RPM').replace(0, np.nan)

    df['Inj_Duty'] = (safe_col(df, 'Injection time') * rpm) / 1200
    df['Lambda_Avg'] = (
        safe_col(df, 'Lambda #1 integrator ') +
        safe_col(df, 'Lambda #2 integrator')
    ) / 2

    df['VE_Calculated'] = (safe_col(df, 'Air mass') * 100) / (rpm * 0.16 + 1)

    df['Knock_Peak'] = df[
        ['Knock sensor #1', 'Knock sensor #2']
    ].max(axis=1)

    df['WOT'] = (safe_col(df, 'Engine load') > 70) & (rpm > 3500)

    return df

# ===================== RENDER =====================
def render_card(title, level, obs, action):
    cls = {"OK": "ok", "WARNING": "warn", "CRITICAL": "crit", "HARD LIMIT": "crit"}[level]
    st.markdown(f"""
    <div class="status-card {cls}">
        <h3>{title} — {level}</h3>
        <p><b>Observație:</b> {obs}</p>
        <p><b>Acțiune recomandată:</b> {action}</p>
    </div>
    """, unsafe_allow_html=True)

# ===================== ANALYSIS =====================
def analyze_fuel(df):
    wot = df[df['WOT']]
    lam = wot['Lambda_Avg'].mean()
    duty = df['Inj_Duty'].max()

    if duty > 90:
        return ("⛽ BENZINĂ", "HARD LIMIT",
                f"Injector duty max = {duty:.1f}%",
                "Injectoare la limită. Scade sarcina sau upgrade hardware.")
    if lam > 0.88:
        return ("⛽ BENZINĂ", "CRITICAL",
                f"Lambda WOT = {lam:.2f} (prea sărac)",
                "Îmbogățește harta de fuel în zonele high load.")
    return ("⛽ BENZINĂ", "OK",
            "Amestec și duty cycle în parametri.",
            "Nu sunt necesare modificări.")

def analyze_ignition(df):
    knock = df['Knock_Peak'].max()
    ign_min = df['Ignition angle'].min()

    if knock > 2.5 or ign_min < 2:
        return ("⚡ APRINDERE", "CRITICAL",
                f"Knock max = {knock:.2f}, Ign min = {ign_min:.1f}°",
                "Reduce avansul 2–3° în zonele afectate.")
    return ("⚡ APRINDERE", "OK",
            "Nu s-au detectat detonații periculoase.",
            "Poți optimiza fin dacă EGT și IAT permit.")

def analyze_air(df):
    ve = df['VE_Calculated'].mean()
    if ve < 70:
        return ("🌬️ AER", "WARNING",
                f"VE mediu = {ve:.1f}%",
                "Verifică admisia, intercooler-ul și eventuale boost leaks.")
    return ("🌬️ AER", "OK",
            "Eficiență volumetrică bună.",
            "Configurația actuală este coerentă.")

def analyze_thermal(df):
    oil = df['Oil temp.'].max()
    coolant = df['Motor temp.'].max()

    if oil > 110 or coolant > 102:
        return ("🌡️ TERMIC", "CRITICAL",
                f"Ulei {oil:.1f}°C | Apă {coolant:.1f}°C",
                "Îmbunătățește răcirea sau limitează sarcina.")
    return ("🌡️ TERMIC", "OK",
            "Temperaturi stabile.",
            "Sistemul de răcire este eficient.")

# ===================== APP =====================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTuned Universal Diagnostic v15.5</h1>
        <p>Sistem Expert de Analiză ECU | <b>Luis Zavoianu</b></p>
    </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader("Încarcă LOG ECU (CSV)", type="csv")
    if not file:
        return

    df = pd.read_csv(file, sep=';')
    df = compute_channels(df)

    # ===== KPI =====
    st.subheader("📊 KPI Motor")
    k = st.columns(4)
    k[0].metric("RPM Max", int(df['Motor RPM'].max()))
    k[1].metric("Air Mass Max", f"{df['Air mass'].max():.1f}")
    k[2].metric("Ignition Min", f"{df['Ignition angle'].min():.1f}°")
    k[3].metric("Oil Temp Max", f"{df['Oil temp.'].max():.1f}°C")

    # ===== REPORT =====
    st.markdown("---")
    st.header("🏁 Raport Diagnostic")

    for res in [
        analyze_fuel(df),
        analyze_ignition(df),
        analyze_air(df),
        analyze_thermal(df)
    ]:
        render_card(*res)

    # ===== TELEMETRY =====
    st.markdown("---")
    t1, t2 = st.tabs(["📈 Telemetrie", "🧬 Corelații"])

    with t1:
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM"), 1, 1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass"), 1, 1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Lambda_Avg'], name="Lambda"), 2, 1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition"), 3, 1)
        fig.update_layout(height=850, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        st.plotly_chart(
            px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r'),
            use_container_width=True
        )

if __name__ == "__main__":
    app()
