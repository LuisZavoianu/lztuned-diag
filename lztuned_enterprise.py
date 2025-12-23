import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ======================================================
# CONFIG & THEME
# ======================================================
st.set_page_config(
    page_title="LZTuned Universal Diagnostic v16.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stiluri rafinate pentru un aspect de software profesional
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    .section-box {
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .section-box:hover { transform: scale(1.01); }
    .ok { border-left: 6px solid #238636; background: rgba(35, 134, 54, 0.1); }
    .warn { border-left: 6px solid #d29922; background: rgba(210, 153, 34, 0.1); }
    .crit { border-left: 6px solid #da3633; background: rgba(218, 54, 51, 0.1); }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Inter', sans-serif; }
    .metric-container { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# UTILS & SAFE HANDLERS
# ======================================================
def col(df, name):
    if name not in df.columns:
        # Încearcă să curețe numele coloanei (strip spaces)
        cleaned_cols = {c.strip(): c for c in df.columns}
        if name.strip() in cleaned_cols:
            return df[cleaned_cols[name.strip()]]
        df[name] = 0
    return df[name]

def load_data(file):
    # Detecție automată separator
    try:
        content = file.getvalue().decode('utf-8')
        sep = ';' if content.count(';') > content.count(',') else ','
        file.seek(0)
        return pd.read_csv(file, sep=sep)
    except Exception as e:
        st.error(f"Eroare la citirea fișierului: {e}")
        return None

# ======================================================
# CORE ENGINES (Derived & Analysis)
# ======================================================
def compute_derived(df):
    rpm = col(df, 'Motor RPM').replace(0, np.nan)
    load = col(df, 'Engine load')
    
    df['RPM_SAFE'] = rpm
    df['LOAD'] = load

    # Fuel & Air - Analiză profundă
    df['Inj_Duty'] = (col(df, 'Injection time') * rpm) / 1200
    df['Lambda_Avg'] = (col(df, 'Lambda #1 integrator ') + col(df, 'Lambda #2 integrator')) / 2
    # VE estimat (Volumetric Efficiency)
    df['VE'] = (col(df, 'Air mass') * 100) / (rpm * 0.16 + 1)

    # Ignition & Knock
    df['Ign_Stability'] = col(df, 'Ignition angle').rolling(10).std()
    df['Knock_Peak'] = df[['Knock sensor #1', 'Knock sensor #2']].max(axis=1)

    # Thermal & Electrical
    df['Thermal_Load'] = col(df, 'Oil temp.') * 0.6 + col(df, 'Motor temp.') * 0.4
    df['Volt_Sag'] = col(df, 'Battery voltage').max() - col(df, 'Battery voltage')

    # Mapping zones pentru tuning specific
    conditions = [
        (rpm < 1200) & (load < 25),
        (rpm.between(1500, 4000)) & (load < 50),
        (load > 75),
        (load < 5)
    ]
    df['ZONE'] = np.select(conditions, ['IDLE', 'CRUISE', 'WOT', 'OVERRUN'], default='TRANSIENT')
    return df

def evaluate_systems(df):
    report = []
    wot = df[df['ZONE'] == 'WOT']
    
    # 1. FUEL SYSTEM
    if not wot.empty and wot['Inj_Duty'].max() > 90:
        report.append(("⛽ Fuel System", "CRITICAL", f"Duty Cycle {wot['Inj_Duty'].max():.1f}%", "Upgrade injectoare sau pompă."))
    elif not wot.empty and wot['Lambda_Avg'].mean() > 0.88:
        report.append(("⛽ Fuel System", "WARNING", "Amestec sărac la Full Load.", "Crește valorile în hărțile de bază."))
    else:
        report.append(("⛽ Fuel System", "OK", "Mix stabil.", "Nu necesită corecții."))

    # 2. IGNITION
    if df['Knock_Peak'].max() > 2.0:
        report.append(("⚡ Ignition", "CRITICAL", f"Detonații: {df['Knock_Peak'].max():.2f}V", "Redu avansul imediat în zonele de sarcină."))
    else:
        report.append(("⚡ Ignition", "OK", "Fără detonații critice.", "Parametri siguri."))

    # 3. THERMAL
    if df['Thermal_Load'].max() > 108:
        report.append(("🌡️ Thermal", "CRITICAL", f"Peak: {df['Thermal_Load'].max():.1f}°C", "Verifică răcirea sau redu boost-ul."))
    else:
        report.append(("🌡️ Thermal", "OK", "Gestiune termică bună.", "Sistem în parametri."))

    # 4. ELECTRICAL
    if df['Volt_Sag'].max() > 1.2:
        report.append(("🔋 Electrical", "WARNING", f"Drop: {df['Volt_Sag'].max():.2f}V", "Verifică alternatorul și conexiunile."))
    else:
        report.append(("🔋 Electrical", "OK", "Tensiune stabilă.", "Sănătate electrică optimă."))

    return report

# ======================================================
# UI COMPONENTS
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTuned Universal Diagnostic v16.0</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Official Automotive Intelligence Platform</p>
        <code style='background: rgba(0,0,0,0.3); padding: 5px 10px; border-radius: 5px;'>Lead Engineer: Luis Zavoianu</code>
    </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader("Încarcă fișierul LOG (.csv)", type="csv")
    if not file:
        st.info("👋 Bine ai venit, Luis! Încarcă un log pentru a începe analiza.")
        return

    df = load_data(file)
    if df is None: return
    df = compute_derived(df)
    report = evaluate_systems(df)
    
    # Scoring
    score = 100
    for _, lvl, _, _ in report:
        if lvl == "WARNING": score -= 10
        if lvl == "CRITICAL": score -= 25
    score = max(score, 0)

    # Dashboard Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Overall Health", f"{score}%")
    with m2: st.metric("Peak RPM", f"{int(df['Motor RPM'].max())}")
    with m3: st.metric("Max Air", f"{df['Air mass'].max():.1f} kg/h")
    with m4: st.metric("Max Duty", f"{df['Inj_Duty'].max():.1f}%")
    with m5: st.metric("Min Ign", f"{df['Ignition angle'].min()}°")

    st.markdown("---")
    
    # Report Section
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.header("📋 Diagnostic Results")
        for t, lvl, o, a in report:
            cls = {"OK":"ok","WARNING":"warn","CRITICAL":"crit"}[lvl]
            st.markdown(f"""
            <div class="section-box {cls}">
                <h3 style='margin:0;'>{t}</h3>
                <p style='margin:5px 0;'><b>Status:</b> {lvl}</p>
                <small><b>Obs:</b> {o}</small><br>
                <small><b>Plan:</b> {a}</small>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.header("📈 Live Telemetry")
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='#3b82f6')), 1, 1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Lambda_Avg'], name="Lambda", line=dict(color='#10b981')), 2, 1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition", line=dict(color='#f59e0b')), 3, 1)
        
        fig.update_layout(height=600, template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Deep Data View
    with st.expander("🔍 Vezi datele brute și statistici"):
        st.dataframe(df.describe().T, use_container_width=True)

    # Export
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("📥 Descarcă Raportul Procesat (.csv)", data=csv_buf.getvalue(), file_name="lztuned_processed_log.csv")

if __name__ == "__main__":
    app()
