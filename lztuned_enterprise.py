import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== CONFIG =====================
st.set_page_config(page_title="LZTuned Absolute Omniscience", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #111; }
    .main-header { background: #001529; padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px; }
    .report-card { background: white; padding: 15px; border-radius: 8px; border-left: 5px solid #1890ff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .metric-box { text-align: center; padding: 10px; background: #fff; border-radius: 8px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

def app():
    st.markdown("<div class='main-header'><h1>LZTuned Absolute Omniscience v9.0</h1><p>Chief Engineer: <b>Luis Zavoianu</b></p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă Log ECU CSV", type="csv")
    if not file:
        st.info("Încarcă fișierul pentru analiza totală.")
        return

    # Citire date
    df = pd.read_csv(file, sep=';')
    
    # --- MATH CHANNELS & DERIVED DATA ---
    safe_rpm = df['Motor RPM'].replace(0, 1)
    df['Inj_Duty_Cycle'] = (df['Injection time'] * safe_rpm) / 1200
    df['VE_Approx'] = (df['Air mass'] * 100) / (safe_rpm * 0.16 + 1)
    df['Lambda_Diff'] = (df['Lambda #1 integrator '] - df['Lambda #2 integrator']).abs()
    df['Cooling_Delta'] = df['Motor temp.'] - df['Radiator coolant outlet temp.']
    df['Power_Est'] = df['Air mass'] / 1.22
    
    # --- FIX PENTRU EROAREA DE PIVOT (BINNING) ---
    df['RPM_BIN'] = pd.cut(df['Motor RPM'], bins=12).astype(str)
    df['LOAD_BIN'] = pd.cut(df['Engine load'], bins=10).astype(str)

    # --- KPI DASHBOARD ---
    st.subheader("🚀 Key Performance Indicators")
    kpi = st.columns(6)
    kpi[0].metric("Peak RPM", int(df['Motor RPM'].max()))
    kpi[1].metric("Air Flow", f"{df['Air mass'].max()} kg/h")
    kpi[2].metric("Max Duty", f"{round(df['Inj_Duty_Cycle'].max(), 1)}%")
    kpi[3].metric("Min Ign", f"{df['Ignition angle'].min()}°")
    kpi[4].metric("Peak Oil", f"{df['Oil temp.'].max()}°C")
    kpi[5].metric("Est. Power", f"{round(df['Power_Est'].max(), 1)} HP")

    # --- TABS ANALIZA TOTALA ---
    t1, t2, t3, t4, t5 = st.tabs(["📊 HARTA MAPPING", "📈 TELEMETRIE MASTER", "🧪 CORELAȚII & STATS", "🌡️ TERMODINAMICĂ", "🏁 CONCLUZII & REZULTAT"])

    with t1:
        st.subheader("Distribuția Avansului (Ignition Mapping)")
        # Folosim observed=True pentru a evita erorile de categorii goale
        heat = df.groupby(['LOAD_BIN', 'RPM_BIN'], observed=True)['Ignition angle'].mean().unstack()
        fig_map = px.imshow(heat, color_continuous_scale='RdYlGn', title="Ignition Map din Log")
        st.plotly_chart(fig_map, use_container_width=True)
        

    with t2:
        st.subheader("Telemetrie Sincronizată Master")
        fig_master = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03)
        
        # RPM & Air
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM"), row=1, col=1)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass", line=dict(dash='dot')), row=1, col=1)
        
        # Injecție & Lambda
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Injection time'], name="Inj Time"), row=2, col=1)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 integrator '], name="L1"), row=2, col=1)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Lambda #2 integrator'], name="L2"), row=2, col=1)
        
        # Knock & Ign
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition"), row=3, col=1)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock 1"), row=3, col=1)
        
        # Electric & Heating (Datele tale vechi)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Battery voltage'], name="Voltage"), row=4, col=1)
        fig_master.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 pre-cat heating'], name="Heat L1"), row=4, col=1)

        fig_master.update_layout(height=1000, template="plotly_white")
        st.plotly_chart(fig_master, use_container_width=True)

    with t3:
        st.subheader("Matricea de Corelație și Statistici Complete")
        corr = df.select_dtypes(include=[np.number]).corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)
        st.dataframe(df.describe().T, use_container_width=True)

    with t4:
        st.subheader("Analiza Sistemului de Răcire")
        fig_therm = px.line(df, x='time', y=['Motor temp.', 'Radiator coolant outlet temp.', 'Oil temp.', 'Intake temp.'])
        st.plotly_chart(fig_therm, use_container_width=True)
        st.write(f"**Eficiență Radiator (Delta Max):** {round(df['Cooling_Delta'].max(), 1)}°C")
        

    with t5:
        st.header("🏁 Rezultat Final și Plan de Acțiune")
        
        # LOGICĂ DE CONCLUZIE
        st.write("### 🔎 Analiză Date Luis Zavoianu:")
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("#### ✅ Puncte Forte")
            if df['Inj_Duty_Cycle'].max() < 85:
                st.write("- **Sistem Injecție:** Injectoarele fac față (Duty Cycle sub 85%).")
            if df['Battery voltage'].min() > 13.2:
                st.write("- **Sistem Electric:** Alternatorul debitează corect sub sarcină.")
            if df['Lambda_Diff'].mean() < 0.05:
                st.write("- **Echilibru Bancuri:** Motorul funcționează simetric pe ambele rânduri de cilindri.")

        with col_res2:
            st.markdown("#### ⚠️ Probleme Detectate")
            if df['Ignition angle'].min() < 0:
                st.write(f"- **Retard Avans:** S-a detectat avans negativ ({df['Ignition angle'].min()}°). ECU intervine pentru a preveni detonația.")
            if df['Oil temp.'].max() > 110:
                st.write(f"- **Temperatură Ulei:** Valoarea de {df['Oil temp.'].max()}°C este la limita superioară pentru utilizare stradală.")
            if df['Air mass'].max() > 550:
                 st.write("- **Debit Aer:** Flux mare de aer detectat, asigurați-vă că amestecul este suficient de bogat (AFR).")

        st.success(f"**CONCLUZIE FINALĂ:** Mașina dezvoltă aproximativ {round(df['Power_Est'].max(), 1)} CP. Recomandăm verificarea hărții de avans în zonele cu valori negative și monitorizarea temperaturii uleiului în sarcină prelungită.")

if __name__ == "__main__":
    app()
