import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================================================
# CONFIG & THEME LOCK
# ======================================================
st.set_page_config(
    page_title="LZTuned Architect Ultimate v20.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Rescrierea UI pentru contrast maxim și estetică perfectă
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

/* Fortare Tema Dark pe tot ecranul */
.stApp {
    background: #0b0f14;
}

/* Stil General Text */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    color: #e0e6ed !important;
}

/* Header High-Tech cu animatie finisata */
.header-box {
    background: linear-gradient(180deg, rgba(16, 24, 39, 1) 0%, rgba(11, 15, 20, 1) 100%);
    padding: 50px 20px;
    border-radius: 0px 0px 30px 30px;
    border-bottom: 2px solid #4da3ff;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 40px;
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(28px, 5vw, 50px);
    font-weight: 900;
    letter-spacing: 6px;
    color: #ffffff;
    text-shadow: 0 0 15px rgba(77, 163, 255, 0.5);
    margin: 0;
}

/* Sectiuni cu stil industrial */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    color: #4da3ff;
    letter-spacing: 2px;
    border-left: 4px solid #4da3ff;
    padding-left: 15px;
    margin: 40px 0 20px 0;
    text-transform: uppercase;
}

/* Carduri Metrici (KPI) - REPARATE PENTRU VIZIBILITATE */
div[data-testid="stMetric"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    padding: 20px !important;
    border-radius: 10px !important;
}
div[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 12px !important;
}
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* Reparare Expandere (Aici era problema in screenshot) */
.streamlit-expanderHeader {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}
.streamlit-expanderContent {
    background-color: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-top: none !important;
}

/* Stil Alerte (Fix culori si contrast) */
.alert-container {
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 6px solid transparent;
}
.alert-critical { 
    background: rgba(248, 81, 73, 0.1); 
    border: 1px solid rgba(248, 81, 73, 0.4);
    border-left: 6px solid #f85149;
}
.alert-ok { 
    background: rgba(63, 185, 80, 0.1); 
    border: 1px solid rgba(63, 185, 80, 0.4);
    border-left: 6px solid #3fb950;
}
.alert-warning { 
    background: rgba(210, 153, 34, 0.1); 
    border: 1px solid rgba(210, 153, 34, 0.4);
    border-left: 6px solid #d29922;
}

.alert-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Tab-uri Custom Contrast */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
    border-radius: 5px 5px 0 0 !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    background-color: #1f6feb !important;
    color: white !important;
    border: 1px solid #1f6feb !important;
}

/* Card Senzor Interior */
.sensor-card {
    background: #1c2128;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #444c56;
    color: #adbac7;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA ENGINE (UNCHANGED LOGIC)
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

def safe_col(df, name):
    if name not in df.columns: df[name] = np.nan
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
        reports.append(("FUEL SYSTEM", "HARD LIMIT", f"Duty Cycle at {duty_max:.1f}%", "Injector capacity exceeded."))
    elif lambda_wot > 0.88:
        reports.append(("FUEL SYSTEM", "CRITICAL", f"WOT Lambda {lambda_wot:.2f}", "Lean mixture! Enrich fueling maps."))
    else:
        reports.append(("FUEL SYSTEM", "OK", "Fuel delivery optimal.", "No correction required."))
    k_peak = df['Knock_Peak'].max()
    if k_peak > 2.2:
        reports.append(("IGNITION SYSTEM", "CRITICAL", f"Knock Peak {k_peak:.2f}V", "Detonation detected! Reduce advance."))
    else:
        reports.append(("IGNITION SYSTEM", "OK", "No knock detected.", "Safe ignition strategy."))
    return reports

# ======================================================
# MAIN APP INTERFACE
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTUNED ARCHITECT</h1>
        <p style="color:#4da3ff; letter-spacing:3px; font-weight:700;">MOTORSPORT DIAGNOSTIC v20.0</p>
    </div>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        file = st.file_uploader("📂 LOAD TELEMETRY DATA (CSV)", type="csv")
    
    if not file:
        st.info("System Ready. Please upload a log file to begin analysis.")
        return

    df = compute_channels(pd.read_csv(file, sep=';'))
    
    # KPI SECTION
    st.markdown("<div class='section-title'>Engine Performance Telemetry</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAX RPM", f"{int(df['Motor RPM'].max())}")
    m2.metric("AIR MASS", f"{df['Air mass'].max():.1f} kg/h")
    m3.metric("INJ DUTY", f"{df['Inj_Duty'].max():.1f}%")
    m4.metric("IGNITION", f"{df['Ignition angle'].min():.1f}°")

    # VERDICTS
    st.markdown("<div class='section-title'>System Verdict & Safety</div>", unsafe_allow_html=True)
    for title, level, obs, action in get_diagnostics(df):
        a_class = "alert-critical" if level == "CRITICAL" else "alert-ok" if level == "OK" else "alert-warning"
        icon = "🛑" if level == "CRITICAL" else "✅" if level == "OK" else "⚠️"
        st.markdown(f"""
        <div class="alert-container {a_class}">
            <div class="alert-header">{icon} {title} // {level}</div>
            <div style="font-size:14px; opacity:0.8;"><b>OBS:</b> {obs}</div>
            <div style="font-weight:700; margin-top:5px; color:white;">👉 ACTION: {action}</div>
        </div>
        """, unsafe_allow_html=True)

    # GRAPHS
    st.markdown("<div class='section-title'>Sensor Forensics Analysis</div>", unsafe_allow_html=True)
    tab_list = ["[ COMB ]", "[ FLOW ]", "[ TEMP ]", "[ ELEC ]"]
    tabs = st.tabs(tab_list)
    
    # Mapare senzori pe taburi
    sensor_groups = [
        ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Lambda_Avg'],
        ['Air mass', 'Engine load', 'VE_Calculated'],
        ['Motor temp.', 'Oil temp.'],
        ['Battery voltage']
    ]

    for tab, sensors in zip(tabs, sensor_groups):
        with tab:
            for s in sensors:
                if s in df.columns:
                    with st.expander(f"📊 DATA CHANNEL: {s.upper()}"):
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            st.markdown(f"<div class='sensor-card'>{SENSOR_DESCRIPTIONS.get(s, 'Telemetry channel')}</div>", unsafe_allow_html=True)
                            st.write(f"**MIN:** {df[s].min():.2f}")
                            st.write(f"**MAX:** {df[s].max():.2f}")
                        with c2:
                            fig = px.line(df, x='time', y=s, template="plotly_dark")
                            fig.update_traces(line_color='#4da3ff', line_width=1.5)
                            fig.update_layout(height=200, margin=dict(l=0,r=0,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Raw Dataset</div>", unsafe_allow_html=True)
    with st.expander("VIEW FULL DATA TABLE"):
        st.dataframe(df.head(100), use_container_width=True)

if __name__ == "__main__":
    app()
