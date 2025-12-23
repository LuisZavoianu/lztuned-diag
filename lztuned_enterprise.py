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
# ULTIMATE UX/UI - MOTORSPORT COMMAND CENTER
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

/* Fundal General si Scrollbar */
.main {
    background: radial-gradient(circle at 50% 10%, #1a2332 0%, #0b0f14 100%);
}

/* Redefinire Fonturi */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    color: #e0e6ed;
}

/* Header High-Tech */
.header-box {
    background: rgba(13, 17, 23, 0.8);
    padding: 60px 20px;
    border-radius: 0px 0px 40px 40px;
    border-bottom: 3px solid #4da3ff;
    border-left: 1px solid rgba(77, 163, 255, 0.3);
    border-right: 1px solid rgba(77, 163, 255, 0.3);
    margin-top: -60px;
    margin-bottom: 50px;
    text-align: center;
    box-shadow: 0 15px 50px rgba(0,0,0,0.8), 0 0 20px rgba(77, 163, 255, 0.2);
    position: relative;
    overflow: hidden;
}

.header-box::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #4da3ff, transparent);
    animation: scanline 3s linear infinite;
}

@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(30px, 6vw, 55px);
    font-weight: 900;
    letter-spacing: 5px;
    margin-bottom: 5px;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(77, 163, 255, 0.6);
}

.header-box p {
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
    letter-spacing: 4px;
    color: #4da3ff;
    text-transform: uppercase;
}

/* Titluri Sectiuni Cyber */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #ffffff;
    margin: 50px 0 30px 0;
    padding: 10px 20px;
    background: linear-gradient(90deg, rgba(77, 163, 255, 0.2) 0%, transparent 100%);
    border-left: 5px solid #4da3ff;
    text-transform: uppercase;
}

/* Alerte Ultra-Vizibile */
.alert-container {
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 25px;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 12px;
    position: relative;
    overflow: hidden;
}

.alert-critical {
    background: rgba(204, 0, 0, 0.1);
    border: 1px solid #ff4d4d;
    box-shadow: inset 0 0 20px rgba(255, 77, 77, 0.2), 0 0 15px rgba(255, 77, 77, 0.1);
}

.alert-warning {
    background: rgba(204, 136, 0, 0.1);
    border: 1px solid #ffcc00;
    box-shadow: inset 0 0 20px rgba(255, 204, 0, 0.2);
}

.alert-ok {
    background: rgba(31, 92, 51, 0.1);
    border: 1px solid #33cc66;
}

.alert-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 26px;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 15px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.alert-body { font-size: 18px; opacity: 0.9; font-weight: 500; }
.alert-action { 
    background: rgba(255,255,255,0.07); 
    padding: 15px; 
    border-radius: 4px; 
    font-weight: 700; 
    border-left: 4px solid #fff;
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
    text-transform: uppercase;
}

/* Metricile */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(77, 163, 255, 0.2);
    padding: 25px !important;
    border-radius: 4px !important;
    transition: 0.3s;
}

div[data-testid="stMetric"]:hover {
    background: rgba(77, 163, 255, 0.08);
    border-color: #4da3ff;
}

div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 2px;
    color: #4da3ff !important;
    text-transform: uppercase;
}

/* Expander si Carduri Senzor */
.streamlit-expanderHeader {
    background: rgba(30, 39, 50, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 14px !important;
}

.sensor-card {
    background: #0d1117;
    padding: 20px;
    border-radius: 4px;
    border: 1px solid #1f2a3a;
    font-size: 15px;
    line-height: 1.6;
    border-left: 3px solid #4da3ff;
}

/* Tab-uri Custom */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #9fb6d9 !important;
    font-family: 'Orbitron', sans-serif !important;
    padding: 0 30px !important;
}

