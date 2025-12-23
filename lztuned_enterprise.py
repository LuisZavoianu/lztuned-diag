import streamlit as st
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===================== CONFIG =====================
st.set_page_config("LZTuned Absolute Control", layout="wide")

# ===================== DATA MODELS =====================
@dataclass
class EngineDerivedData:
    inj_duty: pd.Series
    ve: pd.Series
    lambda_dev: pd.Series
    ignition_stability: pd.Series
    thermal_stress: pd.Series
    volt_sag: pd.Series


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
        self.derived = self._compute_derived()

    def _compute_derived(self) -> EngineDerivedData:
        return EngineDerivedData(
            inj_duty=(self.df['Injection time'] * self.df['Motor RPM']) / 1200,
            ve=(self.df['Air mass'] * 100) / (self.df['Motor RPM'] * 0.16 + 1),
            lambda_dev=(self.df['Lambda #1 integrator '] - self.df['Lambda #2 integrator']).abs(),
            ignition_stability=self.df['Ignition angle'].rolling(10).std(),
            thermal_stress=self.df['Motor temp.'] + self.df['Oil temp.'] * 0.5,
            volt_sag=self.df['Battery voltage'].max() - self.df['Battery voltage']
        )

    def map_bins(self, rpm_bins=16, load_bins=12):
        self.df['RPM_BIN'] = pd.cut(self.df['Motor RPM'], rpm_bins)
        self.df['LOAD_BIN'] = pd.cut(self.df['Engine load'], load_bins)


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
        return self.issues

    def _check_ve(self):
        low_ve = self.d.ve.mean()
        if low_ve < 85:
            self.issues.append(TuningIssue(
                "🔴 CRITICAL",
                "Eficiență Volumetrică Suboptimă",
                f"VE mediu = {low_ve:.1f}%",
                "Revizuiește harta de sarcină și traseul de admisie"
            ))

    def _check_lambda_balance(self):
        dev = self.d.lambda_dev.mean()
        if dev > 0.04:
            self.issues.append(TuningIssue(
                "🔴 CRITICAL",
                "Dezechilibru Lambda între bancuri",
                f"Deviație medie = {dev:.3f}",
                "Verifică injectoare, etanșeitate evacuare, corecții banc separate"
            ))

    def _check_knock_behavior(self):
        unstable = self.d.ignition_stability.max()
        if unstable > 3.5:
            self.issues.append(TuningIssue(
                "🟡 WARNING",
                "Instabilitate avans (spark scatter)",
                f"STD max = {unstable:.2f}",
                "Netedizează harta de avans în zona high load / mid RPM"
            ))

    def _check_voltage(self):
        sag = self.d.volt_sag.max()
        if sag > 1.4:
            self.issues.append(TuningIssue(
                "🟡 WARNING",
                "Căderi de tensiune sub sarcină",
                f"Drop maxim = {sag:.2f}V",
                "Verifică grounding, alternator, regulator"
            ))


# ===================== STREAMLIT UI =====================
def app():
    st.title("🔥 LZTuned Absolute Control v7.0")
    st.caption("Log-based tuning intelligence | CTO: Luis Zavoianu")

    file = st.file_uploader("Încarcă LOG ECU (.csv)", type="csv")

    if not file:
        return

    df = pd.read_csv(file, sep=';')
    model = EngineLogModel(df)
    model.map_bins()

    analyzer = TuningAnalyzer(model)
    issues = analyzer.analyze()

    # ===================== METRICS =====================
    cols = st.columns(6)
    cols[0].metric("RPM Max", int(df['Motor RPM'].max()))
    cols[1].metric("Air Mass Peak", f"{df['Air mass'].max():.1f}")
    cols[2].metric("Inj Duty Max", f"{model.derived.inj_duty.max():.1f}%")
    cols[3].metric("Min Ign", f"{df['Ignition angle'].min():.1f}°")
    cols[4].metric("Oil Temp Max", f"{df['Oil temp.'].max():.1f}°C")
    cols[5].metric("Lambda Δ", f"{model.derived.lambda_dev.mean():.3f}")

    # ===================== MAP ANALYSIS =====================
    st.subheader("📊 Harta de Tuning (RPM × Load)")
    heat = df.pivot_table(
        values='Ignition angle',
        index='LOAD_BIN',
        columns='RPM_BIN',
        aggfunc='mean'
    )

    fig_map = px.imshow(
        heat,
        aspect='auto',
        color_continuous_scale='Turbo',
        title="Ignition Timing Map (Derived from Log)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ===================== REPORT =====================
    st.subheader("🏁 Raport Final de Tuning")
    if not issues:
        st.success("Log curat. Motorul este stabil în parametrii analizați.")
    else:
        for i in issues:
            st.markdown(f"""
            **{i.severity} – {i.title}**  
            • Observație: {i.explanation}  
            • Acțiune: {i.recommendation}
            """)

    st.markdown("---")
    st.caption("LZTuned | Absolute Control | Motorsport-grade log intelligence")


if __name__ == "__main__":
    app()
