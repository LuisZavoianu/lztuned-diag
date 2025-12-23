import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# --- CONFIGURARE INTERFAȚĂ ---
st.set_page_config(page_title="LZTuned Omniscience", layout="wide")

# CSS pentru vizibilitate maximă pe fundal alb și densitate mare de date
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .report-header { background-color: #f1f3f5; padding: 10px; border-radius: 5px; border-left: 10px solid #007bff; margin-bottom: 20px; }
    .data-card { border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; background-color: #ffffff; }
    h1, h2, h3 { color: #002b5e !important; }
    .stMetric { border: 1px solid #eee; padding: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

def lztuned_omniscience():
    st.markdown("<div class='report-header'><h1>LZTuned Omniscience Engine</h1><p>Lead Engineer: <b>Luis Zavoianu</b> | Diagnostic Complet 360°</p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă LOG-ul pentru extracție totală", type="csv")

    if file:
        df = pd.read_csv(file, sep=';')
        
        # --- MOTOR DE CALCUL PENTRU PARAMETRI EXTRAȚI ---
        # Calculăm absolut tot ce se poate deriva
        df['Inj_Duty_Cycle'] = (df['Injection time'] * df['Motor RPM']) / 1200
        df['Air_Per_Rev'] = df['Air mass'] / (df['Motor RPM'] + 1)
        df['Lambda_Error_Bank1'] = (df['Lambda #1 integrator '] - 1).abs()
        df['Lambda_Error_Bank2'] = (df['Lambda #2 integrator'] - 1).abs()
        df['Thermal_Efficiency'] = df['Oil temp.'] / (df['Motor temp.'] + 1)
        df['Spark_Energy_Est'] = df['Battery voltage'] * 0.85 # Factor de eficiență bobină
        df['Fan_Workload'] = df['Electric fan speed'] * df['Motor temp.'] / 100
        
        # --- TABEL DE METRICE MASIVE (2 RÂNDURI) ---
        m_cols = st.columns(8)
        m_cols[0].metric("RPM Max", f"{int(df['Motor RPM'].max())}")
        m_cols[1].metric("Air Mass Peak", f"{df['Air mass'].max()}")
        m_cols[2].metric("Max Inj Time", f"{df['Injection time'].max()}ms")
        m_cols[3].metric("Ign Min", f"{df['Ignition angle'].min()}°")
        m_cols[4].metric("Oil Peak", f"{df['Oil temp.'].max()}°C")
        m_cols[5].metric("Water Peak", f"{df['Motor temp.'].max()}°C")
        m_cols[6].metric("Volt Min", f"{df['Battery voltage'].min()}V")
        m_cols[7].metric("Speed Max", f"{df['Speed'].max()} km/h")

        # --- MODULE DE ANALIZĂ EXHAUSTIVĂ ---
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "📊 DINAMICĂ TOTALĂ", 
            "⛽ INJECȚIE & LAMBDA", 
            "⚡ APRINDERE & KNOCK", 
            "🌡️ TERMICĂ & AUX", 
            "🔬 ANALIZĂ STATISTICĂ",
            "📜 REZOLUȚII LUIS ZAVOIANU"
        ])

        with t1:
            st.subheader("Corelație Universală a Parametrilor")
            # Grafic cu 5 axe sincronizate pentru a vedea TOTUL odată
            fig_master = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                                      subplot_titles=("Performanță", "Admisie", "Injecție", "Aprindere", "Electric"))
            
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='blue')), row=1, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Speed'], name="Speed", line=dict(color='black')), row=1, col=1)
            
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass", line=dict(color='cyan')), row=2, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Throttle pos.'], name="Throttle", line=dict(color='orange')), row=2, col=1)
            
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Injection time'], name="Inj Time", line=dict(color='red')), row=3, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Inj_Duty_Cycle'], name="Duty Cycle %", fill='tozeroy'), row=3, col=1)
            
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Ignition angle'], name="Ignition", line=dict(color='purple')), row=4, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock 1", line=dict(width=1)), row=4, col=1)
            
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Battery voltage'], name="Voltage", line=dict(color='gold')), row=5, col=1)
            fig_master.add_trace(go.Scatter(x=df['time'], y=df['Idle speed controller'], name="Idle Control"), row=5, col=1)

            fig_master.update_layout(height=1200, template="plotly_white")
            st.plotly_chart(fig_master, use_container_width=True)

        with t2:
            st.subheader("Sistemul de Combustibil (Detaliat)")
            c1, c2 = st.columns(2)
            with c1:
                # Vizualizăm încălzirea sondelor Lambda - date pe care le doreai înapoi
                fig_l = go.Figure()
                fig_l.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 pre-cat heating'], name="Heating Bank 1"))
                fig_l.add_trace(go.Scatter(x=df['time'], y=df['Lambda #2 pre-cat heating'], name="Heating Bank 2"))
                st.plotly_chart(fig_l, use_container_width=True)
            with c2:
                # Corelație integratori vs Sarcina
                fig_int = px.scatter(df, x="Engine load", y=["Lambda #1 integrator ", "Lambda #2 integrator"], 
                                    title="Deviație Integratori Lambda în funcție de Sarcina")
                st.plotly_chart(fig_int, use_container_width=True)

        with t3:
            st.subheader("Aprindere și Control Detonații")
            c1, c2 = st.columns(2)
            with c1:
                # Heatmap Spark Retard
                fig_h = px.density_heatmap(df, x="Motor RPM", y="Engine load", z="Ignition angle", histfunc="min",
                                          color_continuous_scale='Magma', title="Harta de Avans Minim (Zone Critice)")
                st.plotly_chart(fig_h, use_container_width=True)
            with c2:
                # Histograme Knock
                fig_k = px.histogram(df, x=["Knock sensor #1", "Knock sensor #2"], barmode="overlay", title="Distribuția Tensiunii Senzorilor de Knock")
                st.plotly_chart(fig_k, use_container_width=True)

        with t4:
            st.subheader("Subsisteme Termice și Radiator")
            # Toate datele despre apă și ventilator
            fig_t = px.line(df, x="time", y=["Motor temp.", "Radiator coolant outlet temp.", "Oil temp.", "Intake temp.", "Electric fan speed"])
            st.plotly_chart(fig_t, use_container_width=True)
            

