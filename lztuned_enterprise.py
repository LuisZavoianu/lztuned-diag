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
# GLOBAL STYLE – LZTuned Motorsport Engineering
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0b0f14;
    color: #d1d7e0;
}

/* Header */
.header-box {
    background: linear-gradient(135deg, #050b14 0%, #0c1f3a 60%, #102c4a 100%);
    padding: 40px;
    border-radius: 18px;
    border: 1px solid #1f2a3a;
    margin-bottom: 40px;
    text-align: center;
}
.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 42px;
    letter-spacing: 2px;
    margin-bottom: 10px;
    color: #4da3ff;
}
.header-box p {
    font-size: 14px;
    letter-spacing: 1px;
    color: #9fb6d9;
}

/* Section titles */
.section-title {
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1.5px;
    color: #58a6ff;
    margin-bottom: 20px;
}

/* Cards */
.status-card {
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    border: 1px solid #263041;
    background: #0f1623;
}

.ok {
    border-left: 6px solid #1f9d55;
}
.warn {
    border-left: 6px solid #d29922;
}
.crit {
    border-left: 6px solid #da3633;
}

/* Sensor cards */
.sensor-card {
    background: #0f1623;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #263041;
    font-size: 13px;
    line-height: 1.5;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #0f1623;
    border: 1px solid #263041;
    padding: 16px;
    border-radius: 14px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
}

/* Expander */
details {
    border-radius: 12px;
    border: 1px solid #263041;
    background: #0f1623;
}

/* Plot background */
.js-plotly-plot {
    border-radius: 14px;
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

    file = st.file_uploader("Load ECU Log File (CSV)", type="csv")
    if not file:
        return

    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # ==================================================
    # KPI DASHBOARD
    # ==================================================
    st.markdown("<h2 class='section-title'>ENGINE PERFORMANCE OVERVIEW</h2>", unsafe_allow_html=True)
    k = st.columns(4)
    k[0].metric("MAX RPM", int(df['Motor RPM'].max()))
    k[1].metric("PEAK AIR MASS", f"{df['Air mass'].max():.1f}")
    k[2].metric("MAX INJ DUTY", f"{df['Inj_Duty'].max():.1f} %")
    k[3].metric("MIN IGNITION", f"{df['Ignition angle'].min():.1f} °")

    # ==================================================
    # VERDICT
    # ==================================================
    st.markdown("<h2 class='section-title'>SYSTEM VERDICT & SAFETY STATUS</h2>", unsafe_allow_html=True)
    for title, level, obs, action in get_diagnostics(df):
        cls = {"OK": "ok", "WARNING": "warn", "CRITICAL": "crit", "HARD LIMIT": "crit"}[level]
        st.markdown(f"""
        <div class="status-card {cls}">
            <h3>{title} — {level}</h3>
            <p><b>Observation:</b> {obs}</p>
            <p><b>Recommended Action:</b> {action}</p>
        </div>
        """, unsafe_allow_html=True)

    # ==================================================
    # SENSOR FORENSICS
    # ==================================================
    st.markdown("<h2 class='section-title'>SENSOR FORENSICS ANALYSIS</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["Combustion", "Airflow", "Thermal", "Electrical"])

    group_map = {
        0: ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Knock sensor #2', 'Lambda_Avg', 'Injection time'],
        1: ['Air mass', 'Engine load', 'Throttle position', 'VE_Calculated'],
        2: ['Motor temp.', 'Oil temp.', 'Intake temp.'],
        3: ['Battery voltage', 'Electric fan speed', 'Gear']
    }

    for tab, keys in zip(tabs, group_map.values()):
        with tab:
            for c in keys:
                if c in df.columns:
                    with st.expander(c):
                        c1, c2 = st.columns([1, 2])
                        c1.markdown(
                            f"<div class='sensor-card'><b>Description</b><br>{SENSOR_DESCRIPTIONS.get(c, 'Telemetry channel')}</div>",
                            unsafe_allow_html=True
                        )
                        c1.write(f"MAX: {df[c].max()} | MIN: {df[c].min()}")
                        fig = px.line(df, x='time', y=c, template="plotly_dark")
                        fig.update_layout(height=280, margin=dict(l=0, r=0, t=0, b=0))
                        c2.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # ADVANCED TELEMETRY
    # ==================================================
    st.markdown("<h2 class='section-title'>ADVANCED TELEMETRY & CORRELATION</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Multi-Channel Overlay", "Correlation Matrix"])

    with t1:
        selected = st.multiselect("Select channels:", all_cols, default=['Motor RPM', 'Ignition angle', 'Knock_Peak'])
        if selected:
            fig = make_subplots(rows=len(selected), cols=1, shared_xaxes=True)
            for i, s in enumerate(selected):
                fig.add_trace(go.Scatter(x=df['time'], y=df[s], name=s), row=i+1, col=1)
            fig.update_layout(height=180*len(selected), template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        st.plotly_chart(px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r"), use_container_width=True)

    # ==================================================
    # DATA TABLE
    # ==================================================
    with st.expander("FULL TELEMETRY DATASET"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    app()
