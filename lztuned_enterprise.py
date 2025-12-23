import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================================================
# CONFIG & STYLE
# ======================================================
st.set_page_config(page_title="LZTuned Ultimate v20.0", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header-box { 
        background: linear-gradient(135deg, #001529 0%, #0050b3 100%); 
        padding: 30px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 30px; text-align: center;
    }
    .status-card { padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #30363d; }
    .sensor-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .ok { background-color: #161b22; border-left: 6px solid #238636; }
    .warn { background-color: #2a2200; border-left: 6px solid #d29922; }
    .crit { background-color: #2d1616; border-left: 6px solid #da3633; }
    h1, h2, h3 { color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA DICTIONARY
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
# UTILS & DATA ENGINE
# =====================-=================================
def safe_col(df, name):
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
    # Curățare turație
    rpm = safe_col(df, 'Motor RPM').replace(0, np.nan)
    
    # Calcule derivate
    df['Inj_Duty'] = (safe_col(df, 'Injection time') * rpm) / 1200
    df['Lambda_Avg'] = (safe_col(df, 'Lambda #1 integrator ') + safe_col(df, 'Lambda #2 integrator')) / 2
    df['VE_Calculated'] = (safe_col(df, 'Air mass') * 100) / (rpm * 0.16 + 1)
    df['Knock_Peak'] = df[['Knock sensor #1', 'Knock sensor #2']].max(axis=1)
    
    # Identificare WOT (Wide Open Throttle)
    df['WOT'] = (safe_col(df, 'Engine load') > 70) & (rpm > 3000)
    
    return df

# ===================== ANALYSIS =====================
def get_diagnostics(df):
    wot = df[df['WOT']]
    reports = []
    
    # Fuel
    duty_max = df['Inj_Duty'].max()
    lambda_wot = wot['Lambda_Avg'].mean() if not wot.empty else 0
    if duty_max > 90:
        reports.append(("⛽ BENZINĂ", "HARD LIMIT", f"Duty Cycle la {duty_max:.1f}%", "Injectoare prea mici. Upgrade necesar."))
    elif lambda_wot > 0.88:
        reports.append(("⛽ BENZINĂ", "CRITICAL", f"Lambda WOT {lambda_wot:.2f} (Sărac)", "Risc de topire pistoane. Îmbogățește amestecul."))
    else:
        reports.append(("⛽ BENZINĂ", "OK", "Amestec optim în sarcină.", "Nu sunt necesare corecții."))

    # Ignition/Knock
    k_peak = df['Knock_Peak'].max()
    if k_peak > 2.2:
        reports.append(("⚡ APRINDERE", "CRITICAL", f"Knock Peak detectat: {k_peak:.2f}V", "Detonație activă! Scade avansul cu 2-4 grade."))
    else:
        reports.append(("⚡ APRINDERE", "OK", "Fără detonații periculoase.", "Avansul este sigur."))

    # Thermal
    oil = df['Oil temp.'].max()
    if oil > 112:
        reports.append(("🌡️ TERMIC", "WARNING", f"Ulei la {oil:.1f}°C", "Răcire ineficientă sub sarcină prelungită."))
    else:
        reports.append(("🌡️ TERMIC", "OK", "Temperaturi stabile.", "Sistem de răcire nominal."))

    return reports

# ======================================================
# APP RENDER
# ======================================================
def app():
    st.markdown("""<div class="header-box"><h1>LZTuned Architect Ultimate v20.0</h1>
    <p>Sistem Expert de Diagnostic & Forensics | Lead: <b>Luis Zavoianu</b></p></div>""", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă LOG ECU (CSV)", type="csv")
    if not file: return

    # Load & Process
    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # 1. KPI DASHBOARD
    st.header("💎 Engine Master KPIs")
    k = st.columns(4)
    k[0].metric("RPM Max", int(df['Motor RPM'].max()))
    k[1].metric("Peak Air Mass", f"{df['Air mass'].max():.1f}")
    k[2].metric("Max Inj Duty", f"{df['Inj_Duty'].max():.1f}%")
    k[3].metric("Min Ignition", f"{df['Ignition angle'].min():.1f}°")

    st.markdown("---")

    # 2. RAPORT DIAGNOSTIC (Verdicte)
    st.header("🏁 Verdict Tuning & Siguranță")
    diag_results = get_diagnostics(df)
    for title, level, obs, action in diag_results:
        cls = {"OK": "ok", "WARNING": "warn", "CRITICAL": "crit", "HARD LIMIT": "crit"}[level]
        st.markdown(f"""<div class="status-card {cls}"><h3>{title} — {level}</h3>
        <p><b>Observație:</b> {obs}</p><p><b>Acțiune:</b> {action}</p></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 3. SENSOR FORENSICS (Explicații și Grafice Individuale)
    st.header("🔍 Sensor Forensics Explorer")
    tabs = st.tabs(["🔥 Combustie", "🌬️ Aer & Boost", "🌡️ Management Termic", "🔋 Hardware"])
    
    group_map = {
        0: ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Knock sensor #2', 'Lambda_Avg', 'Injection time'],
        1: ['Air mass', 'Engine load', 'Throttle position', 'VE_Calculated'],
        2: ['Motor temp.', 'Oil temp.', 'Intake temp.'],
        3: ['Battery voltage', 'Electric fan speed', 'Gear']
    }

    for i, (tab, keys) in enumerate(zip(tabs, group_map.values())):
        with tab:
            for c in keys:
                if c in df.columns:
                    with st.expander(f"📊 {c} Details"):
                        c1, c2 = st.columns([1, 2])
                        desc = SENSOR_DESCRIPTIONS.get(c, "Senzor specific identificat în telemetrie.")
                        c1.markdown(f"<div class='sensor-card'><b>Rol:</b><br>{desc}</div>", unsafe_allow_html=True)
                        c1.write(f"**Max:** {df[c].max()} | **Min:** {df[c].min()}")
                        fig = px.line(df, x='time', y=c, color_discrete_sequence=['#58a6ff'])
                        fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
                        c2.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 4. MULTI-CHANNEL & CORRELATION
    st.header("📈 Advanced Telemetry Analysis")
    t_overlay, t_corr = st.tabs(["Multi-Channel Overlay", "Correlation Matrix"])
    
    with t_overlay:
        selected = st.multiselect("Suprapune senzori pentru analiză:", all_cols, default=['Motor RPM', 'Ignition angle', 'Knock_Peak'])
        if selected:
            fig_multi = make_subplots(rows=len(selected), cols=1, shared_xaxes=True, vertical_spacing=0.02)
            for j, s in enumerate(selected):
                fig_multi.add_trace(go.Scatter(x=df['time'], y=df[s], name=s), row=j+1, col=1)
            fig_multi.update_layout(height=180*len(selected), template="plotly_dark")
            st.plotly_chart(fig_multi, use_container_width=True)

    with t_corr:
        corr = df.select_dtypes(include=[np.number]).corr()
        st.plotly_chart(px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r'), use_container_width=True)

    # 5. DATA TABLE
    st.markdown("---")
    with st.expander("📄 Full Data Table"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    app()
