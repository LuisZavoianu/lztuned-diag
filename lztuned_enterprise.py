import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE UI PREMIUM ---
st.set_page_config(page_title="LZTuned Ultra-Data", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #111111; }
    h1, h2, h3 { color: #0056b3 !important; border-bottom: 1px solid #eee; }
    .report-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0056b3; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_master_engine():
    st.title("🚀 LZTuned Ultra-Data Diagnostic")
    st.write("### Advanced Engineering Suite | Lead: Luis Zavoianu")

    file = st.file_uploader("Încarcă Log CSV pentru Analiză Profundă", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- ENGINE INTELLIGENCE: CALCUL PARAMETRI NOI ---
        # 1. Calcul Duty Cycle Injectoare (Estimare)
        df['Inj_Duty_Cycle'] = (df['Injection time'] * df['Motor RPM']) / 1200
        # 2. Delta Temp (Eficiență Răcire)
        df['Cooling_Delta'] = df['Motor temp.'] - df['Radiator coolant outlet temp.']
        # 3. Analiză Spark Stability
        df['Spark_Dev'] = df['Ignition angle'].rolling(window=5).std()
        
        # --- DASHBOARD METRICS ---
        cols = st.columns(4)
        cols[0].metric("Peak Inj. Duty Cycle", f"{round(df['Inj_Duty_Cycle'].max(), 1)}%")
        cols[1].metric("Max Spark Retard", f"{df['Ignition angle'].min()}°")
        cols[2].metric("Max Cooling Delta", f"{round(df['Cooling_Delta'].max(), 1)}°C")
        cols[3].metric("Air Mass Flow Peak", f"{df['Air mass'].max()} kg/h")

        # --- TABS PENTRU ANALIZĂ ADÂNCĂ ---
        t1, t2, t3, t4, t5 = st.tabs([
            "🎯 HARTA DE PERFORMANȚĂ", 
            "📈 TELEMETRIE SUPRAPUSĂ", 
            "🧬 CORELAȚII SENZORI", 
            "🌡️ ANALIZĂ TERMICĂ",
            "📋 REZOLUȚII TEHNICE"
        ])

        with t1:
            st.subheader("Harta de Avans (Ignition Timing Map)")
            st.info("Această hartă arată unde motorul tău funcționează cel mai eficient și unde ECU retrage avansul.")
            
            # Creare Heatmap: RPM vs Load vs Ignition
            fig_heat = px.density_heatmap(df, x="Motor RPM", y="Engine load", z="Ignition angle", 
                                          histfunc="avg", nbinsx=20, nbinsy=20,
                                          color_continuous_scale='RdYlGn',
                                          labels={'Ignition angle': 'Avans Mediu'})
            st.plotly_chart(fig_heat, use_container_width=True)
            

        with t2:
            st.subheader("Analiză Multi-Senzor")
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02)
            
            # Putere & Flux
            fig.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Masa Aer", line=dict(color='cyan')), row=1, col=1)
            
            # Amestec & Corecții
            fig.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 integrator '], name="Bank 1", line=dict(color='green')), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Lambda #2 integrator'], name="Bank 2", line=dict(color='lime')), row=2, col=1)
            
            # Detonații (Knock)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock 1", line=dict(color='orange')), row=3, col=1)
            fig.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #2'], name="Knock 2", line=dict(color='red')), row=3, col=1)
            
            # Duty Cycle Injectoare
            fig.add_trace(go.Scatter(x=df['time'], y=df['Inj_Duty_Cycle'], name="Inj. Duty Cycle", fill='tozeroy', line=dict(color='purple')), row=4, col=1)

            fig.update_layout(height=1000, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        with t3:
            st.subheader("Analiză Spark Scatter (Corelație Avans/RPM)")
            # Grafic care arată stabilitatea scânteii
            fig_scatter = px.scatter(df, x="Motor RPM", y="Ignition angle", color="Engine load",
                                    size="Knock sensor #1", hover_data=['time'],
                                    title="Stabilitatea Aprinderii în Funcție de Sarcina Motorului")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with t4:
            st.subheader("Eficiența Sistemului de Răcire")
            c1, c2 = st.columns(2)
            with c1:
                # Corelație Temp Apă vs Viteza Fan
                fig_fan = px.line(df, x="time", y=["Motor temp.", "Radiator coolant outlet temp.", "Electric fan speed"],
                                 title="Interacțiune Ventilator / Radiator")
                st.plotly_chart(fig_fan, use_container_width=True)
                
            with c2:
                st.write("**Statistici Termice:**")
                st.write(f"- Temp Max Ulei: {df['Oil temp.'].max()}°C")
                st.write(f"- Eficiență Radiator (Delta): {round(df['Cooling_Delta'].mean(), 2)}°C")
                st.write(f"- Max Intake Temp: {df['Intake temp.'].max()}°C")

        with t5:
            st.header("📋 Rezoluție Tehnică Deep-Dive")
            
            # Logica de detecție automată a problemelor
            with st.expander("🔎 ANALIZĂ SISTEM COMBUSTIBIL", expanded=True):
                if df['Inj_Duty_Cycle'].max() > 85:
                    st.error(f"ALERTĂ: Injectoarele au atins {round(df['Inj_Duty_Cycle'].max(),1)}% duty cycle. Risc de amestec sărac la turații mari!")
                else:
                    st.success("Sistemul de injecție are rezervă de debit suficientă.")

            with st.expander("🔎 ANALIZĂ APRINDERE & KNOCK"):
                knock_count = len(df[df['Knock sensor #1'] > 1.5])
                if knock_count > 0:
                    st.warning(f"S-au detectat {knock_count} evenimente de zgomot (knock) peste 1.5V. Verifică avansul în zonele roșii din hartă.")
                
            with st.expander("🔎 ANALIZĂ SENSORS & VOLTAGE"):
                if df['Battery voltage'].std() > 0.5:
                    st.warning("Instabilitate voltaj detectată. Posibil contact imperfect sau alternator uzat.")

        # --- FOOTER ---
        st.markdown("---")
        st.markdown(f"**LZTuned Enterprise Software** | Analiză generată pentru: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_master_engine()
