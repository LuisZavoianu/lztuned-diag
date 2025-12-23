import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================================================
# CONFIG
# ======================================================
APP_TITLE = "LZTuned Architect Ultimate v20.1"

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# STYLE
# ======================================================
st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #c9d1d9; }

.header-box {
    background: linear-gradient(135deg, #001529 0%, #0050b3 100%);
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #30363d;
    margin-bottom: 30px;
    text-align: center;
}

.section-title { margin-top: 10px; }

.status-card {
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #30363d;
}

.sensor-card {
    background: #161b22;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #30363d;
    margin-bottom: 10px;
}

.ok { background-color: #161b22; border-left: 6px solid #238636; }
.warn { background-color: #2a2200; border-left: 6px solid #d29922; }
.crit { background-color: #2d1616; border-left: 6px solid #da3633; }

h1, h2, h3 { color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SENSOR DICTIONARY
# ======================================================
SENSOR_DESCRIPTIONS = {
    "Motor RPM": "Turația arborelui cotit. Axă principală pentru toate hărțile ECU.",
    "Engine load": "Sarcina motorului raportată la capacitatea volumetrică.",
    "Air mass": "Debit masic de aer. Determină cantitatea de combustibil necesară.",
    "Ignition angle": "Avansul aprinderii. Retardul indică knock sau protecție ECU.",
    "Injection time": "Durata de deschidere a injectorului (ms).",
    "Knock sensor #1": "Senzor de detonație – banc 1.",
    "Knock sensor #2": "Senzor de detonație – banc 2.",
    "Motor temp.": "Temperatura lichidului de răcire.",
    "Oil temp.": "Temperatura uleiului motor.",
    "Battery voltage": "Tensiunea sistemului electric."
}

# ======================================================
# UTILITIES
# ======================================================
def safe_col(df: pd.DataFrame, name: str) -> pd.Series:
    """Asigură existența coloanei."""
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

# ======================================================
# DATA ENGINE
# ======================================================
def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
    rpm = safe_col(df, "Motor RPM").replace(0, np.nan)

    df["Inj_Duty"] = (safe_col(df, "Injection time") * rpm) / 1200
    df["Lambda_Avg"] = (
        safe_col(df, "Lambda #1 integrator ") +
        safe_col(df, "Lambda #2 integrator")
    ) / 2

    df["VE_Calculated"] = (safe_col(df, "Air mass") * 100) / (rpm * 0.16 + 1)
    df["Knock_Peak"] = df[["Knock sensor #1", "Knock sensor #2"]].max(axis=1)

    df["WOT"] = (safe_col(df, "Engine load") > 70) & (rpm > 3000)

    return df

# ======================================================
# DIAGNOSTIC ENGINE
# ======================================================
def get_diagnostics(df: pd.DataFrame):
    reports = []
    wot = df[df["WOT"]]

    # ---- FUEL ----
    duty_max = df["Inj_Duty"].max()
    lambda_wot = wot["Lambda_Avg"].mean() if not wot.empty else np.nan

    if duty_max > 90:
        reports.append(("⛽ BENZINĂ", "HARD LIMIT",
                        f"Duty Cycle maxim {duty_max:.1f}%",
                        "Limită hardware. Injectoare insuficiente."))
    elif lambda_wot > 0.88:
        reports.append(("⛽ BENZINĂ", "CRITICAL",
                        f"Lambda WOT {lambda_wot:.2f} (amestec sărac)",
                        "Risc sever. Îmbogățește zona high load."))
    else:
        reports.append(("⛽ BENZINĂ", "OK",
                        "Amestec corect și injecție în parametri.",
                        "Strategie fuel stabilă."))

    # ---- IGNITION / KNOCK ----
    k_peak = df["Knock_Peak"].max()
    if k_peak > 2.2:
        reports.append(("⚡ APRINDERE", "CRITICAL",
                        f"Knock detectat ({k_peak:.2f}V)",
                        "Scade avansul cu 2–4° în zonele afectate."))
    else:
        reports.append(("⚡ APRINDERE", "OK",
                        "Aprindere stabilă, fără detonații.",
                        "Poți rafina avansul progresiv."))

    # ---- THERMAL ----
    oil_max = df["Oil temp."].max()
    if oil_max > 112:
        reports.append(("🌡️ TERMIC", "WARNING",
                        f"Temperatură ulei {oil_max:.1f}°C",
                        "Îmbunătățește răcirea sau limitează sarcina."))
    else:
        reports.append(("🌡️ TERMIC", "OK",
                        "Management termic stabil.",
                        "Sistem de răcire eficient."))

    return reports

# ======================================================
# UI COMPONENTS
# ======================================================
def render_status_card(title, level, obs, action):
    css = {"OK": "ok", "WARNING": "warn", "CRITICAL": "crit", "HARD LIMIT": "crit"}[level]
    st.markdown(f"""
    <div class="status-card {css}">
        <h3>{title} — {level}</h3>
        <p><b>Observație:</b> {obs}</p>
        <p><b>Acțiune recomandată:</b> {action}</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MAIN APP
# ======================================================
def app():
    st.markdown(f"""
    <div class="header-box">
        <h1>{APP_TITLE}</h1>
        <p>Sistem Expert de Diagnostic & Tuning Forensic<br>
        <b>Lead Engineer: Luis Zavoianu</b></p>
    </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader("Încarcă LOG ECU (CSV)", type="csv")
    if not file:
        return

    df_raw = pd.read_csv(file, sep=";")
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # ==================================================
    # KPI
    # ==================================================
    st.header("💎 Engine Master KPIs")
    k = st.columns(4)
    k[0].metric("RPM Max", int(df["Motor RPM"].max()))
    k[1].metric("Peak Air Mass", f"{df['Air mass'].max():.1f}")
    k[2].metric("Max Injector Duty", f"{df['Inj_Duty'].max():.1f}%")
    k[3].metric("Min Ignition", f"{df['Ignition angle'].min():.1f}°")

    st.markdown("---")

    # ==================================================
    # DIAGNOSTIC REPORT
    # ==================================================
    st.header("🏁 Verdict Tuning & Siguranță")
    for r in get_diagnostics(df):
        render_status_card(*r)

    st.markdown("---")

    # ==================================================
    # SENSOR FORENSICS
    # ==================================================
    st.header("🔍 Sensor Forensics Explorer")
    tabs = st.tabs(["🔥 Combustie", "🌬️ Aer & Sarcină", "🌡️ Termic", "🔋 Electric"])

    groups = [
        ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Knock sensor #2', 'Lambda_Avg', 'Injection time'],
        ['Air mass', 'Engine load', 'Throttle position', 'VE_Calculated'],
        ['Motor temp.', 'Oil temp.', 'Intake temp.'],
        ['Battery voltage', 'Electric fan speed', 'Gear']
    ]

    for tab, sensors in zip(tabs, groups):
        with tab:
            for s in sensors:
                if s in df.columns:
                    with st.expander(f"📊 {s}"):
                        c1, c2 = st.columns([1, 2])
                        c1.markdown(
                            f"<div class='sensor-card'><b>Rol:</b><br>{SENSOR_DESCRIPTIONS.get(s, 'Senzor ECU')}</div>",
                            unsafe_allow_html=True
                        )
                        c1.write(f"**Min:** {df[s].min()} | **Max:** {df[s].max()}")
                        fig = px.line(df, x="time", y=s)
                        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
                        c2.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==================================================
    # ADVANCED ANALYSIS
    # ==================================================
    st.header("📈 Advanced Telemetry Analysis")
    t1, t2 = st.tabs(["Multi-Channel Overlay", "Correlation Matrix"])

    with t1:
        selected = st.multiselect(
            "Selectează senzori pentru suprapunere:",
            all_cols,
            default=["Motor RPM", "Ignition angle", "Knock_Peak"]
        )
        if selected:
            fig = make_subplots(rows=len(selected), cols=1, shared_xaxes=True)
            for i, s in enumerate(selected):
                fig.add_trace(go.Scatter(x=df["time"], y=df[s], name=s), i+1, 1)
            fig.update_layout(height=180 * len(selected), template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        st.plotly_chart(
            px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r"),
            use_container_width=True
        )

    st.markdown("---")
    with st.expander("📄 Full Processed Data Table"):
        st.dataframe(df, use_container_width=True)

# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    app()
