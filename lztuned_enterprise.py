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
# REFINED UX STYLE – LZTuned Motorsport Engineering
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

/* Main Container Optimization */
.main { background-color: #0b0f14; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #d1d7e0;
}

/* Glassmorphism Header */
.header-box {
    background: linear-gradient(135deg, rgba(16, 44, 74, 0.9) 0%, rgba(5, 11, 20, 0.9) 100%);
    padding: 50px 20px;
    border-radius: 20px;
    border: 1px solid rgba(77, 163, 255, 0.2);
    margin-bottom: 45px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(24px, 5vw, 48px);
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 15px;
    background: linear-gradient(90deg, #4da3ff, #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-box p {
    font-size: 16px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #9fb6d9;
    opacity: 0.8;
}

/* Section Titles with Accent Line */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px;
    letter-spacing: 2px;
    color: #58a6ff;
    margin: 40px 0 25px 0;
    padding-left: 15px;
    border-left: 4px solid #58a6ff;
}

/* Modernized Status Cards */
.status-card {
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 20px;
    background: #0f1623;
    border: 1px solid #1f2a3a;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.status-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}
.status-card h3 { 
    margin-top: 0; 
    font-family: 'Orbitron', sans-serif; 
    font-size: 18px;
}

.ok { border-left: 8px solid #1f9d55; box-shadow: inset 10px 0 20px -10px rgba(31, 157, 85, 0.2); }
.warn { border-left: 8px solid #d29922; box-shadow: inset 10px 0 20px -10px rgba(210, 153, 34, 0.2); }
.crit { border-left: 8px solid #da3633; box-shadow: inset 10px 0 20px -10px rgba(218, 54, 51, 0.2); }

/* KPI Metrics Styling */
[data-testid="stMetric"] {
    background: rgba(15, 22, 35, 0.7);
    border: 1px solid #263041;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}
[data-testid="stMetricLabel"] { font-family: 'Orbitron', sans-serif; color: #9fb6d9 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #fff !important; font-weight: 700 !important; }

/* Tabs UX */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', sans-serif;
    background-color: #0f1623;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    color: #9fb6d9;
}
.stTabs [aria-selected="true"] { background-color: #1f2a3a !important; color: #58a6ff !important; }

/* Better Expanders */
.streamlit-expanderHeader {
    background-color: #0f1623 !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}
.sensor-card {
    background: #1a2332;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303e54;
    font-size: 14px;
    color: #d1d7e0;
}

/* File Uploader Customization */
section[data-testid="stFileUploader"] {
    background-color: #0f1623;
    border: 2px dashed #263041;
    border-radius: 16px;
    padding: 20px;
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
        <h1>LZTuned Architect Ultimate</h1>
        <p>MOTORSPORT ECU DIAGNOSTIC PLATFORM<br>
        Engineered by <b>Luis Zavoianu</b> · Application Engineer</p>
    </div>
    """, unsafe_allow_html=True)

    # Centered File Uploader
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        file = st.file_uploader("Upload ECU Log File (CSV)", type="csv")
    
    if not file:
        st.info("Waiting for telemetry data... Please upload a CSV log file.")
        return

    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # KPI DASHBOARD
    st.markdown("<h2 class='section-title'>ENGINE PERFORMANCE OVERVIEW</h2>", unsafe_allow_html=True)
    k = st.columns(4)
    k[0].metric("MAX RPM", f"{int(df['Motor RPM'].max())} 🏁")
    k[1].metric("PEAK AIR MASS", f"{df['Air mass'].max():.1f} kg/h")
    k[2].metric("MAX INJ DUTY", f"{df['Inj_Duty'].max():.1f} %")
    k[3].metric("MIN IGNITION", f"{df['Ignition angle'].min():.1f} °")

# ==================================================
    # VERDICT & CRITICAL ALERTS
    # ==================================================
    st.markdown("<h2 class='section-title'>SYSTEM VERDICT & SAFETY STATUS</h2>", unsafe_allow_html=True)
    
    # Stil special pentru alertele critice
    st.markdown("""
    <style>
    .alert-container {
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        display: flex;
        flex-direction: column;
        gap: 10px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.3);
    }
    .alert-critical {
        background: linear-gradient(90deg, #660000 0%, #cc0000 100%);
        border: 2px solid #ff4d4d;
    }
    .alert-warning {
        background: linear-gradient(90deg, #664400 0%, #cc8800 100%);
        border: 2px solid #ffcc00;
    }
    .alert-ok {
        background: linear-gradient(90deg, #0d2b16 0%, #1f5c33 100%);
        border: 2px solid #33cc66;
    }
    .alert-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 5px;
    }
    .alert-body { font-size: 16px; line-height: 1.4; }
    .alert-action { 
        background: rgba(255,255,255,0.15); 
        padding: 10px; 
        border-radius: 8px; 
        font-weight: 600; 
        border: 1px dashed white;
    }
    </style>
    """, unsafe_allow_html=True)

    diagnostics = get_diagnostics(df)
    
    for title, level, obs, action in diagnostics:
        # Mapare stiluri
        if level in ["CRITICAL", "HARD LIMIT"]:
            alert_class = "alert-critical"
            icon = "🛑"
        elif level == "WARNING":
            alert_class = "alert-warning"
            icon = "⚠️"
        else:
            alert_class = "alert-ok"
            icon = "✅"

        st.markdown(f"""
        <div class="alert-container {alert_class}">
            <div class="alert-header">{icon} {title} — {level}</div>
            <div class="alert-body">
                <b>OBSERVAȚIE:</b> {obs}
            </div>
            <div class="alert-action">
                👉 ACȚIUNE: {action}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # SENSOR FORENSICS
    st.markdown("<h2 class='section-title'>SENSOR FORENSICS ANALYSIS</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["🔥 Combustion", "🌬️ Airflow", "🌡️ Thermal", "🔋 Electrical"])

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
                    with st.expander(f"📊 DATA CHANNEL: {c.upper()}"):
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.markdown(f"<div class='sensor-card'>{SENSOR_DESCRIPTIONS.get(c, 'Telemetry channel')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align:center; padding-top:10px'><b>RANGE:</b> {df[c].min()} — {df[c].max()}</p>", unsafe_allow_html=True)
                        with c2:
                            fig = px.line(df, x='time', y=c, template="plotly_dark", color_discrete_sequence=['#4da3ff'])
                            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=10), 
                                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                              xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#263041'))
                            st.plotly_chart(fig, use_container_width=True)

    # ADVANCED TELEMETRY
    st.markdown("<h2 class='section-title'>ADVANCED TELEMETRY & CORRELATION</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["📈 Multi-Channel Overlay", "🧬 Correlation Matrix"])

    with t1:
        selected = st.multiselect("Select channels to compare:", all_cols, default=['Motor RPM', 'Ignition angle', 'Knock_Peak'])
        if selected:
            fig = make_subplots(rows=len(selected), cols=1, shared_xaxes=True, vertical_spacing=0.05)
            for i, s in enumerate(selected):
                fig.add_trace(go.Scatter(x=df['time'], y=df[s], name=s, line=dict(width=2)), row=i+1, col=1)
            fig.update_layout(height=200*len(selected), template="plotly_dark", showlegend=False,
                              margin=dict(l=0, r=0, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
        fig_corr.update_layout(height=600, template="plotly_dark")
        st.plotly_chart(fig_corr, use_container_width=True)

    # DATA TABLE
    st.markdown("<h2 class='section-title'>RAW TELEMETRY ACCESS</h2>", unsafe_allow_html=True)
    with st.expander("VIEW FULL DATASET"):
        st.dataframe(df.style.background_gradient(cmap='Blues', subset=['Air mass']).format(precision=2), use_container_width=True)

if __name__ == "__main__":
    app()

