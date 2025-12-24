import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from collections import defaultdict
import warnings
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

.stApp {
    background: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0b0f14;
}

.header-box {
    background: linear-gradient(180deg, #ffffff 0%, #f1f3f5 100%);
    padding: 50px 20px;
    border-bottom: 1px solid #dee2e6;
    text-align: center;
    margin: -60px -4rem 40px;
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 42px;
    font-weight: 900;
    color: #0b0f14;
    margin: 0;
    letter-spacing: -1px;
}

.header-box p {
    font-size: 13px;
    color: #6c757d;
    letter-spacing: 3px;
    margin-top: 8px;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    letter-spacing: 2px;
    margin: 40px 0 20px;
    padding-left: 12px;
    border-left: 5px solid #d90429;
    color: #0b0f14;
    text-transform: uppercase;
}

.expert-card {
    background: #ffffff;
    border: 1px solid #e9ecef;
    padding: 20px;
    border-radius: 14px;
    min-height: 280px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}

.resolution-box {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 20px;
}

.res-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
}

.res-body {
    font-size: 14px;
    line-height: 1.6;
    color: #495057;
}

.confidence-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.why-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 15px;
    margin-top: 15px;
    border-radius: 8px;
}

.detection-box {
    background: #e7f5ff;
    border: 1px solid #74c0fc;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
}

.anomaly-alert {
    background: #fff5f5;
    border-left: 4px solid #d90429;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
}

/* =========================
   GLOBAL BASE
========================= */
.main {
    background: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0b0f14;
}

/* =========================
   HEADER – PREMIUM / APPLE STYLE
========================= */
.header-box {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f5f6f8 100%
    );
    padding: 70px 20px 60px;
    margin: -60px -4rem 60px;
    border-bottom: 1px solid #e5e7eb;
    text-align: center;
}

.header-box h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(28px, 5vw, 46px);
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 10px;
    color: #0b0f14;
}

.header-box p {
    font-size: 13px;
    letter-spacing: 3px;
    color: #6b7280;
    text-transform: uppercase;
}

/* =========================
   SECTION TITLES
========================= */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    margin: 60px 0 30px;
    padding-left: 14px;
    border-left: 4px solid #d90429;
    color: #0b0f14;
    text-transform: uppercase;
}

/* =========================
   KPI METRICS
========================= */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}

div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px;
    color: #6b7280 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #0b0f14 !important;
}

/* =========================
   ALERTS / VERDICT
========================= */
.alert-container {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 24px;
    border: 1px solid #e5e7eb;
}

.alert-critical {
    border-left: 6px solid #dc2626;
}

.alert-warning {
    border-left: 6px solid #f59e0b;
}

.alert-ok {
    border-left: 6px solid #16a34a;
}

.alert-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

.alert-body {
    font-size: 15px;
    color: #374151;
}

.alert-action {
    margin-top: 14px;
    padding: 14px;
    background: #f5f6f8;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* =========================
   EXPANDERS
========================= */
.streamlit-expanderHeader {
    background: #f5f6f8 !important;
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
    font-weight: 600 !important;
}

/* =========================
   SENSOR CARD
========================= */
.sensor-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    font-size: 14px;
    line-height: 1.6;
}

