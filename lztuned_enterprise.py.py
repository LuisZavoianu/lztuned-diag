import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURARE INTERFAȚĂ ---
st.set_page_config(page_title="LZTuned Enterprise Diagnostic", layout="wide", page_icon="📈")

# Stil vizual pe fundal alb cu text contrastant (negru/albastru închis)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stMetricValue"] { color: #007BFF !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #555555 !important; }
    .stAlert { background-color: #F8F9FA; border: 1px solid #DEE2E6; color: #212529; }
    h1, h2, h3 { color: #0D1B2A !important; border-bottom: 2px solid #007BFF; padding-bottom: 10px; }
    .footer { text-align: right; color: #6C757D; font-style: italic; margin-top: 50px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #F1F3F5; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #495057 !important; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #007BFF !important; background-color: #E9ECEF; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_enterprise_analyzer():
    st.title("📊 LZTuned Enterprise Telemetry System")
    st.write("**Software de Analiză Tehnică de Înaltă Rezoluție** | Lead Engineer: **Luis Zavoianu**")

    file = st.file_uploader("Încărcați fișierul de date CSV", type="csv")

    if file:
        # Citim datele cu separatorul specific
        df = pd.read_csv(file, sep=';')
        
        # --- LOGICA DE CALCUL TOTALĂ (26 PARAMETRI) ---
        # Calculăm eficiența ventilatorului în funcție de temperatura lichidului
        df['Fan_Efficiency'] = (df['Electric fan speed'] * (df['Motor temp.'] - df['Radiator coolant outlet temp.'])) / 100
        # Calculăm sarcina reală a alternatorului
        df['Volt_Stability'] = df['Battery voltage'].rolling(window=5).std()
        
        # --- HEADER: KPI DASHBOARD ---
        st.subheader("📍 Indicatori de Performanță Critici")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("RPM Maxim", f"{int(df['Motor RPM'].max())}")
        m2.metric("Sarcina Peak", f"{df['Engine load'].max()}%")
        m3.metric("Masa Aer", f"{df['Air mass'].max()} kg/h")
        m4.metric("Temp Ulei", f"{df['Oil temp.'].max()}°C")
        m5.metric("Ignition Min", f"{df['Ignition angle'].min()}°")
        m6.metric("Viteză Max", f"{df['Speed'].max()} km/h")

        # --- TABS: STRUCTURĂ DATE ---
        t1, t2, t3, t4, t5 = st.tabs([
            "📈 Grafice Telemetrie", 
            "🌡️ Management Termic & Flux", 
            "⚡ Electric & Injecție", 
            "📝 Rezoluție Completă", 
            "📋 Tabel Date High-Res"
        ])

        with t1:
            st.write("### Analiză Dinamică: Putere vs. Aprindere")
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
            
            # Subplot 1: RPM, Viteza, Load
            fig.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="Motor RPM", line=dict(color='#007BFF')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Speed'], name="Viteză (km/h)", line=dict(color='#28A745')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Engine load'], name="Load %", line=dict(color='#6C757D', dash='dot')), row=1, col=1)
            
            # Subplot 2: Ignition & Knock
            fig.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition Angle", line=dict(color='#DC3545', width=3)), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock S1 (V)", line=dict(color='#FFC107')), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #2'], name="Knock S2 (V)", line=dict(color='#6F42C1')), row=2, col=1)
            
            fig.update_layout(height=700, template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            st.write("### Management Termic și Admisie")
            c1, c2 = st.columns(2)
            with c1:
                fig_t = go.Figure()
                fig_t.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Apa Motor", line=dict(color='blue')))
                fig_t.add_trace(go.Scatter(x=df['time'], y=df['Radiator coolant outlet temp.'], name="Ieșire Radiator", line=dict(color='cyan')))
                fig_t.add_trace(go.Scatter(x=df['time'], y=df['Oil temp.'], name="Ulei", line=dict(color='red')))
                st.plotly_chart(fig_t, use_container_width=True)
            with c2:
                st.write("**Eficiență Admisie:**")
                st.write(f"- Temp. Admisie (IAT): {df['Intake temp.'].max()}°C")
                st.write(f"- Throttle Position: {df['Throttle pos.'].max()}%")
                st.write(f"- Debit Aer Max: {df['Air mass'].max()} kg/h")

        with t3:
            st.write("### Sisteme Electrice și Control Injecție")
            col_el1, col_el2 = st.columns(2)
            with col_el1:
                st.write("**Sistem Lambda (Integratori):**")
                st.write(f"- Bank 1 Avg: {round(df['Lambda #1 integrator '].mean(), 3)}")
                st.write(f"- Bank 2 Avg: {round(df['Lambda #2 integrator'].mean(), 3)}")
                st.write(f"- Heating Pre-cat 1: {df['Lambda #1 pre-cat heating'].max()}%")
                st.write(f"- Heating Pre-cat 2: {df['Lambda #2 pre-cat heating'].max()}%")
            with col_el2:
                st.write("**Injecție & Idle:**")
                st.write(f"- Timp Injecție Peak: {df['Injection time'].max()} ms")
                st.write(f"- Idle Speed Controller: {df['Idle speed controller'].max()}")
                st.write(f"- Battery Voltage Min: {df['Battery voltage'].min()} V")

        with t4:
            st.header("📋 Rezoluție Tehnică LZTuned")
            
            # Evaluare Automată
            res_score = 100
            
            if df['Ignition angle'].min() < 0:
                st.error("⚠️ **CRITIC: DETONAȚIE DETECTATĂ** - Unghiul de aprindere negativ indică o retragere masivă a avansului. Cauză probabilă: benzină neconformă sau supraîncălzire cameră ardere.")
                res_score -= 30
            
            if df['Oil temp.'].max() > 110:
                st.warning("⚠️ **TERMIC: ALERTĂ ULEI** - Temperatura uleiului a depășit 110°C. Rezoluție: Verificați fluxul de aer prin radiatorul de ulei.")
                res_score -= 10
            
            if df['Battery voltage'].min() < 13.5:
                st.error("⚠️ **ELECTRIC: INSTABILITATE** - Voltajul a scăzut sub pragul de încărcare nominală. Rezoluție: Verificați alternatorul și masa caroseriei.")
                res_score -= 15

            st.metric("SCOR SĂNĂTATE MOTOR", f"{max(0, res_score)}/100")
            
            st.info(f"**Notă Inginer:** Analiza celor {len(df)} rânduri de date confirmă starea curentă a vehiculului. Se recomandă monitorizarea senzorilor de knock la următoarea sesiune.")

        with t5:
            st.write("### Tabel Telemetrie - Rezoluție Completă")
            # Colorăm rândurile problematice
            def highlight_issues(val):
                color = 'red' if val < 0 else 'black'
                return f'color: {color}'

            st.dataframe(df.style.applymap(highlight_issues, subset=['Ignition angle']), height=600)

        # --- FOOTER PERSONALIZAT ---
        st.markdown(f"<div class='footer'>LZTuned Professional Software Solutions<br>Lead Project Engineer: Luis Zavoianu</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    lztuned_enterprise_analyzer()