.stTabs [aria-selected="true"] {
    border-top: 3px solid #4da3ff !important;
    background-color: rgba(77, 163, 255, 0.1) !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA DICTIONARY (UNCHANGED)
# ======================================================
SENSOR_DESCRIPTIONS = {
    "Motor RPM": "Viteza de rotație a arborelui cotit. Esențială pentru axa X în hărțile de tuning.",
    "Engine load": "Sarcina motorului. Indică volumul de aer raportat la capacitatea cilindrică.",
    "Air mass": "Cantitatea de aer absorbită. Determinantă pentru calculul amestecului (MAF).",
    "Ignition angle": "Momentul scânteii. Valorile prea mici indică retard cauzat de detonație.",
    "Injection time": "Durata deschiderii injectoarelor (ms). Peste 20ms indică saturație.",
    "Knock sensor #1": "Senzor piezo care detectează vibrații de detonație în bloc.",
    "Motor temp.": "Temperatura antigelului. Optim: 85-95°C.",
    "Oil temp.": "Temperatura uleiului. Peste 115°C necesită răcire suplimentară.",
    "Battery voltage": "Tensiunea sistemului. Trebuie să fie stabilă (>13.5V în mers)."
}

# ======================================================
# UTILS & DATA ENGINE (UNCHANGED)
# ======================================================
def safe_col(df, name):
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
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
    duty_max = df['Inj_Duty'].max()
    lambda_wot = wot['Lambda_Avg'].mean() if not wot.empty else 0

    if duty_max > 90:
        reports.append(("FUEL SYSTEM", "HARD LIMIT", f"Duty Cycle at {duty_max:.1f}%", "Injector capacity exceeded. Hardware upgrade required."))
    elif lambda_wot > 0.88:
        reports.append(("FUEL SYSTEM", "CRITICAL", f"WOT Lambda {lambda_wot:.2f}", "Lean mixture under load. Enrich fueling maps immediately."))
    else:
        reports.append(("FUEL SYSTEM", "OK", "Fuel delivery within optimal parameters.", "No correction required."))

    k_peak = df['Knock_Peak'].max()
    if k_peak > 2.2:
        reports.append(("IGNITION SYSTEM", "CRITICAL", f"Knock Peak {k_peak:.2f} V", "Active detonation. Reduce ignition advance by 2–4 degrees."))
    else:
        reports.append(("IGNITION SYSTEM", "OK", "No dangerous knock detected.", "Ignition strategy is stable."))

    oil = df['Oil temp.'].max()
    if oil > 112:
        reports.append(("THERMAL MANAGEMENT", "WARNING", f"Oil temperature {oil:.1f} °C", "Cooling efficiency insufficient during sustained load."))
    else:
        reports.append(("THERMAL MANAGEMENT", "OK", "Thermal behavior within safe limits.", "Cooling system operating nominally."))
    return reports

# ======================================================
# APP
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTUNED ARCHITECT</h1>
        <p>Motorsport ECU Diagnostic Platform // v20.0</p>
        <div style="font-size: 10px; opacity: 0.5; margin-top: 15px; letter-spacing: 2px;">
            ENGINEERED BY LUIS ZAVOIANU // APPLICATION ENGINEER
        </div>
    </div>
    """, unsafe_allow_html=True)

    # File Uploader Stilizat implicit
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        file = st.file_uploader("📂 DRAG & DROP ECU LOG (.CSV)", type="csv")
    
    if not file:
        st.markdown("<div style='text-align:center; padding:50px; color:#4da3ff; font-family:Orbitron;'>SYSTEM IDLE - WAITING FOR DATA INPUT...</div>", unsafe_allow_html=True)
        return

    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # KPI DASHBOARD
    st.markdown("<h2 class='section-title'>Engine Performance Telemetry</h2>", unsafe_allow_html=True)
    k = st.columns(4)
    k[0].metric("MAX RPM", f"{int(df['Motor RPM'].max())}")
    k[1].metric("AIR MASS", f"{df['Air mass'].max():.1f}")
    k[2].metric("INJ DUTY", f"{df['Inj_Duty'].max():.1f}%")
    k[3].metric("IGNITION", f"{df['Ignition angle'].min():.1f}°")

    # VERDICT & CRITICAL ALERTS
    st.markdown("<h2 class='section-title'>System Verdict & Safety Status</h2>", unsafe_allow_html=True)
    
    diagnostics = get_diagnostics(df)
    for title, level, obs, action in diagnostics:
        if level in ["CRITICAL", "HARD LIMIT"]:
            alert_class, icon = "alert-critical", "❌"
        elif level == "WARNING":
            alert_class, icon = "alert-warning", "⚠️"
        else:
            alert_class, icon = "alert-ok", "✅"

        st.markdown(f"""
        <div class="alert-container {alert_class}">
            <div class="alert-header">{icon} {title} // {level}</div>
            <div class="alert-body"><b>TELEMETRY OBS:</b> {obs}</div>
            <div class="alert-action">REQUIRED: {action}</div>
        </div>
        """, unsafe_allow_html=True)

    # SENSOR FORENSICS
    st.markdown("<h2 class='section-title'>Sensor Forensics Analysis</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["[ COMB ]", "[ FLOW ]", "[ TEMP ]", "[ ELEC ]"])

    group_map = {
        0: ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Knock sensor #2', 'Lambda_Avg', 'Injection time'],
        1: ['Air mass', 'Engine load', 'Throttle position', 'VE_Calculated'],
        2: ['Motor temp.', 'Oil temp.', 'Intake temp.'],
        3: ['Battery voltage', 'Electric fan speed', 'Gear']
    }

    for tab, keys in zip(tabs, group_map.values()):
        with tab:
            st.write(" ")
            for c in keys:
                if c in df.columns:
                    with st.expander(f"SCAN CHANNEL: {c.upper()}"):
                        c1, c2 = st.columns([1, 2.5])
                        with c1:
                            st.markdown(f"<div class='sensor-card'><b>CHANNEL INFO:</b><br>{SENSOR_DESCRIPTIONS.get(c, 'Standard telemetry input.')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='margin-top:20px; font-size:12px;'><b>PEAK RANGE:</b><br>{df[c].min()} — {df[c].max()}</div>", unsafe_allow_html=True)
                        with c2:
                            fig = px.line(df, x='time', y=c, template="plotly_dark", color_discrete_sequence=['#4da3ff'])
                            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=10), 
                                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                              xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#263041'))
                            st.plotly_chart(fig, use_container_width=True)

    # ADVANCED TELEMETRY
    st.markdown("<h2 class='section-title'>Advanced Overlay & Correlation</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["[ OVERLAY ]", "[ MATRIX ]"])

    with t1:
        selected = st.multiselect("Select Channels:", all_cols, default=['Motor RPM', 'Ignition angle', 'Knock_Peak'])
        if selected:
            fig = make_subplots(rows=len(selected), cols=1, shared_xaxes=True, vertical_spacing=0.02)
            for i, s in enumerate(selected):
                fig.add_trace(go.Scatter(x=df['time'], y=df[s], name=s, line=dict(color='#4da3ff', width=1.5)), row=i+1, col=1)
            fig.update_layout(height=180*len(selected), template="plotly_dark", showlegend=True,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
        fig_corr.update_layout(height=600, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_corr, use_container_width=True)

    # DATA TABLE
    st.markdown("<h2 class='section-title'>Full Telemetry Archive</h2>", unsafe_allow_html=True)
    with st.expander("ACCESS RAW DATASET"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    app()
