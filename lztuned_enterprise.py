import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE BRANDING & VIZUAL ---
st.set_page_config(page_title="LZTuned The Singularity", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .metric-box { background-color: #f0f2f6; border-radius: 10px; padding: 15px; border-top: 4px solid #0047AB; }
    .status-ok { color: #28a745; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-danger { color: #dc3545; font-weight: bold; }
    h1, h2, h3 { color: #0047AB !important; font-family: 'Helvetica Neue', sans-serif; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_singularity():
    st.title("🌐 LZTuned - The Singularity | Enterprise Engine Analytics")
    st.subheader(f"Lead Systems Engineer: Luis Zavoianu")

    file = st.file_uploader("Încarcă LOG-ul Master (CSV High-Res)", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- MOTOR DE CALCUL MATEMATIC AVANSAT ---
        # 1. Calcul Putere Estimată (Pe baza masei de aer - regula de 1.25x)
        df['Est_HP'] = df['Air mass'] / 1.25
        df['Est_Nm'] = (df['Est_HP'] * 7127) / df['Motor RPM'].replace(0, 1)
        
        # 2. Eficiența Volumetrică (VE % - Aproximare)
        # Formula simplificată: (Masa Aer Reala / Masa Aer Teoretica)
        df['VE_Approx'] = (df['Air mass'] * 100) / (df['Motor RPM'] * 0.15) # Constanta adaptata
        
        # 3. Analiză Lambda Transienți (Viteza de reacție)
        df['Lambda_Response'] = df['Lambda #1 integrator '].diff().abs()
        
        # 4. Burn Time & Spark Stability
        df['Spark_Stability'] = 100 - (df['Ignition angle'].rolling(10).std() * 10)
        
        # --- DASHBOARD DE METRICE MASIVE ---
        st.write("### 💎 KPI & Performance Indicators")
        m_row1 = st.columns(5)
        m_row1[0].metric("Peak Power (Est)", f"{round(df['Est_HP'].max(), 1)} HP")
        m_row1[1].metric("Peak Torque (Est)", f"{round(df['Est_Nm'].max(), 1)} Nm")
        m_row1[2].metric("Max VE (%)", f"{round(df['VE_Approx'].replace([np.inf, -np.inf], 0).max(), 1)}%")
        m_row1[3].metric("Spark Stability", f"{round(df['Spark_Stability'].mean(), 1)}%")
        m_row1[4].metric("Air Flow (g/s)", f"{round(df['Air mass'].max() / 3.6, 1)} g/s")

        # --- STRUCTURA DE ANALIZĂ PE MODULE ---
        tabs = st.tabs(["🚀 DINAMICĂ PUTERE", "🧬 ANALIZĂ COMBUSTIBIL", "🌡️ TERMODINAMICĂ", "📉 STABILITATE APRINDERE", "🔍 REZOLUȚII LUIS ZAVOIANU"])

        with tabs[0]:
            st.write("### Curba Puterii și Cuplului (Estimată)")
            fig_pwr = make_subplots(specs=[[{"secondary_y": True}]])
            fig_pwr.add_trace(go.Scatter(x=df['Motor RPM'], y=df['Est_HP'], name="Cai Putere (HP)", line=dict(color='red', width=3)), secondary_y=False)
            fig_pwr.add_trace(go.Scatter(x=df['Motor RPM'], y=df['Est_Nm'], name="Cuplu (Nm)", line=dict(color='blue', width=2, dash='dash')), secondary_y=True)
            fig_pwr.update_layout(title="Power/Torque over RPM Range", template="plotly_white")
            st.plotly_chart(fig_pwr, use_container_width=True)

        with tabs[1]:
            st.write("### Management Amestec și Transienți")
            # Vizualizăm cum reacționează integratoarele la schimbările de clapeta
            fig_lambda = px.scatter(df, x="Throttle pos.", y="Lambda #1 integrator ", color="Motor RPM",
                                     size="Injection time", title="Harta de Corecție Lambda vs Poziție Clapetă")
            st.plotly_chart(fig_lambda, use_container_width=True)
            
            # Tabel de sănătate bancuri
            st.write("**Sănătate Bancuri (Bank 1 vs Bank 2):**")
            l_diff = abs(df['Lambda #1 integrator '].mean() - df['Lambda #2 integrator'].mean())
            st.progress(min(l_diff * 10, 1.0))
            st.write(f"Diferență medie între rânduri: {round(l_diff*100, 2)}%")

        with tabs[2]:
            st.write("### Termodinamică și Eficiență Radiator")
            fig_thermal = go.Figure()
            fig_thermal.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Apa Ieșire Motor", fill='tozeroy'))
            fig_thermal.add_trace(go.Scatter(x=df['time'], y=df['Radiator coolant outlet temp.'], name="Apa Ieșire Radiator"))
            fig_thermal.add_trace(go.Scatter(x=df['time'], y=df['Oil temp.'], name="Ulei Motor", line=dict(color='black', width=4)))
            st.plotly_chart(fig_thermal, use_container_width=True)

        with tabs[3]:
            st.write("### Diagnostic Avansat Aprindere")
            c1, c2 = st.columns(2)
            with c1:
                # Corelația între voltaj și knock (Spark energy analysis)
                fig_spark = px.density_contour(df, x="Battery voltage", y="Knock sensor #1", 
                                              title="Corelație Voltaj Baterie / Vibrație Knock")
                st.plotly_chart(fig_spark, use_container_width=True)
            with c2:
                # Harta de retragere avans
                fig_ign = px.scatter(df, x="time", y="Ignition angle", color="Engine load", size="Air mass",
                                    title="Analiză Avans (Mărimea punctului = Masa Aer)")
                st.plotly_chart(fig_ign, use_container_width=True)

        with tabs[4]:
            st.header("📄 Raport de Rezoluție Luis Zavoianu")
            
            # Generator de Rezoluții bazat pe praguri multiple
            st.write("---")
            
            # Rezoluție 1: Eficiența Volumetrică
            ve_peak = df['VE_Approx'].max()
            if ve_peak > 90:
                st.write(f"✅ **Eficiență Admisie:** Motorul respiră excelent. VE Peak la {round(ve_peak,1)}%.")
            else:
                st.write(f"⚠️ **Eficiență Admisie:** VE scăzut ({round(ve_peak,1)}%). Verificați filtrele sau posibile restricții pe traseu.")

            # Rezoluție 2: Spark Health
            if df['Ignition angle'].std() > 5:
                st.write("❌ **Stabilitate Aprindere:** S-a detectat 'Spark Scatter'. ECU face corecții instabile. Verificați bujiile/bobinele.")
            
            # Rezoluție 3: Thermal Recovery
            recovery_rate = df['Motor temp.'].diff().mean()
            if recovery_rate > 0.5:
                 st.write("⚠️ **Management Termic:** Motorul tinde să se supraîncălzească sub sarcină constantă.")

            # Tabel final cu TOATE datele corelate
            st.write("### 🔍 Master Data View (Toți Parametrii)")
            st.dataframe(df.describe(), use_container_width=True)

        # --- FOOTER ---
        st.markdown("---")
        st.write(f"**LZTuned Intelligence Suite** | Build: 2025.Singularity | Signature: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_singularity()
