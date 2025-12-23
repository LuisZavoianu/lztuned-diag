import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== CONFIG =====================
st.set_page_config(page_title="LZTuned Omni-Tuner v12.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #d1d5db; }
    .status-card { background-color: #1a1f29; padding: 20px; border-radius: 12px; border: 1px solid #2d333b; }
    .highlight { color: #00d1ff; font-weight: bold; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

def app():
    st.title("🛡️ LZTuned Omni-Tuner: Deep Data Extraction")
    st.caption("Advanced Engine Calibration & Forensics | Lead Architect: Luis Zavoianu")

    file = st.file_uploader("Încarcă Log Master (.csv)", type="csv")
    if not file: return

    df = pd.read_csv(file, sep=';')
    
    # --- MATH ENGINE: DATA EXTRACTION ---
    safe_rpm = df['Motor RPM'].replace(0, 1)
    df['Inj_Duty_Cycle'] = (df['Injection time'] * safe_rpm) / 1200
    df['VE_Calculated'] = (df['Air mass'] * 100) / (safe_rpm * 0.16 + 1)
    df['Spark_Energy_Index'] = df['Ignition angle'] * df['Engine load'] / 100
    df['Lambda_Diff_Pct'] = (df['Lambda #1 integrator '] - df['Lambda #2 integrator']).abs() * 100
    
    # Segmentare precisă
    df['RPM_Step'] = (df['Motor RPM'] // 250) * 250 

    # --- KPI DASHBOARD (BRUT) ---
    st.subheader("📊 Parametri Bruti de Performanță")
    kpi = st.columns(4)
    with kpi[0]:
        st.metric("Peak Air Flow", f"{df['Air mass'].max():.1f} kg/h")
        st.write(f"Vârf atins la {df.loc[df['Air mass'].idxmax(), 'Motor RPM']} RPM")
    with kpi[1]:
        st.metric("Max Ignition Retard", f"{df['Ignition angle'].min()}°")
        st.write(f"Sarcina la vârf: {df.loc[df['Ignition angle'].idxmin(), 'Engine load']}%")
    with kpi[2]:
        st.metric("Lambda Bank Skew", f"{df['Lambda_Diff_Pct'].max():.2f}%")
        st.write("Diferența max. între rânduri")
    with kpi[3]:
        st.metric("Peak Exhaust Heat Index", f"{int(df['Motor temp.'].max() + df['Ignition angle'].abs().max())}")
        st.write("Stres termic combinat")

    # --- MODULE DE VIZUALIZARE AVANSATĂ ---
    tabs = st.tabs(["🧬 MAPPING 3D", "🔍 ANALIZA SLICE-BY-SLICE", "⚡ STABILITATE & ZGOMOT", "🛠️ RECOMANDĂRI SOFT"])

    with tabs[0]:
        st.subheader("Harta de Eficiență 3D (RPM vs Load vs Flow)")
        # Vizualizare 3D pentru a vedea "gropile" de putere
        fig_3d = px.scatter_3d(df, x='Motor RPM', y='Engine load', z='Air mass',
                                color='Ignition angle', size='Inj_Duty_Cycle',
                                title="Data Cloud: Interdependența Senzorilor",
                                color_continuous_scale='Turbo', opacity=0.7)
        st.plotly_chart(fig_3d, use_container_width=True)
        st.info("💡 Această vizualizare te ajută să vezi dacă avansul scade brusc exact când masa de aer atinge vârful (indică limitare de protecție).")

    with tabs[1]:
        st.subheader("Analiza pe Felii de Turație (Slice Analysis)")
        # Tabel detaliat pentru fiecare 250 RPM
        slice_df = df.groupby('RPM_Step').agg({
            'Air mass': 'max',
            'Ignition angle': 'mean',
            'Lambda #1 integrator ': 'mean',
            'Knock sensor #1': 'max',
            'Inj_Duty_Cycle': 'max'
        }).reset_index()
        
        fig_slice = make_subplots(specs=[[{"secondary_y": True}]])
        fig_slice.add_trace(go.Bar(x=slice_df['RPM_Step'], y=slice_df['Air mass'], name="Air Mass Peak", marker_color='#1f77b4'), secondary_y=False)
        fig_slice.add_trace(go.Scatter(x=slice_df['RPM_Step'], y=slice_df['Ignition angle'], name="Avg Ignition", line=dict(color='#ff7f0e', width=3)), secondary_y=True)
        st.plotly_chart(fig_slice, use_container_width=True)
        st.write("### 📋 Date Tabelare pentru Tuner (Sarcina Maximă)")
        st.dataframe(slice_df.style.highlight_max(axis=0, color='#161b22'), use_container_width=True)

    with tabs[2]:
        st.subheader("Corelație Knock vs Avans vs Temperatură")
        # Identificăm dacă Knock-ul e cauzat de căldură sau de avans prea mare
        fig_scat = px.scatter(df, x="Ignition angle", y="Knock sensor #1", color="Intake temp.",
                             size="Engine load", title="Knock Correlation Matrix")
        st.plotly_chart(fig_scat, use_container_width=True)

    with tabs[3]:
        st.header("🏁 Verdict de Calibrare - Luis Zavoianu")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.write("### ⛽ Fueling Strategy")
            if df['Lambda #1 integrator '].mean() > 0.90 and df['Air mass'].max() > 500:
                st.error("Amestec prea sărac la debit mare de aer!")
                st.write("- **Update necesar:** Crește valorile în Fuel Table cu 7-10% peste 4500 RPM.")
            else:
                st.success("Amestecul este în zona de siguranță.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.write("### ⚡ Ignition Strategy")
            if df['Ignition angle'].min() < 5:
                st.warning("Retard agresiv detectat.")
                st.write("- **Update necesar:** ECU forțează scăderea avansului. Redu harta de avans cu 2 grade pentru a evita corecțiile bruște.")
            else:
                st.success("Avansul este stabil și permite optimizări fine.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("🔍 Observație Brută Finală")
        peak_idx = df['Air mass'].idxmax()
        st.write(f"La **{df.loc[peak_idx, 'Motor RPM']} RPM**, mașina ta consumă **{df.loc[peak_idx, 'Air mass']} kg/h** de aer cu un avans de **{df.loc[peak_idx, 'Ignition angle']}°**. Aceasta este celula de sarcină maximă unde trebuie să te asiguri că Lambda este sub 0.82.")

if __name__ == "__main__":
    app()
