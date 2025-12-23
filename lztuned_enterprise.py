import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE INTERFAȚĂ INDUSTRIALĂ ---
st.set_page_config(page_title="LZTuned Hyper-Analysis", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D1D1D1; }
    .report-header { background-color: #111; padding: 25px; border-radius: 15px; border-left: 5px solid #00FF41; margin-bottom: 30px; }
    .status-card { background-color: #1A1A1A; border: 1px solid #333; padding: 20px; border-radius: 12px; height: 100%; }
    .metric-value { font-size: 24px; color: #00FF41; font-weight: bold; }
    h1, h2, h3 { color: #00FF41 !important; font-family: 'Courier New', monospace; }
    .stTab { background-color: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_hyper_analysis():
    st.markdown("<div class='report-header'><h1>LZTuned Hyper-Analysis v5.0</h1><p>Lead Systems Architect: <b>Luis Zavoianu</b> | AI-Driven Engine Diagnostics</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă Log Master (High-Resolution Data)", type="csv")

    if file:
        # Detectare separator și citire
        df = pd.read_csv(file, sep=';')
        
        # --- MOTOR DE CALCUL: ANALIZĂ DERIVATĂ (MATH CHANNELS) ---
        # 1. Eficiența Arderii (Spark Efficiency Index)
        df['Spark_Eff'] = (df['Ignition angle'] * df['Engine load']) / (df['Air mass'] + 1)
        
        # 2. Analiza de Sănătate Alternator/Baterie (Ripple Analysis)
        df['Volt_Stability'] = df['Battery voltage'].rolling(window=10).std()
        
        # 3. Virtual Dyno Pro
        df['Rad_HP'] = (df['Air mass'] / 1.15) * (df['Throttle pos.']/100)
        df['Rad_Nm'] = (df['Rad_HP'] * 7127) / df['Motor RPM'].replace(0, 1)
        
        # 4. Thermal Inertia (Cât de repede crește temp față de sarcină)
        df['Thermal_Inertia'] = df['Motor temp.'].diff() / df['Engine load'].replace(0, 0.1)

        # 5. Lambda Error Cross-Bank
        df['Lambda_Cross_Error'] = (df['Lambda #1 integrator '] - df['Lambda #2 integrator']).abs()

        # --- TABLOU DE CONTROL: HEALTH SCORE ---
        st.write("### 🛠️ Engine Component Health Score")
        h1, h2, h3, h4 = st.columns(4)
        
        # Calcul scoruri de sănătate (0-100)
        fuel_health = max(0, 100 - (df['Lambda_Cross_Error'].mean() * 500))
        spark_health = max(0, 100 - (df['Knock sensor #1'].max() * 20))
        cooling_health = 100 if df['Motor temp.'].max() < 105 else 70
        electric_health = max(0, 100 - (df['Battery voltage'].std() * 1000))

        h1.metric("Fuel System Health", f"{round(fuel_health,1)}%", delta=f"{round(df['Lambda_Cross_Error'].mean(),3)} dev")
        h2.metric("Ignition Health", f"{round(spark_health,1)}%", delta=f"{round(df['Knock sensor #1'].mean(),2)}v knock")
        h3.metric("Cooling Efficiency", f"{round(cooling_health,1)}%", delta=f"{df['Motor temp.'].max()}°C Peak")
        h4.metric("Electrical Health", f"{round(electric_health,1)}%", delta=f"{round(df['Battery voltage'].std(),3)} std")

        # --- MODULE DE ANALIZĂ COMBINATĂ ---
        tabs = st.tabs(["📊 POWER DYNAMICS", "🧪 COMBUSTION ANALYSIS", "🌡️ THERMAL MAPPING", "⚡ ELECTRICAL STABILITY", "🏁 FINAL DIAGNOSTIC"])

        with tabs[0]:
            st.subheader("Analiza Coerenței Puterii (HP vs Air Flow)")
            fig_pwr = make_subplots(rows=2, cols=1, shared_xaxes=True)
            fig_pwr.add_trace(go.Scatter(x=df['time'], y=df['Rad_HP'], name="Estimated HP", line=dict(color='#00FF41', width=3)), row=1, col=1)
            fig_pwr.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass Flow", line=dict(color='#00D1FF', dash='dash')), row=2, col=1)
            st.plotly_chart(fig_pwr, use_container_width=True)

        with tabs[1]:
            st.subheader("Combustion Stress Matrix")
            # Corelație avansată între Knock, Avans și Sarcina
            fig_comb = px.scatter(df, x="Motor RPM", y="Ignition angle", size="Knock sensor #1", color="Engine load",
                                 color_continuous_scale='Turbo', title="Harta Stress Aprindere")
            st.plotly_chart(fig_comb, use_container_width=True)

        with tabs[2]:
            st.subheader("Thermal Delta Analysis")
            fig_therm = go.Figure()
            fig_therm.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Engine Temp"))
            fig_therm.add_trace(go.Scatter(x=df['time'], y=df['Radiator coolant outlet temp.'], name="Radiator Outlet"))
            fig_therm.add_trace(go.Scatter(x=df['time'], y=df['Oil temp.'], name="Oil Temp"))
            fig_therm.update_layout(title="Thermal Gradients", template="plotly_dark")
            st.plotly_chart(fig_therm, use_container_width=True)

        with tabs[3]:
            st.subheader("Electrical & Sensor Noise Analysis")
            fig_volt = px.line(df, x="time", y="Battery voltage", title="Stabilitate Tensiune (Alternator Ripple)")
            st.plotly_chart(fig_volt, use_container_width=True)

        with tabs[4]:
            st.header("🏁 Raport Final de Diagnoză și Plan de Acțiune")
            
            # --- LOGICĂ DE ANALIZĂ FINALĂ (EXPERT SYSTEM) ---
            concluzii = []
            actiuni = []

            # 1. Analiza Combustibil
            if fuel_health < 85:
                concluzii.append("🔴 **Dezechilibru Amestec:** Diferență semnificativă între Bank 1 și Bank 2.")
                actiuni.append("- Verificați injectoarele pe bancul cu corecție pozitivă.")
                actiuni.append("- Inspectați prezența unor pierderi de vacuum (vacuum leaks) pe admisie.")
            
            # 2. Analiza Aprindere
            if spark_health < 80:
                concluzii.append("🔴 **Instabilitate Aprindere:** Detecție zgomot (Knock) peste pragul de siguranță.")
                actiuni.append("- Reduceți avansul cu 2-3 grade în zona de Load/RPM afectată.")
                actiuni.append("- Verificați calitatea carburantului (cifră octanică scăzută).")
            
            # 3. Analiza Mecanică/Flux
            if df['Throttle pos.'].max() < 98:
                concluzii.append("🟡 **Restricție Clapeta:** Clapeta de accelerație nu atinge deschiderea maximă.")
                actiuni.append("- Recalibrați senzorul de poziție clapetă (TPS) sau verificați cursa pedalei.")

            # 4. Analiza Termică
            if df['Motor temp.'].max() > 102:
                concluzii.append("🟡 **Stres Termic Ridicat:** Temperatura lichidului de răcire depășește pragul nominal.")
                actiuni.append("- Verificați starea radiatorului și amestecul antigel/apă.")

            # AFIȘARE RAPORT
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📋 Concluzii Tehnice")
                for c in concluzii:
                    st.write(c)
                if not concluzii:
                    st.success("Toate sistemele funcționează în parametri nominali de performanță.")

            with c2:
                st.subheader("🛠️ Ce trebuie făcut la mașină?")
                for a in actiuni:
                    st.write(a)
                if not actiuni:
                    st.write("Nu sunt necesare intervenții mecanice imediate. Continuați monitorizarea.")

        # --- MASTER DATA VIEW ---
        st.write("### 📉 Omniscience Data View")
        st.dataframe(df.describe().T, use_container_width=True)

        st.markdown("---")
        st.write(f"**LZTuned Hyper-Analysis** | Signature: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_hyper_analysis()
