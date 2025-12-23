import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE INTERFAȚĂ ---
st.set_page_config(page_title="LZTuned Omniscience", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .report-header { background-color: #f1f3f5; padding: 15px; border-radius: 10px; border-left: 10px solid #007bff; margin-bottom: 20px; }
    h1, h2, h3 { color: #002b5e !important; }
    .stMetric { border: 1px solid #eee; padding: 10px; border-radius: 8px; background: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_omniscience():
    st.markdown("<div class='report-header'><h1>LZTuned Omniscience Engine</h1><p>Lead Engineer: <b>Luis Zavoianu</b> | Sistem de Extracție Totală a Datelor</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă fișierul LOG pentru procesare completă", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- CALCULI AVANSAȚI (DATA MINING) ---
        df['Inj_Duty_Cycle'] = (df['Injection time'] * df['Motor RPM']) / 1200
        df['Air_Per_Rev'] = df['Air mass'] / (df['Motor RPM'].replace(0, 1))
        df['Thermal_Delta_Engine'] = df['Motor temp.'] - df['Radiator coolant outlet temp.']
        df['Lambda_Diff'] = (df['Lambda #1 integrator '] - df['Lambda #2 integrator']).abs()
        df['Spark_Stability'] = df['Ignition angle'].rolling(window=5).std()
        df['Volt_Efficiency'] = (df['Battery voltage'] / 14.4) * 100

        # --- KPI DASHBOARD (8 PARAMETRI) ---
        m_cols = st.columns(8)
        m_cols[0].metric("RPM Peak", int(df['Motor RPM'].max()))
        m_cols[1].metric("Air Mass Peak", df['Air mass'].max())
        m_cols[2].metric("Inj Duty %", f"{round(df['Inj_Duty_Cycle'].max(), 1)}%")
        m_cols[3].metric("Min Ignition", f"{df['Ignition angle'].min()}°")
        m_cols[4].metric("Max Oil T", f"{df['Oil temp.'].max()}°C")
        m_cols[5].metric("Max Water T", f"{df['Motor temp.'].max()}°C")
        m_cols[6].metric("Volt Min", f"{df['Battery voltage'].min()}V")
        m_cols[7].metric("Max Speed", f"{df['Speed'].max()} km/h")

        # --- MODULE ANALIZĂ ---
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "📊 TELEMETRIE MASTER", "⛽ COMBUSTIBIL & LAMBDA", "⚡ APRINDERE & KNOCK", 
            "🌡️ SISTEME TERMICE", "🔬 STATISTICI COMPLETE", "📜 REZOLUȚII LUIS ZAVOIANU"
        ])

        with t1:
            st.subheader("Sincronizare Totală Senzori")
            fig_master = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='blue')), row=1, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass", line=dict(color='cyan')), row=2, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Injection time'], name="Inj Time", line=dict(color='red')), row=3, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition", line=dict(color='purple')), row=4, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Battery voltage'], name="Voltage", line=dict(color='gold')), row=5, col=1)
            fig_master.update_layout(height=900, template="plotly_white")
            st.plotly_chart(fig_master, use_container_width=True)

        with t2:
            st.subheader("Analiză Detaliată Amestec")
            c1, c2 = st.columns(2)
            with c1:
                # Recuperăm datele de încălzire sonde lambda
                fig_heat = px.line(df, x="time", y=["Lambda #1 pre-cat heating", "Lambda #2 pre-cat heating"], title="Activitate Încălzire Sonde")
                st.plotly_chart(fig_heat, use_container_width=True)
            with c2:
                fig_int = px.scatter(df, x="Engine load", y=["Lambda #1 integrator ", "Lambda #2 integrator"], title="Integratori vs Sarcină")
                st.plotly_chart(fig_int, use_container_width=True)

        with t3:
            st.subheader("Control Detonații și Stabilitate Aprindere")
            c1, c2 = st.columns(2)
            with c1:
                fig_knock = px.area(df, x="time", y=["Knock sensor #1", "Knock sensor #2"], title="Activitate Senzori Knock (V)")
                st.plotly_chart(fig_knock, use_container_width=True)
            with c2:
                fig_scat = px.scatter(df, x="Motor RPM", y="Ignition angle", color="Engine load", title="Scatter Plot: Avans vs Turație")
                st.plotly_chart(fig_scat, use_container_width=True)

        with t4:
            st.subheader("Management Termic și Flux Radiator")
            fig_temp = px.line(df, x="time", y=["Motor temp.", "Radiator coolant outlet temp.", "Oil temp.", "Intake temp.", "Electric fan speed"], title="Monitorizare Termodinamică")
            st.plotly_chart(fig_temp, use_container_width=True)

        with t5:
            st.subheader("Matricea de Corelație și Statistici")
            corr = df.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_corr, use_container_width=True)
            st.write("### Tabel Date Brute (Full Description)")
            st.dataframe(df.describe(), use_container_width=True)

        with t6:
            st.header("📋 Rezoluții Tehnice - Luis Zavoianu")
            r1, r2, r3 = st.columns(3)
            with r1:
                st.write("**FLUX & AER**")
                st.write(f"- Peak Air: {df['Air mass'].max()} kg/h")
                st.write(f"- TPS Max: {df['Throttle pos.'].max()}%")
            with r2:
                st.write("**COMBUSTIE**")
                st.write(f"- Min Ign: {df['Ignition angle'].min()}°")
                st.write(f"- Lambda Diff: {round(df['Lambda_Diff'].mean(), 4)}")
            with r3:
                st.write("**SISTEM ELECTRIC**")
                st.write(f"- Volt Stability: {round(df['Battery voltage'].std(), 3)}")
                st.write(f"- Fan Activity: {'Activ' if df['Electric fan speed'].max() > 0 else 'Inactiv'}")

        st.markdown("---")
        st.write(f"**LZTuned Omniscience Engine** | Lead: **Luis Zavoianu**")

if __name__ == "__main__":
    lztuned_omniscience()
