import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE BRANDING ---
st.set_page_config(page_title="LZTuned Absolute Control", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; color: #1e1e1e; }
    .main-header { background: linear-gradient(90deg, #001529 0%, #003a8c 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #1890ff; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_absolute_control():
    st.markdown("<div class='main-header'><h1>LZTuned Absolute Control v6.0</h1><p>Chief Technical Officer: <b>Luis Zavoianu</b> | Total Engine Data Sovereignty</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încărcare LOG Master (CSV)", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- MOTORUL DE LOGICĂ: CALCUL EXHAUSTIV ---
        # Calculăm toți parametrii virtuali posibili
        df['Inj_Duty_Cycle'] = (df['Injection time'] * df['Motor RPM']) / 1200
        df['VE_Calculated'] = (df['Air mass'] * 100) / (df['Motor RPM'] * 0.16 + 1)
        df['Lambda_Deviation'] = (df['Lambda #1 integrator '] - df['Lambda #2 integrator']).abs()
        df['Ignition_Stability'] = df['Ignition angle'].rolling(10).std()
        df['Thermal_Stress'] = df['Motor temp.'] + (df['Oil temp.'] * 0.5)
        df['Volt_Sag'] = df['Battery voltage'].max() - df['Battery voltage']
        
        # --- 1. DASHBOARD DE ANALIZĂ INSTANTANEE ---
        st.write("### 💎 Indicatori de Performanță Critică")
        m_row = st.columns(6)
        m_row[0].metric("RPM Max", int(df['Motor RPM'].max()))
        m_row[1].metric("Peak Air Mass", f"{df['Air mass'].max()} kg/h")
        m_row[2].metric("Max Inj Duty", f"{round(df['Inj_Duty_Cycle'].max(), 1)}%")
        m_row[3].metric("Min Ignition", f"{df['Ignition angle'].min()}°")
        m_row[4].metric("Max Oil Temp", f"{df['Oil temp.'].max()}°C")
        m_row[5].metric("Lambda Variance", f"{round(df['Lambda_Deviation'].max(), 3)}")

        # --- 2. CORELAȚIA TUTUROR DATELOR (OBLIGATORIU) ---
        t1, t2, t3, t4 = st.tabs(["🌐 SINCRONIZARE TOTALĂ", "📉 ANALIZĂ DE COERENȚĂ", "🔬 MATRICEA SENZORILOR", "🏁 CONCLUZII FINALE"])

        with t1:
            st.subheader("Suprapunerea tuturor parametrilor cheie")
            # Creăm un grafic gigant cu toate datele pentru a vedea cum interacționează
            fig_all = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                                   subplot_titles=("Dinamica Puterii", "Sistem Combustibil", "Management Termic", "Control Detonații"))
            
            # Subplot 1: Putere
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='blue', width=3)), row=1, col=1)
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass", line=dict(color='cyan')), row=1, col=1)
            
            # Subplot 2: Injecție
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Injection time'], name="Inj Time", line=dict(color='red')), row=2, col=1)
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 integrator '], name="Bank 1", line=dict(dash='dot')), row=2, col=1)
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Lambda #2 integrator'], name="Bank 2", line=dict(dash='dot')), row=2, col=1)

            # Subplot 3: Termic
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Motor temp.'], name="Apa"), row=3, col=1)
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Oil temp.'], name="Ulei", line=dict(color='orange')), row=3, col=1)
            
            # Subplot 4: Ignitie
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Avans", line=dict(color='purple')), row=4, col=1)
            fig_all.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock 1"), row=4, col=1)

            fig_all.update_layout(height=1000, template="simple_white")
            st.plotly_chart(fig_all, use_container_width=True)

        with t2:
            st.subheader("Analiza de Coerență (Scatter Matrix Custom)")
            # Corelație între sarcină, turație și avans pentru a vedea eficiența hărții
            fig_scat = px.scatter(df, x="Motor RPM", y="Ignition angle", color="Engine load", size="Air mass",
                                 hover_data=df.columns, title="Harta de Eficiență 4D (RPM, Ign, Load, Flow)")
            st.plotly_chart(fig_scat, use_container_width=True)

        with t3:
            st.subheader("Matricea de Corelație (Interdependența Senzorilor)")
            # Aceasta arată cum un senzor îl "trage" pe altul după el
            corr = df.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='Picnic')
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.write("### Statistici Complete (Extrase din toate coloanele)")
            st.dataframe(df.describe().T, use_container_width=True)

        with t4:
            st.header("🏁 Raport Final și Plan de Lucru - Luis Zavoianu")
            
            # --- LOGICĂ DE DECIZIE AUTOMATĂ ---
            errors = []
            checks = []
            
            # 1. Test Eficiență Volumetrică
            if df['VE_Calculated'].max() < 80:
                errors.append("🔴 **Eficiență Volumetrică Scăzută:** Motorul nu trage suficient aer pentru turația curentă.")
                checks.append("- Verificați filtrul de aer și integritatea traseului de admisie.")
            
            # 2. Test Coerență Bancuri
            if df['Lambda_Deviation'].mean() > 0.05:
                errors.append("🔴 **Dezechilibru Lambda Critic:** Diferența între rânduri indică o problemă de hardware.")
                checks.append("- Verificați injectoarele pe bancul cu valoarea mai mare.")
                checks.append("- Verificați etanșeitatea galeriei de evacuare înainte de sonde.")
                
            # 3. Test Knock & Ign Stability
            if df['Ignition_Stability'].max() > 4:
                errors.append("🟡 **Instabilitate Avans (Spark Scatter):** ECU corecteză agresiv aprinderea.")
                checks.append("- Verificați bujiile și distanța dintre electrozi.")
            
            # 4. Test Tensiune
            if df['Volt_Sag'].max() > 1.5:
                errors.append("🟡 **Cădere de Tensiune:** S-au detectat fluctuații mari sub sarcină.")
                checks.append("- Verificați masa (grounding) motorului și starea alternatorului.")

            # AFIȘARE REZULTATE
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📋 Ce am găsit în LOG:")
                for e in errors: st.write(e)
                if not errors: st.success("Analiza nu a detectat anomalii majore.")
                
            with c2:
                st.subheader("🛠️ Ce trebuie să faci la mașină:")
                for c in checks: st.write(c)

        st.markdown("---")
        st.write(f"**LZTuned Absolute Control** | Build: 2025.Final | Lead: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_absolute_control()
