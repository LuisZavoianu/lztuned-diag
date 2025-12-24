import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from collections import defaultdict
import warnings
import base64
from io import BytesIO

warnings.filterwarnings('ignore')

# ====================================================== 
# CONFIGURATION & STYLING
# ======================================================
st.set_page_config(
    page_title="LZTuned Architect Pro - ECU Interpretation Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Orbitron:wght@700;900&display=swap');

.stApp { background: #ffffff; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #0b0f14; }

.header-box { background: linear-gradient(180deg, #ffffff 0%, #f1f3f5 100%);
             padding: 50px 20px; border-bottom: 1px solid #dee2e6; text-align: center; margin: -60px -4rem 40px; }
.header-box h1 { font-family: 'Orbitron', sans-serif; font-size: 42px; font-weight: 900; color: #0b0f14; margin: 0; letter-spacing: -1px; }
.header-box p { font-size: 13px; color: #6c757d; letter-spacing: 3px; margin-top: 8px; }

.section-title { font-family: 'Orbitron', sans-serif; font-size: 16px; letter-spacing: 2px;
                 margin: 40px 0 20px; padding-left: 12px; border-left: 5px solid #d90429; color: #0b0f14; text-transform: uppercase; }

.expert-card { background: #ffffff; border: 1px solid #e9ecef; padding: 20px; border-radius: 14px; min-height: 280px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
.resolution-box { background: #f8f9fa; border: 1px solid #dee2e6; padding: 25px; border-radius: 16px; margin-bottom: 20px; }
.res-title { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 10px; }
.res-body { font-size: 14px; line-height: 1.6; color: #495057; }

.confidence-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.why-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-top: 15px; border-radius: 8px; }
.detection-box { background: #e7f5ff; border: 1px solid #74c0fc; padding: 20px; border-radius: 12px; margin: 20px 0; }
.anomaly-alert { background: #fff5f5; border-left: 4px solid #d90429; padding: 15px; margin: 10px 0; border-radius: 8px; }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>LZTuned Architect Pro</h1><p>ECU Interpretation Engine</p></div>', unsafe_allow_html=True)

# ======================================================
# FILE UPLOAD
# ======================================================
st.sidebar.header("Load ECU Log CSV")
uploaded_file = st.sidebar.file_uploader("Choose CSV", type="csv")

ecu_type = st.sidebar.selectbox("Select ECU Type", ["ECUMaster", "MaxxECU", "Link"], index=0)
profile_mode = st.sidebar.selectbox("Select Driving Mode", ["Street", "Track", "Drift"], index=0)

if uploaded_file is None:
    st.info("Upload a CSV log to start analysis")
    st.stop()

df = pd.read_csv(uploaded_file)
st.success(f"CSV Loaded: {uploaded_file.name} ({len(df)} rows)")

# ======================================================
# CHANNEL DETECTION ENGINE
# ======================================================
class ChannelDetectionEngine:
    """Detectează și normalizează coloanele din orice log ECU"""
    
    CHANNEL_MAP = {
        'rpm': ['Motor RPM', 'RPM', 'Engine RPM', 'EngineRPM', 'rpm'],
        'load': ['Engine load', 'Load', 'Engine Load', 'MAP', 'Manifold Pressure'],
        'lambda1': ['Lambda #1 integrator ', 'Lambda 1', 'AFR 1', 'Lambda#1', 'O2 Sensor 1'],
        'lambda2': ['Lambda #2 integrator', 'Lambda 2', 'AFR 2', 'Lambda#2', 'O2 Sensor 2'],
        'knock1': ['Knock sensor #1', 'Knock 1', 'KnockSensor1', 'Knock #1'],
        'knock2': ['Knock sensor #2', 'Knock 2', 'KnockSensor2', 'Knock #2'],
        'inj_time': ['Injection time', 'Injector PW', 'Pulse Width', 'InjTime'],
        'oil_temp': ['Oil temp.', 'Oil Temp', 'Oil Temperature', 'OilTemp'],
        'coolant_temp': ['Coolant temp.', 'Coolant Temp', 'Water Temp', 'ECT'],
        'iat': ['IAT', 'Intake Air Temp', 'Air Temp', 'IntakeTemp'],
        'egt1': ['EGT 1', 'Exhaust Gas Temp 1', 'EGT#1'],
        'egt2': ['EGT 2', 'Exhaust Gas Temp 2', 'EGT#2'],
        'boost': ['Boost', 'Turbo Pressure', 'Manifold Pressure'],
        'fuel_pressure': ['Fuel Pressure', 'FuelPress', 'Rail Pressure'],
        'ignition_timing': ['Ignition timing', 'Timing', 'Spark Advance', 'IgnTiming'],
        'battery_voltage': ['Battery voltage', 'Voltage', 'Batt V', 'VBatt'],
        'tps': ['TPS', 'Throttle Position', 'Throttle %'],
        'stft': ['STFT', 'Short Term Fuel Trim', 'FuelTrimShort'],
        'ltft': ['LTFT', 'Long Term Fuel Trim', 'FuelTrimLong'],
    }
    
    def __init__(self, df):
        self.df = df
        self.detected = {}
        self.missing = []
        self.noisy = []
        self.confidence = {}
        
    def detect_channels(self):
        """Mapează automat coloanele din CSV către canale standard"""
        for std_name, variants in self.CHANNEL_MAP.items():
            found = False
            for variant in variants:
                if variant in self.df.columns:
                    self.detected[std_name] = variant
                    self.confidence[std_name] = self._assess_signal_quality(variant)
                    found = True
                    break
            if not found:
                self.missing.append(std_name)
        return self.detected
    
    def _assess_signal_quality(self, col):
        """Evaluează calitatea semnalului pentru o coloană"""
        data = self.df[col].dropna()
        if len(data) == 0: return 0.0
        null_pct = self.df[col].isnull().sum() / len(self.df) * 100
        constant_check = data.std() == 0
        flatline_pct = 0
        if not constant_check:
            consecutive_same = (data.diff() == 0).sum() / len(data) * 100
            flatline_pct = consecutive_same
        confidence = 100.0
        confidence -= null_pct
        if constant_check:
            confidence = 0
        elif flatline_pct > 50:
            confidence -= 40
            self.noisy.append(col)
        return max(0, min(100, confidence))
    
    def get_report(self):
        """Returnează raport detaliat despre detectare"""
        total_possible = len(self.CHANNEL_MAP)
        detected_count = len(self.detected)
        report = {
            'total_channels': len(self.df.columns),
            'detected': detected_count,
            'missing': len(self.missing),
            'noisy': len(self.noisy),
            'coverage': (detected_count / total_possible) * 100
        }
        return report

# ======================================================
# DETECT CHANNELS
# ======================================================
channel_engine = ChannelDetectionEngine(df)
channels = channel_engine.detect_channels()
report = channel_engine.get_report()

st.markdown('<h3 class="section-title">Channel Detection Report</h3>', unsafe_allow_html=True)
st.write(report)
st.write("Detected Channels:", channels)
if channel_engine.missing:
    st.warning(f"Missing channels: {channel_engine.missing}")
if channel_engine.noisy:
    st.info(f"Noisy channels: {channel_engine.noisy}")

# ======================================================
# MODES DETECTION
# ======================================================
class OperatingModeEngine:
    """Detectează regimurile de funcționare ale motorului"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.modes = pd.DataFrame(index=df.index)
        
    def detect_modes(self):
        rpm = self._get_channel('rpm', 0)
        load = self._get_channel('load', 0)
        tps = self._get_channel('tps', 0)
        
        self.modes['Idle'] = (rpm < 1500) & (load < 30)
        self.modes['Cruise'] = (rpm >= 1500) & (rpm <= 4000) & (load >= 30) & (load <= 60)
        if 'tps' in self.channels:
            tps_rate = tps.diff().fillna(0)
            self.modes['Acceleration'] = (tps_rate > 5) & (load > 40)
        else:
            load_rate = load.diff().fillna(0)
            self.modes['Acceleration'] = (load_rate > 10) & (rpm > 2000)
        self.modes['WOT'] = (load > 70) & (rpm > 3000)
        if 'tps' in self.channels:
            self.modes['Overrun'] = (tps < 5) & (rpm > 2000)
        else:
            self.modes['Overrun'] = (load < 20) & (rpm > 2000)
        coolant = self._get_channel('coolant_temp', 0)
        oil = self._get_channel('oil_temp', 0)
        self.modes['Heat_Soak'] = (coolant > 95) | (oil > 110)
        return self.modes
    
    def _get_channel(self, name, default):
        if name in self.channels:
            col = self.channels[name]
            return self.df[col].fillna(default)
        return pd.Series(default, index=self.df.index)
    
    def get_mode_summary(self):
        summary = {}
        for mode in self.modes.columns:
            count = self.modes[mode].sum()
            pct = (count / len(self.modes)) * 100
            summary[mode] = {'count': int(count), 'percentage': round(pct, 1)}
        return summary

mode_engine = OperatingModeEngine(df, channels)
modes_df = mode_engine.detect_modes()
mode_summary = mode_engine.get_mode_summary()
st.markdown('<h3 class="section-title">Operating Mode Summary</h3>', unsafe_allow_html=True)
st.write(mode_summary)

# ======================================================
# HEATMAP RPM vs LOAD
# ======================================================
st.markdown('<h3 class="section-title">RPM vs Load Heatmap</h3>', unsafe_allow_html=True)
if 'rpm' in channels and 'load' in channels:
    fig = px.density_heatmap(df, x=channels['rpm'], y=channels['load'], nbinsx=50, nbinsy=50,
                             color_continuous_scale='Viridis')
    fig.update_layout(height=500, width=900)
    st.plotly_chart(fig)

# ======================================================
# PDF EXPORT
# ======================================================
def generate_pdf(df, report, mode_summary):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="LZTuned ECU Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Channels detected: {len(channels)} / {len(ChannelDetectionEngine.CHANNEL_MAP)}", ln=True)
    for mode, val in mode_summary.items():
        pdf.cell(200, 10, txt=f"{mode}: {val['count']} points ({val['percentage']}%)", ln=True)
    return pdf

st.sidebar.markdown("### Export Options")
if st.sidebar.button("Export PDF Report"):
    pdf = generate_pdf(df, report, mode_summary)
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="LZTuned_Report.pdf">Download PDF</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

st.success("Analysis Complete! ✅")