/* =========================
   TABS – CLEAN / PREMIUM
========================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: #f5f6f8 !important;
    border-radius: 10px;
    padding: 10px 24px;
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    letter-spacing: 2px;
    color: #6b7280 !important;
}

.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    color: #0b0f14 !important;
}

/* =========================
   FILE UPLOADER
========================= */
section[data-testid="stFileUploader"] {
    background: #f9fafb;
    border: 2px dashed #d1d5db;
    border-radius: 16px;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# CORE: CHANNEL DETECTION & NORMALIZATION ENGINE
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

    """, unsafe_allow_html=True)

    # File Uploader Stilizat implicit
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        file = st.file_uploader("📂 DRAG & DROP ECU LOG (.CSV)", type="csv")
    
    if not file:
        st.markdown("<div style='text-align:center; padding:50px; color:#4da3ff; font-family:Orbitron;'>SYSTEM IDLE - WAITING FOR DATA INPUT...</div>", unsafe_allow_html=True)
        return

    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()
    
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
        
        if len(data) == 0:
            return 0.0
        
        # Verificări de calitate
        null_pct = self.df[col].isnull().sum() / len(self.df) * 100
        constant_check = data.std() == 0
        
        # Detectare flatline (valori constante consecutive)
        flatline_pct = 0
        if not constant_check:
            consecutive_same = (data.diff() == 0).sum() / len(data) * 100
            flatline_pct = consecutive_same
        
        # Scor de confidence
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
# CORE: OPERATING MODE DETECTION ENGINE
# ======================================================
class OperatingModeEngine:
    """Identifică regimurile de funcționare ale motorului"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.modes = pd.DataFrame(index=df.index)
        
    def detect_modes(self):
        """Detectează toate regimurile de funcționare"""
        rpm = self._get_channel('rpm', 0)
        load = self._get_channel('load', 0)
        tps = self._get_channel('tps', 0)
        
        # IDLE: RPM < 1500, Load < 30%
        self.modes['Idle'] = (rpm < 1500) & (load < 30)
        
        # CRUISE: RPM 1500-4000, Load 30-60%, TPS stabil
        self.modes['Cruise'] = (rpm >= 1500) & (rpm <= 4000) & (load >= 30) & (load <= 60)
        
        # ACCELERATION: TPS rate > 5%/s, Load crescător
        if 'tps' in self.channels:
            tps_rate = tps.diff().fillna(0)
            self.modes['Acceleration'] = (tps_rate > 5) & (load > 40)
        else:
            load_rate = load.diff().fillna(0)
            self.modes['Acceleration'] = (load_rate > 10) & (rpm > 2000)
        
        # WOT: Load > 70%, RPM > 3000
        self.modes['WOT'] = (load > 70) & (rpm > 3000)
        
        # OVERRUN: TPS < 5%, RPM > 2000 (deceleration cu motor brake)
        if 'tps' in self.channels:
            self.modes['Overrun'] = (tps < 5) & (rpm > 2000)
        else:
            self.modes['Overrun'] = (load < 20) & (rpm > 2000)
        
        # HEAT SOAK: Coolant > 95°C sau Oil > 110°C
        coolant = self._get_channel('coolant_temp', 0)
        oil = self._get_channel('oil_temp', 0)
        self.modes['Heat_Soak'] = (coolant > 95) | (oil > 110)
        
        return self.modes
    
    def _get_channel(self, name, default):
        """Helper pentru a obține canal cu fallback"""
        if name in self.channels:
            col = self.channels[name]
            return self.df[col].fillna(default)
        return pd.Series(default, index=self.df.index)
    
    def get_mode_summary(self):
        """Returnează statistici despre regimuri"""
        summary = {}
        for mode in self.modes.columns:
            count = self.modes[mode].sum()
            pct = (count / len(self.modes)) * 100
            summary[mode] = {'count': int(count), 'percentage': round(pct, 1)}
        return summary

# ======================================================
# CORE: ADVANCED FUEL ANALYSIS ENGINE
# ======================================================
class FuelAnalysisEngine:
    """Analiză avansată a sistemului de alimentare"""
    
    def __init__(self, df, channels, modes):
        self.df = df
        self.channels = channels
        self.modes = modes
        self.results = {}
        
    def analyze(self):
        """Rulează analiza completă de fuel"""
        self._analyze_lambda()
        self._analyze_injector_duty()
        self._analyze_fuel_trims()
        self._analyze_linearity()
        
        return self.results
    
    def _analyze_lambda(self):
        """Analiză Lambda cu separare pe regimuri"""
        l1 = self._get_channel('lambda1')
        l2 = self._get_channel('lambda2')
        
        if l1 is None:
            self.results['lambda'] = {'status': 'NO_DATA', 'confidence': 0}
            return
        
        # Calculează media
        if l2 is not None:
            lambda_avg = (l1 + l2) / 2
        else:
            lambda_avg = l1
        
        self.df['Lambda_Avg'] = lambda_avg
        
        # Analiză pe WOT
        wot_lambda = lambda_avg[self.modes['WOT']]
        
        if len(wot_lambda) > 0:
            mean_wot = wot_lambda.mean()
            std_wot = wot_lambda.std()
            
            # Verdict
            if mean_wot > 0.86:
                status = 'LEAN_DANGER'
                severity = 'CRITICAL'
            elif mean_wot < 0.78:
                status = 'RICH_INEFFICIENT'
                severity = 'WARNING'
            else:
                status = 'OPTIMAL'
                severity = 'SAFE'
            
            self.results['lambda'] = {
                'status': status,
                'severity': severity,
                'mean_wot': round(mean_wot, 3),
                'std_wot': round(std_wot, 3),
                'min_wot': round(wot_lambda.min(), 3),
                'confidence': 95 if l2 is not None else 75
            }
        else:
            self.results['lambda'] = {
                'status': 'NO_WOT_DATA',
                'confidence': 0
            }
    
    def _analyze_injector_duty(self):
        """Analiză duty cycle injectoare"""
        inj_time = self._get_channel('inj_time')
        rpm = self._get_channel('rpm')
        
        if inj_time is None or rpm is None:
            self.results['duty'] = {'status': 'NO_DATA', 'confidence': 0}
            return
        
        # Calculează Duty Cycle
        rpm_safe = rpm.replace(0, np.nan)
        duty = (inj_time * rpm_safe) / 1200
        self.df['Inj_Duty'] = duty
        
        max_duty = duty.max()
        
        # Analiză slope (linearity)
        wot_duty = duty[self.modes['WOT']]
        wot_rpm = rpm[self.modes['WOT']]
        
        if len(wot_duty) > 10:
            slope, intercept, r_value, _, _ = stats.linregress(wot_rpm, wot_duty)
            linearity = abs(r_value)
        else:
            linearity = 0
        
        # Verdict
        if max_duty > 90:
            status = 'SATURATED'
            severity = 'CRITICAL'
        elif max_duty > 85:
            status = 'NEAR_LIMIT'
            severity = 'WARNING'
        else:
            status = 'HEALTHY'
            severity = 'SAFE'
        
        self.results['duty'] = {
            'status': status,
            'severity': severity,
            'max_duty': round(max_duty, 1),
            'linearity': round(linearity, 2),
            'confidence': 90
        }
    
    def _analyze_fuel_trims(self):
        """Analiză fuel trim (STFT/LTFT)"""
        stft = self._get_channel('stft')
        ltft = self._get_channel('ltft')
        
        if stft is None and ltft is None:
            self.results['fuel_trim'] = {'status': 'NO_DATA', 'confidence': 0}
            return
        
        # Analiză deviație
        if stft is not None:
            stft_mean = stft.mean()
            stft_std = stft.std()
            
            if abs(stft_mean) > 10:
                status = 'ADAPTATION_ACTIVE'
                severity = 'WARNING'
            else:
                status = 'STABLE'
                severity = 'SAFE'
            
            self.results['fuel_trim'] = {
                'status': status,
                'severity': severity,
                'stft_mean': round(stft_mean, 2),
                'stft_std': round(stft_std, 2),
                'confidence': 85
            }
    
    def _analyze_linearity(self):
        """Verifică liniaritatea fuel delivery"""
        if 'Inj_Duty' not in self.df.columns or 'Lambda_Avg' not in self.df.columns:
            return
        
        wot_duty = self.df.loc[self.modes['WOT'], 'Inj_Duty']
        wot_lambda = self.df.loc[self.modes['WOT'], 'Lambda_Avg']
        
        if len(wot_duty) > 10:
            # Duty crescător ar trebui să producă Lambda descrescător
            correlation = wot_duty.corr(wot_lambda)
            
            if correlation > -0.3:  # Corelație slabă sau pozitivă = PROBLEMĂ
                self.results['linearity'] = {
                    'status': 'NON_LINEAR',
                    'severity': 'WARNING',
                    'correlation': round(correlation, 2),
                    'explanation': 'Creșterea duty-ului nu produce scădere lambda → injectoare subdimensionate sau presiune inconsistentă'
                }
    
    def _get_channel(self, name):
        """Helper cu None fallback"""
        if name in self.channels:
            return self.df[self.channels[name]]
        return None

# ======================================================
# CORE: ADVANCED IGNITION ANALYSIS ENGINE
# ======================================================
class IgnitionAnalysisEngine:
    """Analiză avansată a sistemului de aprindere"""
    
    def __init__(self, df, channels, modes):
        self.df = df
        self.channels = channels
        self.modes = modes
        self.results = {}
        
    def analyze(self):
        """Rulează analiza completă de ignition"""
        self._analyze_knock()
        self._analyze_timing_stability()
        self._analyze_knock_correlation()
        
        return self.results
    
    def _analyze_knock(self):
        """Analiză detonație cu clustering și threshold adaptat"""
        k1 = self._get_channel('knock1')
        k2 = self._get_channel('knock2')
        
        if k1 is None:
            self.results['knock'] = {'status': 'NO_DATA', 'confidence': 0}
            return
        
        # Calculează peak knock
        if k2 is not None:
            knock_peak = np.maximum(k1, k2)
        else:
            knock_peak = k1
        
        self.df['Knock_Peak'] = knock_peak
        
        # Statistici
        max_knock = knock_peak.max()
        mean_knock = knock_peak.mean()
        
        # Detectare evenimente knock (peste 1.2V)
        knock_events = (knock_peak > 1.2).sum()
        knock_event_pct = (knock_events / len(knock_peak)) * 100
        
        # Knock clustering (eventi în burst vs sporadic)
        knock_mask = knock_peak > 1.2
        knock_bursts = (knock_mask.astype(int).diff() == 1).sum()
        
        # Verdict
        if max_knock > 1.5:
            status = 'SEVERE_DETONATION'
            severity = 'CRITICAL'
        elif max_knock > 1.2:
            if knock_event_pct > 5:
                status = 'SUSTAINED_KNOCK'
                severity = 'CRITICAL'
            else:
                status = 'SPORADIC_KNOCK'
                severity = 'WARNING'
        else:
            status = 'SAFE'
            severity = 'SAFE'
        
        self.results['knock'] = {
            'status': status,
            'severity': severity,
            'max_knock': round(max_knock, 3),
            'mean_knock': round(mean_knock, 3),
            'events': int(knock_events),
            'event_pct': round(knock_event_pct, 2),
            'bursts': int(knock_bursts),
            'confidence': 90 if k2 is not None else 70
        }
    
    def _analyze_timing_stability(self):
        """Analiză stabilitate avans la aprindere"""
        timing = self._get_channel('ignition_timing')
        
        if timing is None:
            return
        
        wot_timing = timing[self.modes['WOT']]
        
        if len(wot_timing) > 0:
            std_timing = wot_timing.std()
            
            if std_timing > 3:
                status = 'UNSTABLE'
                severity = 'WARNING'
            else:
                status = 'STABLE'
                severity = 'SAFE'
            
            self.results['timing_stability'] = {
                'status': status,
                'severity': severity,
                'std': round(std_timing, 2),
                'confidence': 80
            }
    
    def _analyze_knock_correlation(self):
        """Analiză corelație knock cu alți parametri"""
        if 'Knock_Peak' not in self.df.columns:
            return
        
        knock = self.df['Knock_Peak']
        
        # Corelație cu Lambda
        if 'Lambda_Avg' in self.df.columns:
            lambda_corr = knock.corr(self.df['Lambda_Avg'])
            
            if abs(lambda_corr) < 0.2:
                # Knock independent de lambda = PROBLEMA MECHANICĂ
                self.results['knock_cause'] = {
                    'type': 'MECHANICAL',
                    'explanation': 'Knock apare independent de lambda → zgomot mecanic sau timing problem, nu fueling'
                }
            else:
                self.results['knock_cause'] = {
                    'type': 'FUELING_RELATED',
                    'explanation': 'Knock corelat cu lambda → verifică amestec și calitate combustibil'
                }
    
    def _get_channel(self, name):
        if name in self.channels:
            return self.df[self.channels[name]]
        return None

# ======================================================
# CORE: THERMAL & MECHANICAL STRESS ENGINE
# ======================================================
class ThermalStressEngine:
    """Analiză stres termic și mecanic"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.results = {}
        
    def analyze(self):
        """Rulează analiza termică completă"""
        self._analyze_oil_stress()
        self._analyze_coolant_stress()
        self._analyze_egt()
        self._analyze_thermal_rate()
        
        return self.results
    
    def _analyze_oil_stress(self):
        """Analiză stres termic ulei"""
        oil = self._get_channel('oil_temp')
        
        if oil is None:
            self.results['oil'] = {'status': 'NO_DATA'}
            return
        
        max_oil = oil.max()
        
        # Detectare sustained high temp
        high_temp_duration = (oil > 110).sum()
        high_temp_minutes = high_temp_duration / 60  # presupunem 1Hz sampling
        
        if max_oil > 125:
            status = 'CRITICAL_OVERHEAT'
            severity = 'CRITICAL'
        elif max_oil > 115:
            status = 'OVERHEAT'
            severity = 'WARNING'
        elif high_temp_minutes > 5:
            status = 'SUSTAINED_HIGH'
            severity = 'WARNING'
        else:
            status = 'HEALTHY'
            severity = 'SAFE'
        
        self.results['oil'] = {
            'status': status,
            'severity': severity,
            'max': round(max_oil, 1),
            'sustained_high_min': round(high_temp_minutes, 1),
            'confidence': 90
        }
    
    def _analyze_coolant_stress(self):
        """Analiză stres termic coolant"""
        coolant = self._get_channel('coolant_temp')
        
        if coolant is None:
            return
        
        max_coolant = coolant.max()
        
        if max_coolant > 105:
            status = 'OVERHEATING'
            severity = 'CRITICAL'
        elif max_coolant > 98:
            status = 'HIGH'
            severity = 'WARNING'
        else:
            status = 'NORMAL'
            severity = 'SAFE'
        
        self.results['coolant'] = {
            'status': status,
            'severity': severity,
            'max': round(max_coolant, 1),
            'confidence': 90
        }
    
    def _analyze_egt(self):
        """Analiză EGT (Exhaust Gas Temperature)"""
        egt1 = self._get_channel('egt1')
        
        if egt1 is None:
            return
        
        max_egt = egt1.max()
        
        if max_egt > 950:
            status = 'TURBO_RISK'
            severity = 'CRITICAL'
        elif max_egt > 900:
            status = 'HIGH'
            severity = 'WARNING'
        else:
            status = 'SAFE'
            severity = 'SAFE'
        
        self.results['egt'] = {
            'status': status,
            'severity': severity,
            'max': round(max_egt, 0),
            'confidence': 85
        }
    
    def _analyze_thermal_rate(self):
        """Analiză rată de creștere termică"""
        oil = self._get_channel('oil_temp')
        
        if oil is None:
            return
        
        # Calculează delta rate (°C/sec)
        oil_rate = oil.diff().abs()
        max_rate = oil_rate.max()
        
        if max_rate > 5:
            self.results['thermal_shock'] = {
                'status': 'RAPID_CHANGE',
                'severity': 'WARNING',
                'max_rate': round(max_rate, 2),
                'explanation': 'Schimbare termică rapidă poate cauza stress material'
            }
    
    def _get_channel(self, name):
        if name in self.channels:
            return self.df[self.channels[name]]
        return None

# ======================================================
# CORE: ELECTRICAL HEALTH ENGINE
# ======================================================
class ElectricalHealthEngine:
    """Analiză sănătate electrică și senzori"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.results = {}
        
    def analyze(self):
        """Rulează analiza electrică"""
        self._analyze_voltage()
        self._analyze_sensor_health()
        
        return self.results
    
    def _analyze_voltage(self):
        """Analiză stabilitate voltage"""
        voltage = self._get_channel('battery_voltage')
        
        if voltage is None:
            return
        
        min_v = voltage.min()
        max_v = voltage.max()
        std_v = voltage.std()
        
        if min_v < 12.5:
            status = 'LOW_VOLTAGE'
            severity = 'WARNING'
        elif std_v > 1.0:
            status = 'UNSTABLE'
            severity = 'WARNING'
        else:
            status = 'STABLE'
            severity = 'SAFE'
        
        self.results['voltage'] = {
            'status': status,
            'severity': severity,
            'min': round(min_v, 2),
            'max': round(max_v, 2),
            'std': round(std_v, 2),
            'confidence': 85
        }
    
    def _analyze_sensor_health(self):
        """Detectare senzori defecți (flatline, dropout)"""
        sensor_issues = []
        
        for sensor_name, col_name in self.channels.items():
            data = self.df[col_name]
            
            # Flatline detection
            if data.std() == 0:
                sensor_issues.append({
                    'sensor': sensor_name,
                    'issue': 'FLATLINE',
                    'description': f'{sensor_name} returnează valoare constantă'
                })
            
            # Dropout detection (mai mult de 10% null)
            null_pct = data.isnull().sum() / len(data) * 100
            if null_pct > 10:
                sensor_issues.append({
                    'sensor': sensor_name,
                    'issue': 'DROPOUT',
                    'description': f'{sensor_name} are {null_pct:.1f}% date lipsă'
                })
        
        if sensor_issues:
            self.results['sensor_health'] = {
                'status': 'ISSUES_DETECTED',
                'issues': sensor_issues,
                'confidence': 75
            }
    
    def _get_channel(self, name):
        if name in self.channels:
            return self.df[self.channels[name]]
        return None

# ======================================================
# CORE: ANOMALY DETECTION ENGINE
# ======================================================
class AnomalyDetectionEngine:
    """Detectare anomalii și pattern-uri rare"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.anomalies = []
        
    def detect(self):
        """Detectează anomalii în toate canalele principale"""
        
        # Detectare spike-uri (valori > 3 std dev)
        for sensor_name, col_name in self.channels.items():
            data = self.df[col_name].dropna()
            
            if len(data) < 10:
                continue
            
            mean = data.mean()
            std = data.std()
            
            if std == 0:
                continue
            
            # Z-score method
            z_scores = np.abs((data - mean) / std)
            spikes = z_scores > 3
            
            if spikes.sum() > 0:
                spike_indices = data[spikes].index.tolist()
                self.anomalies.append({
                    'type': 'SPIKE',
                    'sensor': sensor_name,
                    'count': int(spikes.sum()),
                    'max_deviation': round(z_scores.max(), 2),
                    'indices': spike_indices[:5],  # Primele 5
                    'severity': 'WARNING' if spikes.sum() < 3 else 'CRITICAL'
                })
        
        # Detectare sudden drops (căderi bruște)
        rpm_col = self.channels.get('rpm')
        if rpm_col:
            rpm = self.df[rpm_col]
            rpm_diff = rpm.diff().abs()
            sudden_drops = rpm_diff > 1000  # Drop > 1000 RPM
            
            if sudden_drops.sum() > 0:
                self.anomalies.append({
                    'type': 'SUDDEN_DROP',
                    'sensor': 'rpm',
                    'count': int(sudden_drops.sum()),
                    'explanation': 'Posibil wheel hop, misfire sau întrerupere în log',
                    'severity': 'WARNING'
                })
        
        return self.anomalies

# ======================================================
# CORE: CORRELATION ENGINE
# ======================================================
class CorrelationEngine:
    """Analiză corelații între parametri"""
    
    def __init__(self, df, channels):
        self.df = df
        self.channels = channels
        self.correlations = {}
        
    def analyze(self):
        """Calculează corelații importante"""
        
        # RPM vs Knock
        if 'rpm' in self.channels and 'Knock_Peak' in self.df.columns:
            rpm = self.df[self.channels['rpm']]
            knock = self.df['Knock_Peak']
            corr = rpm.corr(knock)
            
            self.correlations['rpm_knock'] = {
                'value': round(corr, 3),
                'interpretation': self._interpret_correlation(corr, 'rpm', 'knock')
            }
        
        # Lambda vs EGT
        if 'Lambda_Avg' in self.df.columns and 'egt1' in self.channels:
            lambda_avg = self.df['Lambda_Avg']
            egt = self.df[self.channels['egt1']]
            corr = lambda_avg.corr(egt)
            
            self.correlations['lambda_egt'] = {
                'value': round(corr, 3),
                'interpretation': self._interpret_correlation(corr, 'lambda', 'egt')
            }
        
        # Duty vs Load
        if 'Inj_Duty' in self.df.columns and 'load' in self.channels:
            duty = self.df['Inj_Duty']
            load = self.df[self.channels['load']]
            corr = duty.corr(load)
            
            self.correlations['duty_load'] = {
                'value': round(corr, 3),
                'interpretation': self._interpret_correlation(corr, 'duty', 'load')
            }
        
        return self.correlations
    
    def _interpret_correlation(self, corr, param1, param2):
        """Interpretează semnificația corelației"""
        abs_corr = abs(corr)
        
        if abs_corr > 0.8:
            strength = "corelație PUTERNICĂ"
        elif abs_corr > 0.5:
            strength = "corelație MODERATĂ"
        elif abs_corr > 0.3:
            strength = "corelație SLABĂ"
        else:
            strength = "corelație NEGLIJABILĂ"
        
        direction = "pozitivă" if corr > 0 else "negativă"
        
        return f"{strength} {direction} între {param1} și {param2}"

# ======================================================
# CORE: PREDICTIVE RISK ENGINE
# ======================================================
class PredictiveRiskEngine:
    """Evaluare risc predictiv pe baza pattern-urilor"""
    
    def __init__(self, results_dict):
        self.results = results_dict
        self.risk_score = 0
        self.risk_factors = []
        
    def assess(self):
        """Calculează risk score global"""
        
        # Factor risc: Knock
        if 'knock' in self.results:
            knock = self.results['knock']
            if knock.get('severity') == 'CRITICAL':
                self.risk_score += 40
                self.risk_factors.append({
                    'factor': 'DETONATION',
                    'impact': 'HIGH',
                    'consequence': 'Risc deteriorare piston, segmenți sau chiuloasă'
                })
            elif knock.get('severity') == 'WARNING':
                self.risk_score += 20
                self.risk_factors.append({
                    'factor': 'KNOCK_EVENTS',
                    'impact': 'MEDIUM',
                    'consequence': 'Uzură accelerată în timp'
                })
        
        # Factor risc: Lambda lean
        if 'lambda' in self.results:
            lamb = self.results['lambda']
            if lamb.get('status') == 'LEAN_DANGER':
                self.risk_score += 35
                self.risk_factors.append({
                    'factor': 'LEAN_MIXTURE',
                    'impact': 'HIGH',
                    'consequence': 'Risc topire piston, ardere supape evacuare'
                })
        
        # Factor risc: Oil overheat
        if 'oil' in self.results:
            oil = self.results['oil']
            if oil.get('severity') == 'CRITICAL':
                self.risk_score += 30
                self.risk_factors.append({
                    'factor': 'OIL_OVERHEAT',
                    'impact': 'HIGH',
                    'consequence': 'Pierdere viscozitate, risc gripare lagăre'
                })
            elif oil.get('sustained_high_min', 0) > 5:
                self.risk_score += 15
                self.risk_factors.append({
                    'factor': 'SUSTAINED_HIGH_OIL',
                    'impact': 'MEDIUM',
                    'consequence': 'Degradare accelerată a uleiului'
                })
        
        # Factor risc: Injector saturation
        if 'duty' in self.results:
            duty = self.results['duty']
            if duty.get('severity') == 'CRITICAL':
                self.risk_score += 25
                self.risk_factors.append({
                    'factor': 'INJECTOR_LIMIT',
                    'impact': 'MEDIUM',
                    'consequence': 'Risc amestec sărac la turații mari'
                })
        
        # Factor risc: EGT
        if 'egt' in self.results:
            egt = self.results['egt']
            if egt.get('severity') == 'CRITICAL':
                self.risk_score += 30
                self.risk_factors.append({
                    'factor': 'EGT_CRITICAL',
                    'impact': 'HIGH',
                    'consequence': 'Risc deteriorare turbină'
                })
        
        return {
            'risk_score': min(100, self.risk_score),
            'risk_level': self._get_risk_level(),
            'factors': self.risk_factors
        }
    
    def _get_risk_level(self):
        """Returnează nivelul de risc"""
        if self.risk_score >= 70:
            return 'CRITICAL'
        elif self.risk_score >= 40:
            return 'HIGH'
        elif self.risk_score >= 20:
            return 'MEDIUM'
        else:
            return 'LOW'

# ======================================================
# RENDERING FUNCTIONS
# ======================================================

def render_detection_report(report, detected, missing, noisy, confidence):
    """Renderează raportul de detectare canale"""
    st.markdown("<h2 class='section-title'>📡 Channel Detection & Signal Quality</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Channels", report['total_channels'])
    col2.metric("Detected", f"{report['detected']}/{len(ChannelDetectionEngine.CHANNEL_MAP)}")
    col3.metric("Coverage", f"{report['coverage']:.0f}%")
    col4.metric("Noisy Signals", len(noisy))
    
    # Detalii detectare
    st.markdown("""
    <div class="detection-box">
        <h4 style="margin-top:0;">🔍 Detection Details</h4>
    """, unsafe_allow_html=True)
    
    if detected:
        st.markdown("**✅ Detected Channels:**")
        for std_name, col_name in detected.items():
            conf = confidence.get(std_name, 0)
            conf_color = "#10b981" if conf > 80 else "#f59e0b" if conf > 50 else "#d90429"
            st.markdown(f"- **{std_name}** → `{col_name}` <span class='confidence-badge' style='background:{conf_color}20;color:{conf_color}'>CONFIDENCE: {conf:.0f}%</span>", unsafe_allow_html=True)
    
    if missing:
        st.markdown("**⚠️ Missing Channels:**")
        for m in missing[:10]:  # Primele 10
            st.markdown(f"- {m}")
        if len(missing) > 10:
            st.markdown(f"*... și încă {len(missing)-10} canale*")
    
    if noisy:
        st.markdown("**🔊 Noisy/Suspect Signals:**")
        for n in noisy:
            st.markdown(f"- {n} (flatline detection sau zgomot excesiv)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WHY explainer
    st.markdown("""
    <div class="why-box">
        <b>💡 WHY THIS MATTERS:</b><br>
        Channel detection este primul pas critic. Fără identificarea corectă a semnalelor, orice analiză ulterioară este inutilă. 
        Un semnal "noisy" poate indica cablaj defect, împământare proastă sau senzor în curs de defectare.
    </div>
    """, unsafe_allow_html=True)

def render_operating_modes(mode_summary, modes_df):
    """Renderează analiza regimurilor de funcționare"""
    st.markdown("<h2 class='section-title'>⚙️ Operating Mode Analysis</h2>", unsafe_allow_html=True)
    
    cols = st.columns(len(mode_summary))
    for i, (mode, data) in enumerate(mode_summary.items()):
        with cols[i]:
            st.metric(mode.replace('_', ' '), f"{data['percentage']}%", f"{data['count']} samples")
    
    # Grafic timeline
    fig = go.Figure()
    
    for mode in modes_df.columns:
        fig.add_trace(go.Scatter(
            y=modes_df[mode].astype(int),
            mode='lines',
            name=mode,
            line=dict(width=1),
            stackgroup='one'
        ))
    
    fig.update_layout(
        title="Operating Modes Timeline",
        xaxis_title="Sample Index",
        yaxis_title="Active Mode",
        template="plotly_white",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="why-box">
        <b>💡 WHY THIS MATTERS:</b><br>
        Problemele apar rar uniform. De exemplu, knock-ul poate apărea DOAR în WOT @ 4500 RPM, nu la Idle. 
        Separarea pe regimuri îți arată EXACT unde e problema, nu doar "că există".
    </div>
    """, unsafe_allow_html=True)