[Image of an automotive thermostat and coolant circuit diagram]


        with t5:
            st.subheader("Analiză Matematică și Corelații Toate Datele")
            # Matricea de corelație (Pearson) pentru a vedea ce senzor influențează pe care
            corr = df.corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Matricea de Influență a Senzorilor (Correlation Matrix)")
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.write("### Statistici Descriptive Complete")
            st.dataframe(df.describe(percentiles=[.05, .25, .5, .75, .95]), use_container_width=True)

        with t6:
            st.header("📋 Rezoluții Tehnice Massive - Luis Zavoianu")
            
            # Verificăm ABSOLUT tot
            res_cols = st.columns(3)
            with res_cols[0]:
                st.info("🛠️ MECANICĂ & FLUX")
                if df['Air mass'].max() > 0: st.write(f"- Masa Aer Peak: {df['Air mass'].max()} kg/h")
                if df['Throttle pos.'].max() < 95: st.warning("- Clapeta nu se deschide 100%!")
                st.write(f"- Eficiență Radiator Max: {round(df['Motor temp.'].max() - df['Radiator coolant outlet temp.'].min(), 1)}°C")

            with res_cols[1]:
                st.info("🔥 COMBUSTIE")
                if df['Ignition angle'].min() < 2: st.error("- Detonație detectată în sarcină!")
                st.write(f"- Duty Cycle Injectoare Max: {round(df['Inj_Duty_Cycle'].max(), 1)}%")
                st.write(f"- Tensiune Baterie Stabilă: {'Da' if df['Battery voltage'].std() < 0.2 else 'Nu (Variații mari)'}")

            with res_cols[2]:
                st.info("🔌 SENZORI")
                st.write(f"- Pre-cat Heating Actv: {df['Lambda #1 pre-cat heating'].mean() > 0}")
                st.write(f"- Diferență Bank 1/2: {round(abs(df['Lambda #1 integrator '].mean() - df['Lambda #2 integrator'].mean()) * 100, 2)}%")

        # --- FOOTER ---
        st.markdown("---")
        st.write(f"**LZTuned Omniscience Engine** | Lead: **Luis Zavoianu** | Toate datele procesate.")

if __name__ == "__main__":
    lztuned_omniscience()
