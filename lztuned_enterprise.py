import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats, signal
from fpdf import FPDF
import base64
import io

# ======================================================
# CONFIG & ARCHITECT THEME (ULTIMATE UX)
# ======================================================
st.set_page_config(
    page_title="LZTuned Architect Ultimate v22.0 | Enterprise",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap');
.main { background: #ffffff; }
.header-box {
    background: linear-gradient(180deg, #0b0f14 0%, #1c1f26 100%);
    padding: 60px 40px;
    margin: -60px -4rem 40px;
    border-bottom: 4px solid #d90429;
    color: white;
}
.header-box h1 { font-family: 'Orbitron', sans-serif; font-size: 48px; margin: 0; }
.section-title { font-family: 'Orbitron', sans-serif; border-left: 5px solid #d90429; padding-left: 15px; margin-top: 30px; text-transform: uppercase; }
.alert-container { border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e5e7eb; }
.alert-critical { background: #fff5f5; border-left: 8px solid #dc2626; }
.alert-ok { background: #f6fff9; border-left: 8px solid #16a34a; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATA ENGINE & MAPPING
# ======================================================
CHANNELS_MAP = {
    'rpm': ['Motor RPM', 'Engine RPM', 'RPM', 'nMot'],
    'load': ['Engine load', 'MAP', 'Boost', 'pManifold'],
    'tps': ['Throttle pos.', 'Throttle position', 'TPS', 'AccPedal'],
    'lambda1': ['Lambda #1 integrator', 'Lambda #1 integrator ', 'Lambda1'],
    'ign': ['Ignition angle', 'Advance', 'Ign_Advance'],
    'iat': ['Intake temp.', 'IAT', 'Air_Temp'],
    'knock1': ['Knock sensor #1', 'Knock1'],
    'maf': ['Air mass', 'MAF', 'Mass_Air_Flow'],
    'inj': ['Injection time', 'Inj_Time', 'tInj']
}

def auto_map(df):
    mapped = {}
    for k, variants in CHANNELS_MAP.items():
        for v in variants:
            if v in df.columns:
                mapped[k] = v
                break
    return mapped

def clean_data(df, mapped):
    # Fix Boost (mBar to Bar)
    if 'load' in mapped:
        if df[mapped['load']].max() > 500:
            df[mapped['load']] /= 1000.0
    
    # Fill missing essentials with 0 to prevent crashes
    for k in ['rpm', 'tps', 'load', 'lambda1', 'knock1', 'iat', 'ign', 'maf']:
        if k not in mapped:
            df[f"DUMMY_{k}"] = 0.0
            mapped[k] = f"DUMMY_{k}"
    return df, mapped

# ======================================================
# ADVANCED ANALYTICS MODULES
# ======================================================
class EngineScience:
    @staticmethod
    def calculate_ve(maf, rpm, map_bar, iat, displacement=2.0):
        if rpm.max() < 500: return 0
        temp_k = iat + 273.15
        rho_manifold = (map_bar * 100000) / (287.05 * temp_k)
        theoretical = (displacement / 1000) * (rpm / 120) * rho_manifold * 3600
        return (maf / theoretical.max()) * 100 if theoretical.max() > 0 else 0

# ======================================================
# APPLICATION INTERFACE
# ======================================================
def main():
    st.markdown('<div class="header-box"><h1>LZTUNED ARCHITECT <span style="color:#d90429">PRO</span></h1><p>ENTERPRISE ECU CALIBRATION SUITE</p></div>', unsafe_allow_html=True)
    
    file = st.file_uploader("📂 INCARCA LOG-UL MOTORSPORT (.CSV)", type="csv")
    if not file:
        st.info("Sistem în așteptare. Încarcă un fișier CSV pentru analiză.")
        return

    df_raw = pd.read_csv(file, sep=';')
    mapped = auto_map(df_raw)
    df, mapped = clean_data(df_raw, mapped)

    # --- TELEMETRY DASHBOARD ---
    st.markdown("<h2 class='section-title'>Live Engine Telemetry</h2>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("PEAK RPM", int(df[mapped['rpm']].max()))
    k2.metric("MAX BOOST", f"{df[mapped['load']].max():.2f} bar")
    k3.metric("IAT MAX", f"{df[mapped['iat']].max()}°C")
    k4.metric("KNOCK PEAK", f"{df[mapped['knock1']].max():.2f}V")

    t_diag, t_advanced, t_report = st.tabs(["🔍 DIAGNOSTIC", "🧪 ADVANCED LAB", "📄 REPORT GEN"])

    with t_diag:
        st.subheader("Analiză Automată Stare Motor")
        if df[mapped['knock1']].max() > 1.8:
            st.markdown('<div class="alert-container alert-critical"><b>CRITICAL:</b> Detonație detectată! Redu avansul cu 2-3 grade.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-container alert-ok"><b>OPTIM:</b> Parametrii de aprindere sunt stabili.</div>', unsafe_allow_html=True)
        
        fig = px.line(df, x=df.index, y=[mapped['rpm'], mapped['tps']], title="Corelație RPM vs TPS")
        st.plotly_chart(fig, use_container_width=True)

    with t_advanced:
        st.subheader("Science & Physics Lab")
        ve = EngineScience.calculate_ve(df[mapped['maf']].max(), df[mapped['rpm']], df[mapped['load']].max(), df[mapped['iat']].max())
        st.metric("Efficiency (VE)", f"{ve:.1f}%")
        
        # Driver aggression
        diff = np.abs(np.diff(df[mapped['tps']]))
        score = np.mean(diff) * 10
        st.metric("Driver Aggression Index", f"{score:.2f}")

    with t_report:
        if st.button("🏗️ GENEREAZĂ RAPORT PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "LZTUNED ENTERPRISE DIAGNOSTIC", 0, 1, "C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.cell(0, 10, f"Peak RPM: {int(df[mapped['rpm']].max())}", 0, 1)
            pdf.cell(0, 10, f"Max Boost: {df[mapped['load']].max():.2f} bar", 0, 1)
            
            pdf_out = pdf.output(dest='S').encode('latin-1')
            b64 = base64.b64encode(pdf_out).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="Raport_LZTuned.pdf" style="padding:15px; background:#d90429; color:white; border-radius:8px; text-decoration:none;">📥 DESCARCĂ RAPORTUL</a>'
            st.markdown(href, unsafe_allow_html=True)

# ======================================================
# MOTORSPORT ENGINEERING MODULES (FUNCTII NOI)
# ======================================================

def calculate_estimated_power(df, mapped, weight_kg=1500):
    """Calculează puterea estimativă la roată bazată pe accelerare (VSS Delta)"""
    if 'vss' in mapped and 'time' in mapped:
        df['speed_ms'] = df[mapped['vss']] / 3.6
        df['accel'] = df['speed_ms'].diff() / df['time'].diff()
        # F = m * a
        df['force'] = weight_kg * df['accel']
        # P = F * v
        df['power_kw'] = (df['force'] * df['speed_ms']) / 1000
        df['hp'] = df['power_kw'] * 1.34102
        return df['hp'].max()
    return 0

def analyze_lambda_safety(df, mapped):
    """Analizează diferența dintre bănci (Lambda Bank Deviation)"""
    if 'lambda1' in mapped and 'lambda2' in mapped:
        deviation = np.abs(df[mapped['lambda1']] - df[mapped['lambda2']]).mean()
        return deviation
    return 0

def detect_misfires(df, mapped):
    """Detectează potențiale misfire-uri prin analiza fluctuațiilor RPM la ralanti"""
    if 'rpm' in mapped:
        rpm_smooth = df[mapped['rpm']].rolling(window=5).mean()
        rpm_delta = np.abs(df[mapped['rpm']] - rpm_smooth)
        return rpm_delta.max()
    return 0

def get_performance_summary(df, mapped):
    """Generează un obiect de sumar pentru raportul final"""
    summary = {
        "max_boost": df[mapped['load']].max(),
        "max_rpm": df[mapped['rpm']].max(),
        "avg_iat": df[mapped['iat']].mean(),
        "peak_knock": df[mapped['knock1']].max(),
        "hp_est": calculate_estimated_power(df, mapped)
    }
    return summary

# ======================================================
# INTEGRARE IN INTERFATA (In interiorul functiei main)
# ======================================================
# Adaugă acest bloc în interiorul funcției main(), sub tab-uri sau într-un tab nou:

def display_advanced_analytics(df, mapped):
    st.markdown("<h2 class='section-title'>🧬 Deep Data Forensics</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hp = calculate_estimated_power(df, mapped)
        st.metric("EST. PEAK HP", f"{hp:.1f} HP", help="Calculat pe baza accelerației masei vehiculului")
        
    with col2:
        dev = analyze_lambda_safety(df, mapped)
        status = "SAFE" if dev < 0.05 else "CHECK INJECTORS"
        st.metric("BANK DEVIATION", f"{dev:.4f} λ", delta=status, delta_color="inverse")
        
    with col3:
        misfire_index = detect_misfires(df, mapped)
        st.metric("STABILITY INDEX", f"{misfire_index:.1f}", help="Fluctuația RPM. Valori mari indică aprindere instabilă.")

    # Grafic suprapus pentru presiune vs aprindere
    fig_adv = make_subplots(specs=[[{"secondary_y": True}]])
    fig_adv.add_trace(go.Scatter(x=df.index, y=df[mapped['load']], name="Boost (Bar)", line=dict(color="red")), secondary_y=False)
    fig_adv.add_trace(go.Scatter(x=df.index, y=df[mapped['ign']], name="Ignition Angle", line=dict(color="blue", dash="dash")), secondary_y=True)
    fig_adv.update_layout(title="Relationship: Load vs Ignition Timing")
    st.plotly_chart(fig_adv, use_container_width=True)



# ======================================================
# FINAL SCRIPT EXECUTION
# ======================================================

# ======================================================
# MODULE TEHNICE AVANSATE (ENTERPRISE GRADE)
# ======================================================

class ThermalDynamics:
    @staticmethod
    def analyze_cooling_efficiency(df, mapped):
        """Analizează cât de repede scade temperatura după un Pull (Heat Soak recovery)"""
        if 'ect' in mapped and 'iat' in mapped:
            ect_start = df[mapped['ect']].iloc[0]
            ect_max = df[mapped['ect']].max()
            recovery_rate = (ect_max - df[mapped['ect']].iloc[-1])
            return {
                "ect_delta": ect_max - ect_start,
                "heat_soak_risk": "HIGH" if df[mapped['iat']].max() > 60 else "NORMAL",
                "recovery": recovery_rate
            }
        return None

class FuelSystemForensics:
    @staticmethod
    def calculate_injector_headroom(df, mapped):
        """Calculează limita fizică a injectoarelor (Duty Cycle vs RPM)"""
        if 'inj' in mapped and 'rpm' in mapped:
            # Duty Cycle (%) = (Injection Time * RPM) / 1200
            dc = (df[mapped['inj']] * df[mapped['rpm']]) / 1200
            max_dc = dc.max()
            status = "DANGER" if max_dc > 90 else "SAFE"
            return max_dc, status
        return 0, "N/A"

class IgnitionStability:
    @staticmethod
    def spark_jitter_analysis(df, mapped):
        """Analizează instabilitatea avansului (Jitter) care indică probleme de senzori"""
        if 'ign' in mapped:
            jitter = df[mapped['ign']].diff().abs().mean()
            return jitter
        return 0

class GearRatioCalculator:
    @staticmethod
    def detect_gear_slips(df, mapped):
        """Detectează dacă patinează ambreiajul (Raport RPM / Viteza)"""
        if 'rpm' in mapped and 'vss' in mapped:
            # Evităm diviziunea la zero
            valid = df[df[mapped['vss']] > 10]
            if not valid.empty:
                ratio = valid[mapped['rpm']] / valid[mapped['vss']]
                ratio_std = ratio.std()
                # O deviație standard mare în treaptă indică patinare
                return "SLIP DETECTED" if ratio_std > 5 else "STABLE"
        return "N/A"

# ======================================================
# INTEGRARE ÎN INTERFAȚA (Tab-ul LAB AVANSAT)
# ======================================================

def display_forensic_modules(df, mapped):
    st.markdown("<h2 class='section-title'>🛡️ Hardware Safety Forensics</h2>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        dc, status = FuelSystemForensics.calculate_injector_headroom(df, mapped)
        color = "normal" if status == "SAFE" else "inverse"
        st.metric("INJECTOR DUTY", f"{dc:.1f}%", delta=status, delta_color=color)
        st.caption("Peste 85% indică injectoare prea mici.")

    with m2:
        thermal = ThermalDynamics.analyze_cooling_efficiency(df, mapped)
        if thermal:
            st.metric("HEAT SOAK RISK", thermal['heat_soak_risk'], delta=f"{thermal['ect_delta']:.1f}°C")
            st.caption("Variația temperaturii apei în log.")

    with m3:
        jitter = IgnitionStability.spark_jitter_analysis(df, mapped)
        st.metric("IGN JITTER", f"{jitter:.3f}°", help="Instabilitatea scânteii. Valori mari = senzori de vibrație defecti.")

    with m4:
        slip = GearRatioCalculator.detect_gear_slips(df, mapped)
        st.metric("CLUTCH STATUS", slip)
        st.caption("Analiza patinării ambreiajului.")

    # Vizualizare grafică pentru Injector Duty Cycle
    if 'inj' in mapped:
        df['dc_calc'] = (df[mapped['inj']] * df[mapped['rpm']]) / 1200
        fig_dc = px.area(df, x=df.index, y='dc_calc', title="Injector Duty Cycle Trend (%)", color_discrete_sequence=['#ff4b4b'])
        st.plotly_chart(fig_dc, use_container_width=True)


if __name__ == "__main__":
    main()


