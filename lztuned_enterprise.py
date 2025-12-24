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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@500;700&display=swap');

/* =========================
   GLOBAL BASE
========================= */
.main {
    background: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0b0f14;
}

/* =========================
   HEADER – PREMIUM / APPLE STYLE
========================= */
.header-box {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f5f6f8 100%
    );
    padding: 70px 20px 60px;
    margin: -60px -4rem 60px;
    border-bottom: 1px solid #e5e7eb;
    text-align: center;
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(28px, 5vw, 46px);
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 10px;
    color: #0b0f14;
}

.header-box p {
    font-size: 13px;
    letter-spacing: 3px;
    color: #6b7280;
    text-transform: uppercase;
}

/* =========================
   SECTION TITLES
========================= */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    margin: 60px 0 30px;
    padding-left: 14px;
    border-left: 4px solid #d90429;
    color: #0b0f14;
    text-transform: uppercase;
}

/* =========================
   KPI METRICS
========================= */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}

div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px;
    color: #6b7280 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #0b0f14 !important;
}

/* =========================
   ALERTS / VERDICT
========================= */
.alert-container {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 24px;
    border: 1px solid #e5e7eb;
}

.alert-critical {
    border-left: 6px solid #dc2626;
}

.alert-warning {
    border-left: 6px solid #f59e0b;
}

.alert-ok {
    border-left: 6px solid #16a34a;
}

.alert-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

.alert-body {
    font-size: 15px;
    color: #374151;
}

.alert-action {
    margin-top: 14px;
    padding: 14px;
    background: #f5f6f8;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* =========================
   EXPANDERS
========================= */
.streamlit-expanderHeader {
    background: #f5f6f8 !important;
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
    font-weight: 600 !important;
}

/* =========================
   SENSOR CARD
========================= */
.sensor-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    font-size: 14px;
    line-height: 1.6;
}

/* =========================
   TABS – CLEAN / PREMIUM
========================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: #f5f6f8 !important;
    border-radius: 10px;
    padding: 10px 24px;
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    letter-spacing: 2px;
    color: #6b7280 !important;
}

.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    color: #0b0f14 !important;
}

/* =========================
   FILE UPLOADER
========================= */
section[data-testid="stFileUploader"] {
    background: #f9fafb;
    border: 2px dashed #d1d5db;
    border-radius: 16px;
    padding: 30px;
}

# ======================================================
# EXPERT THRESHOLD INTELLIGENCE (EXTENDED DATA)
# ======================================================

def get_expert_advice(sensor, value, wot_active):
    """
    Returnează (status, explicație, culoare) bazat pe praguri de motorsport.
    """
    # Definiții Praguri: (Min, Max, Unitate)
    limits = {
        'Motor RPM': (800, 7000, 'RPM'),
        'Oil temp.': (80, 115, '°C'),
        'Motor temp.': (75, 100, '°C'),
        'Lambda_Avg': (0.76, 0.88, 'λ'), # Valabil doar pentru WOT
        'Knock_Peak': (0, 2.0, 'V'),
        'Battery voltage': (13.2, 14.8, 'V'),
        'Inj_Duty': (0, 85, '%')
    }

    if sensor not in limits:
        return "MONITORIZARE", "Parametru în limite de funcționare standard.", "#58a6ff"

    min_v, max_v, unit = limits[sensor]
    
    # Logica pentru Lambda (doar în sarcină)
    if sensor == 'Lambda_Avg' and not wot_active:
        return "STOECHIOMETRIC", "Motorul este în Cruise Mode. Lambda 1.0 este normal.", "#8b949e"

    if value > max_v:
        if sensor == 'Inj_Duty':
            return "CRITICAL", f"Peste {max_v}{unit}. Injectoarele nu se mai închid. Risc de amestec sărac la turații mari.", "#f85149"
        if sensor == 'Knock_Peak':
            return "PERICOL", f"Detonație detected ({value}V). Risc de spargere pistoane. Redu avansul!", "#f85149"
        if sensor == 'Oil temp.':
            return "WARNING", f"Ulei la {value}{unit}. Vâscozitatea scade periculos. Verifică răcitorul.", "#d29922"
        return "HIGH", f"Valoare peste pragul optim de {max_v}{unit}.", "#d29922"

    if value < min_v:
        if sensor == 'Battery voltage':
            return "LOW VOLTAGE", "Alternator sub-eficient. Poate afecta timpii de injecție (Deadtime).", "#f85149"
        if sensor == 'Motor temp.':
            return "COLD", "Motor sub temperatura de regim. Uzură mecanică crescută.", "#58a6ff"
        return "LOW", f"Sub pragul minim de {min_v}{unit}.", "#58a6ff"

    return "OPTIM", f"Funcționare nominală în parametri ({value:.2f} {unit}).", "#3fb950"
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

def render_advanced_diagnostics(df):
    st.markdown("<div class='section-title'>Advanced Threshold Intelligence</div>", unsafe_allow_html=True)
    
    # Luăm valorile de vârf pentru analiză
    analysis_sensors = {
        'Motor RPM': df['Motor RPM'].max(),
        'Inj_Duty': df['Inj_Duty'].max() if 'Inj_Duty' in df.columns else 0,
        'Knock_Peak': df['Knock_Peak'].max() if 'Knock_Peak' in df.columns else 0,
        'Lambda_Avg': df[df['WOT']]['Lambda_Avg'].mean() if not df[df['WOT']].empty else 1.0,
        'Oil temp.': df['Oil temp.'].max() if 'Oil temp.' in df.columns else 0,
        'Battery voltage': df['Battery voltage'].min() if 'Battery voltage' in df.columns else 0
    }

    cols = st.columns(3)
    for i, (sensor, val) in enumerate(analysis_sensors.items()):
        status, desc, color = get_expert_advice(sensor, val, not df[df['WOT']].empty)
        
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:{color}15; border:1px solid {color}44; padding:20px; border-radius:12px; margin-bottom:20px; height:200px;">
                <div style="color:{color}; font-family:Orbitron; font-weight:900; font-size:14px; margin-bottom:5px;">{sensor.upper()}</div>
                <div style="font-size:24px; font-weight:700;">{val:.2f}</div>
                <div style="background:{color}; color:white; display:inline-block; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:900; margin-bottom:10px;">{status}</div>
                <div style="font-size:13px; opacity:0.9; line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
if __name__ == "__main__":
    app()

