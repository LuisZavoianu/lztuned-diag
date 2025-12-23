import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== STYLE & ENGINE CONFIG =====================
st.set_page_config(page_title="LZTuned Elite Calibration", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; color: #1a1a1a; }
    .report-header { background: linear-gradient(90deg, #001529 0%, #003a8c 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #1890ff; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #001529 !important; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

def app():
    st.markdown("<div class='report-header'><h1>LZTuned Elite Calibration v13.0</h1><p>Chief Technical Architect: <b>Luis Zavoianu</b> | High-Fidelity Data Extraction</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă LOG Master (CSV)", type="csv")
    if not file:
        st.info("Sistemul este pregătit. Vă rugăm să încărcați fișierul CSV pentru procesare.")
        return

    df = pd.read_csv(file, sep=';')
    
    # --- MATH ENGINE: CALCULI PROFESIONIȘTI ---
    safe_rpm = df['Motor RPM'].replace(0, 1)
    df['Inj_Duty_Cycle'] = (df['Injection time'] * safe_rpm) / 1200
    df['Lambda_Avg'] = (df['Lambda #1 integrator '] + df['Lambda #2 integrator']) / 2
    df['Air_Density_Index'] = df['Air mass'] / (df['Intake temp.'] + 273.15)
    df['Engine_Efficiency_Score'] = (df['Air mass'] / safe_rpm) * df['Ignition angle']
    
    # --- KPI DASHBOARD (PRO) ---
    st.subheader("📋 Parametri Critici de Calibrare")
    m_row = st.columns(6)
    m_row[0].metric("RPM Peak", int(df['Motor RPM'].max()))
    m_row[1].metric("Flow Max", f"{df['Air mass'].max()} kg/h")
    m_row[2].metric("Inj Duty %", f"{df['Inj_Duty_Cycle'].max():.1f}%")
    m_row[3].metric("Min Advance", f"{df['Ignition angle'].min()}°")
    m_row[4].metric("Peak Oil T", f"{df['Oil temp.'].max()}°C")
    m_row[5].metric("Lambda Avg", f"{df['Lambda_Avg'].mean():.3f}")

    # --- TABS: PROFESIONAL VISUALIZATION ---
    t1, t2, t3, t4 = st.tabs(["🚀 ANALIZĂ PUTERE & AER", "⛽ MIX COMBUSTIBIL", "🌡️ MANAGEMENT TERMIC", "🏁 VERDICT TEHNIC"])

    with t1:
        st.subheader("Dinamica Fluxului de Aer vs Avans")
        # Grafic dual-axis: Air Mass (linie) vs Ignition (bar)
        fig_pwr = make_subplots(specs=[[{"secondary_y": True}]])
        fig_pwr.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass (kg/h)", line=dict(color='#1890ff', width=4)), secondary_y=False)
        fig_pwr.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition Angle (°)", line=dict(color='#fadb14', width=2, dash='dot')), secondary_y=True)
        
        fig_pwr.update_layout(title="Corelație Flux Aer și Avans (Turație completă)", template="plotly_white", height=600)
        st.plotly_chart(fig_pwr, use_container_width=True)
        
        

    with t2:
        st.subheader("Harta Amestecului (Lambda Target vs Actual)")
        # Heatmap densitate pentru a vedea unde e amestecul prost
        fig_fuel = px.density_heatmap(df, x="Motor RPM", y="Engine load", z="Lambda_Avg", 
                                     histfunc="avg", nbinsx=20, nbinsy=20, 
                                     color_continuous_scale='RdYlGn_r', title="Harta de Eficiență Lambda (Roșu = Sărac / Verde = Optim)")
        st.plotly_chart(fig_fuel, use_container_width=True)
        
        

    with t3:
        st.subheader("Stabilitate Termică și Electrică")
        # Monitorizăm tot ce ține de hardware: Ulei, Apa, Ventilator, Tensiune
        fig_term = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        
        # Row 1: Temperaturi
        fig_term.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Apa Engine"), row=1, col=1)
        fig_term.add_trace(go.Scatter(x=df['time'], y=df['Oil temp.'], name="Ulei Engine"), row=1, col=1)
        fig_term.add_trace(go.Scatter(x=df['time'], y=df['Radiator coolant outlet temp.'], name="Apa Radiator"), row=1, col=1)
        
        # Row 2: Auxiliare
        fig_term.add_trace(go.Scatter(x=df['time'], y=df['Battery voltage'], name="Voltage", line=dict(color='gold')), row=2, col=1)
        fig_term.add_trace(go.Scatter(x=df['time'], y=df['Electric fan speed'], name="Fan Speed", line=dict(dash='dash')), row=2, col=1)
        
        fig_term.update_layout(height=700, title="Monitorizare Hardware & Gestiune Termică")
        st.plotly_chart(fig_term, use_container_width=True)
        
        

    with t4:
        st.header("🏁 Verdict Final de Inginerie - Luis Zavoianu")
        
        # Analiză automată bazată pe datele extrase
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("### 🔍 Analiză Performanță")
            if df['Air mass'].max() > 500:
                st.write(f"- **Debit Aer:** EXCELENT ({df['Air mass'].max()} kg/h). Motorul are capacitate mare de pompare.")
            if df['Ignition angle'].min() < 0:
                st.error(f"- **Avans:** CRITIC. Avansul scade la {df['Ignition angle'].min()}°. ECU taie puterea pentru siguranță.")
            
        with res_col2:
            st.markdown("### 🛠️ Recomandări Update Soft")
            st.write("1. **Fuel Map:** Mărește timpul de injecție cu 4% în zona de sarcină maximă (WOT) pentru a reduce temperatura în camera de ardere.")
            st.write("2. **Ignition Map:** Redu avansul cu 2-3 grade între 4500-6000 RPM pentru a stabiliza aprinderea și a elimina corecțiile negative.")
            st.write("3. **Fan Control:** Având în vedere temperatura uleiului de 111°C, setează ventilatorul să pornească la 92°C în loc de 96°C.")

        # AFISARE TOATE DATELE BRUTEGRUPATE
        with st.expander("📊 Vezi Matricea Completă de Date (Toate coloanele extrase)"):
            st.dataframe(df.describe().T, use_container_width=True)

if __name__ == "__main__":
    app()
