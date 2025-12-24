import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================================================
# CONFIG & INITIALIZATION
# ======================================================
st.set_page_config(
    page_title="LZTuned Architect Ultimate v20.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# ULTIMATE UX/UI - PREMIUM LIGHT MODE STYLING
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@500;700;900&display=swap');

/* Base App Setup */
.main { background: #ffffff; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0b0f14;
}

/* Header - Apple Style */
.header-box {
    background: linear-gradient(180deg, #ffffff 0%, #f5f6f8 100%);
    padding: 60px 20px;
    margin: -60px -4rem 40px;
    border-bottom: 1px solid #e5e7eb;
    text-align: center;
}
.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(28px, 5vw, 42px);
    font-weight: 900;
    letter-spacing: 4px;
    color: #0b0f14;
    margin: 0;
}
.header-box p {
    font-size: 12px;
    letter-spacing: 3px;
    color: #6b7280;
    text-transform: uppercase;
    margin-top: 10px;
}

/* Section Titles */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    margin: 50px 0 25px;
    padding-left: 14px;
    border-left: 4px solid #4da3ff;
    color: #0b0f14;
    text-transform: uppercase;
}

/* Expert Cards (Threshold Analysis) */
.expert-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 24px;
    border-radius: 16px;
    height: 240px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    transition: transform 0.2s;
}
.expert-card:hover { transform: translateY(-5px); }
.status-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 900;
    font-family: 'Orbitron';
    margin-bottom: 12px;
    text-transform: uppercase;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 20px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.02);
}
div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 1px;
    color: #6b7280 !important;
}

