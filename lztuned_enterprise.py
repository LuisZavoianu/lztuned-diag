import streamlit as st
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== CONFIG =====================
st.set_page_config(page_title="LZTuned Absolute Control v8.0", layout="wide")

# CSS pentru un aspect profesional (Dark Theme Optimized)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .report-card { background-color: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #58a6ff; margin-bottom: 10px; }
    .metric-container { background-color: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
    h1, h2, h3 { color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)

# ===================== DATA MODELS =====================
@dataclass
class EngineDerivedData:
    inj_duty: pd.Series
    ve: pd.Series
    lambda_dev: pd.Series
    ignition_stability: pd.Series
    thermal_stress: pd.Series
    volt_sag: pd.Series
    air_fuel_ratio: pd.Series # Calculat estimativ

@dataclass
class TuningIssue:
    severity: str
    title: str
    explanation: str
    recommendation: str

# ===================== ENGINE LOG CORE =====================
class EngineLogModel:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Curățăm datele de eventuale valori nule sau infinite
        self.df = self.df.replace([np.inf, -np.inf], np.nan).fillna(0)
        self.derived = self._compute_derived()

    def _compute_derived(self) -> EngineDerivedData:
        # Prevenim divizia la zero pentru RPM
        safe_rpm = self.df['Motor RPM'].replace(0, 1)
        
        return EngineDerivedData(
            inj_duty=(self.df['Injection time'] * safe_rpm) / 1200,
            ve=(self.df['Air mass'] * 100) / (safe_rpm * 0.16 + 1),
            lambda_dev=(self.df['Lambda #1 integrator '] - self.df['Lambda #2 integrator']).abs(),
            ignition_stability=self.df['Ignition angle'].rolling(10, center=True).std(),
            thermal_stress=self.df['Motor temp.'] + (self.df['Oil temp.'] * 0.5),
            volt_sag=self.df['Battery voltage'].max() - self.df['Battery voltage'],
            air_fuel_ratio=14.7 * (self.df['Lambda #1 integrator '] + self.df['Lambda #2 integrator']) / 2
        )

    def map_bins(self, rpm_bins=12, load_bins=10):
        # Folosim qcut pentru o distribuție egală a datelor sau cut pentru axe liniare
        self.df['RPM_BIN'] = pd.cut(self.df['Motor RPM'], bins=rpm_bins)
        self.df['LOAD_BIN'] = pd.cut(self.df['Engine load'], bins=load_bins)

# ===================== TUNING ANALYZER =====================
class TuningAnalyzer:
    def __init__(self, model: EngineLogModel):
        self.df = model.df
        self.d = model.derived
        self.issues: List[TuningIssue] = []

    def analyze(self):
        self._check_ve()
        self._check_lambda_balance()
        self._check_knock_behavior()
        self._check_voltage()
        self._check_thermal_efficiency()
        return self.issues

    def _check_ve(self):
        avg_ve = self.d.ve.mean()
        if avg_ve < 75:
            self.issues.append(TuningIssue(
                "🔴 CRITICAL", "Eficiență Volumetrică Scăzută",
                f"VE mediu detectat este de {avg_ve:.1f}%. Motorul nu 'respiră' la capacitate.",
                "Verifică integritatea filtrului de aer, a traseului de admisie sau posibile restricții în evacuare."
            ))

    def _check_lambda_balance(self):
        max_dev = self.d.lambda_dev.max()
        if max_dev > 0.08:
            self.issues.append(TuningIssue(
                "🔴 CRITICAL", "Dezechilibru Masiv Lambda (Cross-Bank)",
                f"Deviație maximă de {max_dev:.3f} între bancuri.",
                "Sugerăm verificarea injectoarelor pe bancul cu valoarea mai mare și inspecția senzorilor O2."
            ))

    def _check_knock_behavior(self):
        if self.df['Knock sensor #1'].max() > 2.5 or self.df['Knock sensor #2'].max() > 2.5:
            self.issues.append(TuningIssue(
                "🟡 WARNING", "Activitate Knock Detectată",
                "Senzorii de zgomot au raportat valori peste pragul de siguranță (2.5V).",
                "Reduceți avansul (Ignition Timing) cu 1.5 - 3 grade în celulele de sarcină maximă."
            ))

    def _check_voltage(self):
        if self.df['Battery voltage'].min() < 13.0:
            self.issues.append(TuningIssue(
                "🟡 WARNING", "Instabilitate Tensiune Electrică",
                f"Tensiunea a scăzut la {self.df['Battery voltage'].min():.2f}V sub sarcină.",
                "Verifică alternatorul și punctele de masă (grounding). Tensiunea mică afectează forța scânteii."
            ))

    def _check_thermal_efficiency(self):
        if self.df['Motor temp.'].max() > 105:
            self.issues.append(TuningIssue(
                "🟠 ADVISORY", "Management Termic la Limită",
                f"Temperatura apei a atins {self.df['Motor temp.'].max()}°C.",
                "Verifică mixul de antigel sau viteza ventilatorului (Electric Fan Speed)."
            ))

# ===================== STREAMLIT UI =====================
def app():
    st.markdown("<div class='report-header'><h1>LZTuned Absolute Control v8.0</h1><p>Master Diagnostic Suite | Lead: <b>Luis Zavoianu</b></p></div>", unsafe_allow_html=True)

    file = st.file_uploader("Încarcă fișierul LOG exportat (Format CSV)", type="csv")

    if not file:
        st.info("Aștept încărcarea datelor pentru inițializarea diagnozei...")
        return

    # Citire și inițializare model
    try:
        df = pd.read_csv(file, sep=';')
        model = EngineLogModel(df)
        model.map_bins()
        analyzer = TuningAnalyzer(model)
        issues = analyzer.analyze()
    except Exception as e:
        st.error(f"Eroare la procesarea fișierului: {e}. Asigură-te că separatorul este ';' și coloanele sunt corecte.")
        return

    # ===================== KPI METRICS =====================
    st.subheader("🚀 Key Performance Indicators")
    m_row1 = st.columns(6)
    m_row1[0].metric("Peak RPM", int(df['Motor RPM'].max()))
    m_row1[1].metric("Air Flow Peak", f"{df['Air mass'].max():.1f} kg/h")
    m_row1[2].metric("Max Inj Duty", f"{model.derived.inj_duty.max():.1f}%")
    m_row1[3].metric("Min Ignition", f"{df['Ignition angle'].min():.1f}°")
    m_row1[4].metric("Peak Oil Temp", f"{df['Oil temp.'].max():.1f}°C")
    m_row1[5].metric("Avg AFR", f"{model.derived.air_fuel_ratio.mean():.2f}")

    # ===================== VIZUALIZARE AVANSATĂ =====================
    st.markdown("---")
    t1, t2, t3 = st.tabs(["📊 ANALIZĂ HĂRȚI", "📈 TELEMETRIE TIMP", "🧬 MATRICEA DE CORELAȚIE"])

    with t1:
        st.subheader("Harta de Avans Real (Ignition Mapping)")
        heat = df.pivot_table(values='Ignition angle', index='LOAD_BIN', columns='RPM_BIN', aggfunc='mean')
        fig_map = px.imshow(heat, aspect='auto', color_continuous_scale='RdYlGn', origin='lower',
                            title="Ignition Advance Map (Real Logged Data)")
        st.plotly_chart(fig_map, use_container_width=True)
        

    with t2:
        st.subheader("Sincronizare Multi-Senzor")
        fig_time = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05)
        fig_time.add_trace(go.Scatter(x=df['time'], y=df['Motor RPM'], name="RPM", line=dict(color='blue')), row=1, col=1)
        fig_time.add_trace(go.Scatter(x=df['time'], y=df['Air mass'], name="Air Mass", line=dict(color='cyan')), row=1, col=1)
        fig_time.add_trace(go.Scatter(x=df['time'], y=df['Lambda #1 integrator '], name="Lambda 1", line=dict(color='green')), row=2, col=1)
        fig_time.add_trace(go.Scatter(x=df['time'], y=df['Lambda #2 integrator'], name="Lambda 2", line=dict(color='lime')), row=2, col=1)
        fig_time.add_trace(go.Scatter(x=df['time'], y=df['Knock sensor #1'], name="Knock B1", line=dict(color='red')), row=3, col=1)
        fig_time.update_layout(height=800, template="plotly_dark")
        st.plotly_chart(fig_time, use_container_width=True)

    with t3:
        st.subheader("Interdependența Senzorilor (Data Mining)")
        corr = df.corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='Picnic', title="Sensor Correlation Matrix")
        st.plotly_chart(fig_corr, use_container_width=True)

    # ===================== RAPORT FINAL =====================
    st.markdown("---")
    st.subheader("🏁 Raport Final de Diagnoză (AI Expert System)")
    
    if not issues:
        st.success("Analiza completă a fost finalizată. Nu s-au detectat anomalii mecanice sau de calibrare.")
    else:
        for i in issues:
            with st.container():
                st.markdown(f"""
                <div class="report-card">
                    <h4>{i.severity} – {i.title}</h4>
                    <p><b>Diagnostic:</b> {i.explanation}</p>
                    <p><b>Acțiune Recomandată:</b> {i.recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

    # Export Date Statistice
    with st.expander("Vezi statistici descriptive brute (Full Table)"):
        st.dataframe(df.describe().T, use_container_width=True)

    st.markdown("---")
    st.caption("LZTuned | Absolute Control | Software conceput pentru performanță extremă.")

if __name__ == "__main__":
    app()