def render_fuel_analysis(fuel_results):
    """Renderează analiza fuel detaliată"""
    st.markdown("<h2 class='section-title'>⛽ Advanced Fuel System Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Lambda Analysis
    if 'lambda' in fuel_results and fuel_results['lambda']['status'] != 'NO_DATA':
        lamb = fuel_results['lambda']
        color = get_severity_color(lamb.get('severity', 'SAFE'))
        
        with col1:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{lamb['status']}</div>
                <div style="font-size:11px; color:#6c757d;">LAMBDA (AFR) WOT</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{lamb['mean_wot']:.3f}</div>
                <div style="font-size:13px; line-height:1.5;">
                    Min: {lamb['min_wot']:.3f} | StdDev: {lamb['std_wot']:.3f}<br>
                    <span class='confidence-badge' style='background:#e7f5ff;color:#1971c2;margin-top:8px;'>
                        CONFIDENCE: {lamb['confidence']}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if lamb['status'] == 'LEAN_DANGER':
                render_resolution(
                    "LEAN MIXTURE - CRITICAL ACTION REQUIRED",
                    "CRITICAL",
                    f"Lambda WOT medie este {lamb['mean_wot']:.3f}, peste limita de 0.86. Acest lucru înseamnă că gazele de evacuare sunt EXTREM de fierbinți, putând cauza:\n- Topirea pistonului\n- Arderea supapelor de evacuare\n- Deteriorarea turbinei\n- Crăparea chiuloasei",
                    "ACȚIUNE IMEDIATĂ: Crește Fuel Target Map cu 8-12% în zona WOT sau verifică:\n1. Presiunea în rampa de benzină (min 3.5 bar)\n2. Filtru combustibil înfundat\n3. Pompă slabă\n4. Injectoare murdare\n\nTarget optim: 0.80-0.82 lambda pentru protecție termică maximă."
                )
    
    # Duty Analysis
    if 'duty' in fuel_results and fuel_results['duty']['status'] != 'NO_DATA':
        duty = fuel_results['duty']
        color = get_severity_color(duty.get('severity', 'SAFE'))
        
        with col2:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{duty['status']}</div>
                <div style="font-size:11px; color:#6c757d;">INJECTOR DUTY CYCLE</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{duty['max_duty']:.1f}%</div>
                <div style="font-size:13px; line-height:1.5;">
                    Linearity: {duty['linearity']:.2f}<br>
                    <span class='confidence-badge' style='background:#e7f5ff;color:#1971c2;margin-top:8px;'>
                        CONFIDENCE: {duty['confidence']}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if duty['status'] in ['SATURATED', 'NEAR_LIMIT']:
                render_resolution(
                    "INJECTOR CAPACITY LIMIT REACHED",
                    duty['severity'],
                    f"Duty cycle a atins {duty['max_duty']:.1f}%. Peste 85%, injectoarele nu mai pot menține presiunea necesară, rezultând amestec sărac forțat la turații mari.",
                    "SOLUȚII:\n1. UPGRADE injectoare (ex: de la 440cc la 550cc+)\n2. Crește presiunea în rampă (+0.5 bar)\n3. Verifică regulator presiune\n4. LIMITEAZĂ boost-ul până la upgrade\n\nDacă linearity < 0.70, injectoarele sunt subdimensionate sau presiunea e inconsistentă."
                )
    
    # Fuel Trim
    if 'fuel_trim' in fuel_results and fuel_results['fuel_trim']['status'] != 'NO_DATA':
        trim = fuel_results['fuel_trim']
        
        st.markdown(f"""
        <div class="resolution-box">
            <div class="res-title" style="color:{get_severity_color(trim['severity'])};">
                FUEL TRIM ADAPTATION // {trim['status']}
            </div>
            <div class="res-body">
                <b>SHORT TERM:</b> Mean = {trim['stft_mean']:.2f}% | StdDev = {trim['stft_std']:.2f}%<br>
                {'⚠️ ECU-ul compensează activ diferențe în fueling. Verifică vacuum leaks sau senzor O2.' if abs(trim['stft_mean']) > 10 else '✅ Adaptare minimă, sistemul e calibrat corect.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Linearity Issue
    if 'linearity' in fuel_results:
        lin = fuel_results['linearity']
        st.markdown(f"""
        <div class="anomaly-alert">
            <b>⚠️ NON-LINEAR FUEL DELIVERY DETECTED</b><br>
            Correlation Duty ↔ Lambda: {lin['correlation']:.2f}<br>
            {lin['explanation']}
        </div>
        """, unsafe_allow_html=True)

def render_ignition_analysis(ign_results):
    """Renderează analiza ignition detaliată"""
    st.markdown("<h2 class='section-title'>⚡ Advanced Ignition System Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Knock Analysis
    if 'knock' in ign_results and ign_results['knock']['status'] != 'NO_DATA':
        knock = ign_results['knock']
        color = get_severity_color(knock.get('severity', 'SAFE'))
        
        with col1:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{knock['status']}</div>
                <div style="font-size:11px; color:#6c757d;">KNOCK / DETONATION</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{knock['max_knock']:.2f}V</div>
                <div style="font-size:13px; line-height:1.5;">
                    Mean: {knock['mean_knock']:.2f}V | Events: {knock['events']}<br>
                    Event %: {knock['event_pct']:.1f}% | Bursts: {knock['bursts']}<br>
                    <span class='confidence-badge' style='background:#e7f5ff;color:#1971c2;margin-top:8px;'>
                        CONFIDENCE: {knock['confidence']}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if knock['status'] in ['SEVERE_DETONATION', 'SUSTAINED_KNOCK']:
                render_resolution(
                    "DETONATION DETECTED - IMMEDIATE ACTION",
                    "CRITICAL",
                    f"Peak knock: {knock['max_knock']:.2f}V (Limită: 1.2V). {knock['events']} evenimente detectate ({knock['event_pct']:.1f}% din log).\n\nDetonația înseamnă că amestecul se aprinde ÎNAINTE de scânteie din cauza:\n- Avans prea mare\n- Temperatura prea mare în cameră\n- Cifră octanică insuficientă\n- Puncte fierbinți (carbon deposits)",
                    "ACȚIUNE IMEDIATĂ:\n1. RETARD ignition cu 3-4 grade în zona Load/RPM unde apare\n2. Verifică bujiile (heat range prea cald?)\n3. Testează cu combustibil mai bun (98+ RON)\n4. Verifică temperatura IAT (dacă > 50°C, intercooler insuficient)\n5. Dacă persistă: cleaning injectoare + decarbonizare\n\nNU ignora knock-ul - poate distruge motorul în secunde."
                )
            elif knock['status'] == 'SPORADIC_KNOCK':
                st.markdown("""
                <div class="resolution-box">
                    <div class="res-title" style="color:#f59e0b;">SPORADIC KNOCK EVENTS // WARNING</div>
                    <div class="res-body">
                        <b>OBSERVAȚIE:</b> Knock sporadic (sub 5% din timp) poate fi normal sau cauzat de zgomot extern.<br><br>
                        <b>RECOMANDARE:</b> Monitorizează în continuare. Dacă crește frecvența, aplică retard preventiv de 1-2 grade.
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Timing Stability
    if 'timing_stability' in ign_results:
        timing = ign_results['timing_stability']
        color = get_severity_color(timing['severity'])
        
        with col2:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{timing['status']}</div>
                <div style="font-size:11px; color:#6c757d;">TIMING STABILITY</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{timing['std']:.1f}°</div>
                <div style="font-size:13px; line-height:1.5;">
                    Standard Deviation WOT<br>
                    <span class='confidence-badge' style='background:#e7f5ff;color:#1971c2;margin-top:8px;'>
                        CONFIDENCE: {timing['confidence']}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Knock Cause Analysis
    if 'knock_cause' in ign_results:
        cause = ign_results['knock_cause']
        st.markdown(f"""
        <div class="why-box">
            <b>🔍 KNOCK ROOT CAUSE ANALYSIS:</b><br>
            Type: <b>{cause['type']}</b><br>
            {cause['explanation']}
        </div>
        """, unsafe_allow_html=True)

def render_thermal_analysis(thermal_results):
    """Renderează analiza termică"""
    st.markdown("<h2 class='section-title'>🌡️ Thermal & Mechanical Stress Analysis</h2>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    # Oil
    if 'oil' in thermal_results and thermal_results['oil']['status'] != 'NO_DATA':
        oil = thermal_results['oil']
        color = get_severity_color(oil['severity'])
        
        with cols[0]:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{oil['status']}</div>
                <div style="font-size:11px; color:#6c757d;">OIL TEMPERATURE</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{oil['max']:.0f}°C</div>
                <div style="font-size:13px; line-height:1.5;">
                    Sustained High: {oil['sustained_high_min']:.1f} min
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if oil['severity'] != 'SAFE':
                st.markdown(f"""
                <div class="resolution-box">
                    <div class="res-title" style="color:{color};">OIL THERMAL STRESS</div>
                    <div class="res-body">
                        Peste 115°C, uleiul își pierde viscozitatea și capacitatea de lubrifiere. 
                        {oil['sustained_high_min']:.1f} minute la temperatură mare accelerează degradarea.<br><br>
                        <b>SOLUȚIE:</b> Oil cooler, ventilație îmbunătățită sau verifică termostat blocat.
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Coolant
    if 'coolant' in thermal_results:
        coolant = thermal_results['coolant']
        color = get_severity_color(coolant['severity'])
        
        with cols[1]:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{coolant['status']}</div>
                <div style="font-size:11px; color:#6c757d;">COOLANT TEMPERATURE</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{coolant['max']:.0f}°C</div>
            </div>
            """, unsafe_allow_html=True)
    
    # EGT
    if 'egt' in thermal_results:
        egt = thermal_results['egt']
        color = get_severity_color(egt['severity'])
        
        with cols[2]:
            st.markdown(f"""
            <div class="expert-card" style="border-top: 5px solid {color};">
                <div style="color:{color}; font-weight:900; font-size:13px; font-family:Orbitron;">{egt['status']}</div>
                <div style="font-size:11px; color:#6c757d;">EXHAUST GAS TEMP</div>
                <div style="font-size:38px; font-weight:700; margin:12px 0;">{egt['max']:.0f}°C</div>
            </div>
            """, unsafe_allow_html=True)
            
            if egt['severity'] == 'CRITICAL':
                st.markdown("""
                <div class="anomaly-alert">
                    <b>⚠️ EGT CRITICAL - TURBO AT RISK</b><br>
                    EGT peste 950°C poate deteriora paletele turbinei. Cauze: amestec prea sărac, boost excesiv, timing prea avansat.
                </div>
                """, unsafe_allow_html=True)
    
    # Thermal Shock
    if 'thermal_shock' in thermal_results:
        shock = thermal_results['thermal_shock']
        st.markdown(f"""
        <div class="anomaly-alert">
            <b>⚠️ RAPID THERMAL CHANGE</b><br>
            Max rate: {shock['max_rate']:.2f}°C/sec<br>
            {shock['explanation']}
        </div>
        """, unsafe_allow_html=True)

def render_predictive_risk(risk_data):
    """Renderează analiza de risc predictivă"""
    st.markdown("<h2 class='section-title'>🎯 Predictive Risk Assessment</h2>", unsafe_allow_html=True)
    
    risk_score = risk_data['risk_score']
    risk_level = risk_data['risk_level']
    
    # Risk gauge
    if risk_level == 'CRITICAL':
        color = "#d90429"
    elif risk_level == 'HIGH':
        color = "#f59e0b"
    elif risk_level == 'MEDIUM':
        color = "#ffc107"
    else:
        color = "#10b981"
    
   # ======================================================
# DATA DICTIONARY (UNCHANGED)
# ======================================================
SENSOR_DESCRIPTIONS = {
    "Motor RPM": "Viteza de rotație a arborelui cotit. Esențială pentru axa X în hărțile de tuning.",
    "Engine load": "Sarcina motorului. Indică volumul de aer raportat la capacitatea cilindrică.",
    "Air mass": "Cantitatea de aer absorbită. Determinantă pentru calculul amestecului (MAF).",
    "Ignition angle": "Momentul scânteii. Valorile prea mici indică retard cauzat de detonație.",
    "Injection time": "Durata deschiderii injectoarelor (ms). Peste 20ms indică saturație.",
    "Knock sensor #1": "Senzor piezo care detectează vibrații de detonație în bloc.",
    "Motor temp.": "Temperatura antigelului. Optim: 85-95°C.",
    "Oil temp.": "Temperatura uleiului. Peste 115°C necesită răcire suplimentară.",
    "Battery voltage": "Tensiunea sistemului. Trebuie să fie stabilă (>13.5V în mers)."
}

# ======================================================
# UTILS & DATA ENGINE (UNCHANGED)
# ======================================================
def safe_col(df, name):
    if name not in df.columns:
        df[name] = np.nan
    return df[name]

def compute_channels(df: pd.DataFrame) -> pd.DataFrame:
    rpm = safe_col(df, 'Motor RPM').replace(0, np.nan)
    df['Inj_Duty'] = (safe_col(df, 'Injection time') * rpm) / 1200
    df['Lambda_Avg'] = (safe_col(df, 'Lambda #1 integrator ') + safe_col(df, 'Lambda #2 integrator')) / 2
    df['VE_Calculated'] = (safe_col(df, 'Air mass') * 100) / (rpm * 0.16 + 1)
    df['Knock_Peak'] = df[['Knock sensor #1', 'Knock sensor #2']].max(axis=1)
    df['WOT'] = (safe_col(df, 'Engine load') > 70) & (rpm > 3000)
    return df

def get_diagnostics(df):
    wot = df[df['WOT']]
    reports = []
    duty_max = df['Inj_Duty'].max()
    lambda_wot = wot['Lambda_Avg'].mean() if not wot.empty else 0

    if duty_max > 90:
        reports.append(("FUEL SYSTEM", "HARD LIMIT", f"Duty Cycle at {duty_max:.1f}%", "Injector capacity exceeded. Hardware upgrade required."))
    elif lambda_wot > 0.88:
        reports.append(("FUEL SYSTEM", "CRITICAL", f"WOT Lambda {lambda_wot:.2f}", "Lean mixture under load. Enrich fueling maps immediately."))
    else:
        reports.append(("FUEL SYSTEM", "OK", "Fuel delivery within optimal parameters.", "No correction required."))

    k_peak = df['Knock_Peak'].max()
    if k_peak > 2.2:
        reports.append(("IGNITION SYSTEM", "CRITICAL", f"Knock Peak {k_peak:.2f} V", "Active detonation. Reduce ignition advance by 2–4 degrees."))
    else:
        reports.append(("IGNITION SYSTEM", "OK", "No dangerous knock detected.", "Ignition strategy is stable."))

    oil = df['Oil temp.'].max()
    if oil > 112:
        reports.append(("THERMAL MANAGEMENT", "WARNING", f"Oil temperature {oil:.1f} °C", "Cooling efficiency insufficient during sustained load."))
    else:
        reports.append(("THERMAL MANAGEMENT", "OK", "Thermal behavior within safe limits.", "Cooling system operating nominally."))
    return reports

# ======================================================
# APP
# ======================================================
def app():
    st.markdown("""
    <div class="header-box">
        <h1>LZTUNED ARCHITECT</h1>
        <p>Motorsport ECU Diagnostic Platform // v20.0</p>
        <div style="font-size: 10px; opacity: 0.5; margin-top: 15px; letter-spacing: 2px;">
            ENGINEERED BY LUIS ZAVOIANU // APPLICATION ENGINEER
        </div>
    </div>
    """, unsafe_allow_html=True)

    # File Uploader Stilizat implicit
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        file = st.file_uploader("📂 DRAG & DROP ECU LOG (.CSV)", type="csv")
    
    if not file:
        st.markdown("<div style='text-align:center; padding:50px; color:#4da3ff; font-family:Orbitron;'>SYSTEM IDLE - WAITING FOR DATA INPUT...</div>", unsafe_allow_html=True)
        return

    df_raw = pd.read_csv(file, sep=';')
    df = compute_channels(df_raw)
    all_cols = df.columns.tolist()

    # KPI DASHBOARD
    st.markdown("<h2 class='section-title'>Engine Performance Telemetry</h2>", unsafe_allow_html=True)
    k = st.columns(4)
    k[0].metric("MAX RPM", f"{int(df['Motor RPM'].max())}")
    k[1].metric("AIR MASS", f"{df['Air mass'].max():.1f}")
    k[2].metric("INJ DUTY", f"{df['Inj_Duty'].max():.1f}%")
    k[3].metric("IGNITION", f"{df['Ignition angle'].min():.1f}°")

    # VERDICT & CRITICAL ALERTS
    st.markdown("<h2 class='section-title'>System Verdict & Safety Status</h2>", unsafe_allow_html=True)
    
    diagnostics = get_diagnostics(df)
    for title, level, obs, action in diagnostics:
        if level in ["CRITICAL", "HARD LIMIT"]:
            alert_class, icon = "alert-critical", "❌"
        elif level == "WARNING":
            alert_class, icon = "alert-warning", "⚠️"
        else:
            alert_class, icon = "alert-ok", "✅"

        st.markdown(f"""
        <div class="alert-container {alert_class}">
            <div class="alert-header">{icon} {title} // {level}</div>
            <div class="alert-body"><b>TELEMETRY OBS:</b> {obs}</div>
            <div class="alert-action">REQUIRED: {action}</div>
        </div>
        """, unsafe_allow_html=True)

    # SENSOR FORENSICS
    st.markdown("<h2 class='section-title'>Sensor Forensics Analysis</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["[ COMB ]", "[ FLOW ]", "[ TEMP ]", "[ ELEC ]"])

    group_map = {
        0: ['Motor RPM', 'Ignition angle', 'Knock sensor #1', 'Knock sensor #2', 'Lambda_Avg', 'Injection time'],
        1: ['Air mass', 'Engine load', 'Throttle position', 'VE_Calculated'],
        2: ['Motor temp.', 'Oil temp.', 'Intake temp.'],
        3: ['Battery voltage', 'Electric fan speed', 'Gear']
    }

    for tab, keys in zip(tabs, group_map.values()):
        with tab:
            st.write(" ")
            for c in keys:
                if c in df.columns:
                    with st.expander(f"SCAN CHANNEL: {c.upper()}"):
                        c1, c2 = st.columns([1, 2.5])
                        with c1:
                            st.markdown(f"<div class='sensor-card'><b>CHANNEL INFO:</b><br>{SENSOR_DESCRIPTIONS.get(c, 'Standard telemetry input.')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='margin-top:20px; font-size:12px;'><b>PEAK RANGE:</b><br>{df[c].min()} — {df[c].max()}</div>", unsafe_allow_html=True)
                        with c2:
                            fig = px.line(df, x='time', y=c, template="plotly_dark", color_discrete_sequence=['#4da3ff'])
                            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=10), 
                                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                              xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#263041'))
                            st.plotly_chart(fig, use_container_width=True)

    # ADVANCED TELEMETRY
    st.markdown("<h2 class='section-title'>Advanced Overlay & Correlation</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["[ OVERLAY ]", "[ MATRIX ]"])

    with t1:
        selected = st.multiselect("Select Channels:", all_cols, default=['Motor RPM', 'Ignition angle', 'Knock_Peak'])
        if selected:
            fig = make_subplots(rows=len(selected), cols=1, shared_xaxes=True, vertical_spacing=0.02)
            for i, s in enumerate(selected):
                fig.add_trace(go.Scatter(x=df['time'], y=df[s], name=s, line=dict(color='#4da3ff', width=1.5)), row=i+1, col=1)
            fig.update_layout(height=180*len(selected), template="plotly_dark", showlegend=True,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        corr = df.select_dtypes(include=[np.number]).corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
        fig_corr.update_layout(height=600, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_corr, use_container_width=True)

    # DATA TABLE
    st.markdown("<h2 class='section-title'>Full Telemetry Archive</h2>", unsafe_allow_html=True)
    with st.expander("ACCESS RAW DATASET"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    app()