/* Alerts */
.alert-container {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}
.alert-critical { border-left: 6px solid #ef4444; }
.alert-warning { border-left: 6px solid #f59e0b; }
.alert-ok { border-left: 6px solid #10b981; }

/* Tabs & Expanders */
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    letter-spacing: 1px;
}
.streamlit-expanderHeader {
    background: #f9fafb !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA DICTIONARY & LOGIC
# ======================================================
SENSOR_DESCRIPTIONS = {
    "Motor RPM": "Viteza de rotație a arborelui cotit. Esențială pentru axa X în hărțile de tuning.",
    "Engine load": "Sarcina motorului. Indică volumul de aer raportat la capacitatea cilindrică.",
    "Air mass": "Cantitatea de aer absorbită (MAF).",
    "Ignition angle": "Momentul scânteii. Valorile mici indică retard cauzat de detonație.",
    "Injection time": "Durata deschiderii injectoarelor (ms).",
    "Knock sensor #1": "Detecție vibrații de detonație.",
    "Motor temp.": "Temperatura antigelului. Optim: 85-95°C.",
    "Oil temp.": "Temperatura uleiului. Peste 115°C necesită răcire.",
    "Battery voltage": "Tensiunea sistemului (Optim >13.5V)."
}

def safe_col(df, name):
    if name not in df.columns: df[name] = np.nan
    return df[name]

def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
    rpm = safe_col(df, 'Motor RPM').replace(0, np.nan)
    df['Inj_Duty'] = (safe_col(df, 'Injection time') * rpm) / 1200
    if 'Lambda #1 integrator ' in df.columns and 'Lambda #2 integrator' in df.columns:
        df['Lambda_Avg'] = (df['Lambda #1 integrator '] + df['Lambda #2 integrator']) / 2
    else:
        df['Lambda_Avg'] = safe_col(df, 'Lambda #1 integrator ')
    
    df['Knock_Peak'] = df[['Knock sensor #1', 'Knock sensor #2']].max(axis=1) if 'Knock sensor #2' in df.columns else safe_col(df, 'Knock sensor #1')
    df['WOT'] = (safe_col(df, 'Engine load') > 70) & (rpm > 3000)
    return df

def get_threshold_analysis(sensor, val, wot_active):
    # Praguri: (Min, Max, Unitate, Explicație)
    db = {
        'Inj_Duty': (0, 85, '%', "Peste 85%: Injectorul devine instabil termic și nu mai poate compensa debitul corect."),
        'Lambda_Avg': (0.78, 0.88, 'λ', "WOT Target: Sub 0.78 pierzi putere, peste 0.88 riști topirea evacuării."),
        'Knock_Peak': (0, 2.0, 'V', "Peste 2.0V: Unda de șoc a detonației lovește pistoanele. Pericol mecanic iminent."),
        'Oil temp.': (80, 115, '°C', "Peste 115°C: Uleiul își pierde vâscozitatea. Risc de gripare cuzineți."),
        'Battery voltage': (13.5, 14.7, 'V', "Sub 13.5V: Timpul de reacție al injectorului crește, sărăcind amestecul accidental.")
    }
    if sensor not in db: return "OK", "Parametru monitorizat.", "#4da3ff"
    min_v, max_v, unit, desc = db[sensor]
    if sensor == 'Lambda_Avg' and not wot_active: return "CRUISE", "Target 1.00 λ (Closed Loop). Amestec economic.", "#6b7280"
    if val > max_v: return "CRITICAL", desc, "#ef4444"
    if val < min_v: return "LOW", desc, "#f59e0b"
    return "OPTIM", "Funcționare în limitele de siguranță motorsport.", "#10b981"

# ======================================================
# MAIN APP
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTUNED ARCHITECT</h1>
        <p>Motorsport ECU Diagnostic Platform // v20.0</p>
    </div>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        file = st.file_uploader("📂 DRAG & DROP ECU LOG (.CSV)", type="csv")
    
    if not file:
        st.markdown("<div style='text-align:center; padding:50px; color:#6b7280; font-family:Orbitron;'>SYSTEM IDLE - WAITING FOR TELEMETRY DATA...</div>", unsafe_allow_html=True)
        return

    df = compute_channels(pd.read_csv(file, sep=';'))

    # 1. PERFORMANCE OVERVIEW
    st.markdown("<h2 class='section-title'>Performance Overview</h2>", unsafe_allow_html=True)
    k = st.columns(4)
    k[0].metric("MAX RPM", f"{int(df['Motor RPM'].max())}")
    k[1].metric("AIR MASS", f"{df['Air mass'].max():.1f}")
    k[2].metric("MAX INJ DUTY", f"{df['Inj_Duty'].max():.1f}%")
    k[3].metric("MAX KNOCK", f"{df['Knock_Peak'].max():.2f}V")

    # 2. EXPERT THRESHOLD INTELLIGENCE
    st.markdown("<h2 class='section-title'>Expert Threshold Intelligence</h2>", unsafe_allow_html=True)
    
    wot_status = not df[df['WOT']].empty
    sensors_to_check = {
        'Inj_Duty': df['Inj_Duty'].max(),
        'Lambda_Avg': df[df['WOT']]['Lambda_Avg'].mean() if wot_status else 1.0,
        'Knock_Peak': df['Knock_Peak'].max(),
        'Oil temp.': df['Oil temp.'].max(),
        'Battery voltage': df['Battery voltage'].min()
    }

    cols = st.columns(len(sensors_to_check))
    for i, (name, value) in enumerate(sensors_to_check.items()):
        status, info, color = get_threshold_analysis(name, value, wot_status)
        with cols[i]:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div class="status-tag" style="background:{color}; color:white;">{status}</div>
                <div style="font-size:11px; opacity:0.6; font-family:Orbitron;">{name.upper()}</div>
                <div style="font-size:28px; font-weight:700; margin:10px 0;">{value:.2f}</div>
                <div style="font-size:13px; line-height:1.4; color:#374151;">{info}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. SENSOR TRACE ANALYSIS
    st.markdown("<h2 class='section-title'>Sensor Trace Analysis</h2>", unsafe_allow_html=True)
    
    
    
    t_comb, t_flow, t_temp = st.tabs(["[ COMBUSTION ]", "[ FLOW ]", "[ THERMAL ]"])
    groups = {
        t_comb: ['Motor RPM', 'Ignition angle', 'Knock_Peak', 'Lambda_Avg'],
        t_flow: ['Air mass', 'Engine load', 'VE_Calculated'],
        t_temp: ['Motor temp.', 'Oil temp.', 'Battery voltage']
    }

    for tab, keys in groups.items():
        with tab:
            for c in keys:
                if c in df.columns:
                    with st.expander(f"SCAN CHANNEL: {c.upper()}"):
                        c1, c2 = st.columns([1, 2.5])
                        with c1:
                            st.markdown(f"<div class='sensor-card'><b>INFO:</b><br>{SENSOR_DESCRIPTIONS.get(c, 'Standard input.')}</div>", unsafe_allow_html=True)
                        with c2:
                            fig = px.line(df, y=c, template="plotly_white", color_discrete_sequence=['#4da3ff'])
                            fig.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=10))
                            st.plotly_chart(fig, use_container_width=True)

    # 4. RAW DATA
    st.markdown("<h2 class='section-title'>Full Telemetry Archive</h2>", unsafe_allow_html=True)
    with st.expander("ACCESS RAW DATASET"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    app()
