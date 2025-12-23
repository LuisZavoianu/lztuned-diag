import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE INTERFAȚĂ HIGH-TECH ---
st.set_page_config(page_title="LZTuned Apex Predator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .report-header { background-color: #1B1E23; padding: 20px; border-radius: 10px; border-bottom: 3px solid #00D1FF; margin-bottom: 25px; }
    h1, h2, h3 { color: #00D1FF !important; font-family: 'Orbitron', sans-serif; }
    .stMetric { background-color: #161A1D; border: 1px solid #30363D; padding: 15px; border-radius: 10px; }
    .stTab { background-color: #0E1117 !important; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_apex():
    st.markdown("<div class='report-header'><h1>LZTuned Apex Predator v4.0</h1><p>Lead Systems Engineer: <b>Luis Zavoianu</b> | High-Performance Telemetry</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă Log Master (Pro Level CSV)", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- MOTOR DE CALCUL ENGINE DYNAMICS (MATH CHANNELS) ---
        # 1. Virtual Dyno (HP & Torque estimat prin Masa Aer & Randament Volumic)
        df['Engine_Load_Norm'] = df['Engine load'] / 100
        df['Est_HP'] = (df['Air mass'] / 1.18) * (1 + (df['Ignition angle'] * 0.01))
        df['Est_Torque'] = (df['Est_HP'] * 5252) / df['Motor RPM'].replace(0, 1)
        
        # 2. Burn Speed & Stability (Calculat prin derivata avansului)
        df['Spark_Advance_Rate'] = df['Ignition angle'].diff() / df['time'].diff()
        
        # 3. Analiză Gaze (Lambda Error & Balance)
        df['Target_Lambda'] = 0.85 # Valoare ideală estimată pentru sarcină
        df['Lambda_Dev_B1'] = df['Lambda #1 integrator '] - df['Target_Lambda']
        
        # 4. Thermal Stress Index (TSI)
        df['Thermal_Stress'] = (df['Oil temp.'] * 0.6) + (df['Motor temp.'] * 0.4)
        
        # 5. Volumetric Efficiency Approximation
        df['VE_Calculated'] = (df['Air mass'] * 287.05 * (df['Intake temp.'] + 273.15)) / (101325 * (df['Motor RPM']/60) * 0.002) # Calculat pentru 2.0L

        # --- DASHBOARD DE METRICE CRITICE ---
        st.write("### 💎 Telemetrie Peak Performance")
        m_cols = st.columns(6)
        m_cols[0].metric("Virtual HP Peak", f"{round(df['Est_HP'].max(), 1)} HP")
        m_cols[1].metric("Virtual Torque", f"{round(df['Est_Torque'].max(), 1)} Nm")
        m_cols[2].metric("Max VE (%)", f"{round(df['VE_Calculated'].max(), 1)}%")
        m_cols[3].metric("TSI (Stress)", f"{round(df['Thermal_Stress'].max(), 1)}")
        m_cols[4].metric("G-Force Est.", f"{round(df['Speed'].diff().max() / 9.8, 2)} G")
        m_cols[5].metric("Battery SOH", f"{round(df['Battery voltage'].mean(), 2)}V")

        # --- MODULE ANALIZĂ AVANSATĂ ---
        tabs = st.tabs(["🏎️ DYNAMOMETER", "🌪️ AIR & VE FLOW", "🔥 COMBUSTION", "❄️ THERMAL DYNAMICS", "📊 OMNI-DATA MATRIX"])

        with tabs[0]:
            st.subheader("Virtual Dyno & Acceleration Analysis")
            fig_dyno = make_subplots(specs=[[{"secondary_y": True}]])
            fig_dyno.add_trace(go.Scatter(x=df['Motor RPM'], y=df['Est_HP'], name="Power (HP)", line=dict(color='#00D1FF', width=4)), secondary_y=False)
            fig_dyno.add_trace(go.Scatter(x=df['Motor RPM'], y=df['Est_Torque'], name="Torque (Nm)", line=dict(color='#FF4B4B', width=2, dash='dot')), secondary_y=True)
            fig_dyno.update_layout(title="Curba de Putere Estimată (Math Channels)", template="plotly_dark")
            st.plotly_chart(fig_dyno, use_container_width=True)

        with tabs[1]:
            st.subheader("Eficiență Volumetrică & Flux de Aer")
            # Vizualizare 3D a modului în care motorul "trage" aer
            fig_3d_air = px.scatter_3d(df, x='Motor RPM', y='Engine load', z='Air mass', color='VE_Calculated',
                                     title="3D Airflow Mapping (RPM vs Load vs Flow)")
            st.plotly_chart(fig_3d_air, use_container_width=True)

        with tabs[2]:
            st.subheader("Combustion Stability & Knock Analysis")
            c1, c2 = st.columns(2)
            with c1:
                # Corelație Ignition vs Knock retard
                fig_ign = px.scatter(df, x="time", y="Ignition angle", size="Knock sensor #1", color="Knock sensor #1",
                                    color_continuous_scale='Reds', title="Spark Stability vs Knock Activity")
                st.plotly_chart(fig_ign, use_container_width=True)
            with c2:
                # Analiză Timp Injecție vs RPM
                fig_inj = px.histogram(df, x="Injection time", nbins=50, title="Distribuția Timpului de Injecție (Duty Cycle Stress)")
                st.plotly_chart(fig_inj, use_container_width=True)

        with tabs[3]:
            st.subheader("Thermodynamic Exchange (Engine vs Radiator)")
            fig_heat = go.Figure()
            fig_heat.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Engine Exit Temp", line=dict(color='red')))
            fig_heat.add_trace(go.Scatter(x=df['time'], y=df['Radiator coolant outlet temp.'], name="Radiator Exit Temp", line=dict(color='blue')))
            fig_heat.add_trace(go.Scatter(x=df['time'], y=df['Intake temp.'], name="Intake Air Temp", fill='tonexty'))
            fig_heat.update_layout(title="Thermal Management Over Time", template="plotly_dark")
            st.plotly_chart(fig_heat, use_container_width=True)

        with tabs[4]:
            st.subheader("Omniscience Data Matrix")
            # Afișăm TOATE datele corelate
            corr_matrix = df.corr()
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='Viridis')
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.write("### Master Table (Full Stats)")
            st.dataframe(df.describe().T, use_container_width=True)

        # --- INSIGHT-URI GENERATE AUTOMAT (EXPERT SYSTEM) ---
        st.markdown("### 📜 Raport de Inginerie - Luis Zavoianu")
        with st.expander("VEZI DETALII ANALIZĂ AVANSATĂ", expanded=True):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.write("**Sistemul de Aer:**")
                st.write(f"- Eficiență Peak: {round(df['VE_Calculated'].max(), 2)}%")
                st.write(f"- Viteza Aerului: {'Optimă' if df['Air mass'].max() > 150 else 'Scăzută (Verificați Turbo/Admisie)'}")
            with r_col2:
                st.write("**Stabilitate Electrică:**")
                st.write(f"- Variație Tensiune: {round(df['Battery voltage'].std(), 4)}V")
                st.write(f"- Lambda Balance: {'Perfect' if df['Lambda_Diff'].mean() < 0.02 else 'Dezechilibrat'}")

        st.markdown("---")
        st.write(f"**LZTuned Apex Predator** | Build: 2025.Elite | Lead: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_apex()
