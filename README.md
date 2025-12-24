# <p align="center">LZTuned Architect Pro</p>
<p align="center"><strong>Advanced ECU Interpretation Engine // Production v1.0</strong></p>
<p align="center"> <img width="643" alt="LZTuned Banner" src="https://github.com/user-attachments/assets/b43f767a-ad7e-44b5-8d13-9e949a80adcf" /> </p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-GPLv3-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" />
</p>

---

### 📑 Overview
**LZTuned Architect Pro** is a professional-grade ECU log interpretation engine designed for motorsport teams, professional tuners, and advanced automotive enthusiasts. 

The software transforms raw telemetry data into high-level diagnostic intelligence, identifying mechanical risks before they lead to engine failure.

* ✅ **Universal Support:** Petrol, E85, Diesel, Naturally Aspirated (NA), Turbo, and Twin-Turbo configurations.
* ✅ **Compatibility:** Processes CSV logs from OEM and Standalone ECUs (Ecumaster, MaxxECU, Link, Haltech, Bosch, etc.).

🔗 **Live Demo:** [lztuned-pro.streamlit.app](https://lztuned-pro.streamlit.app/)

---

### 🚀 Core Engine Features

#### 1️⃣ Intelligent Channel Detection
The system automatically identifies vital engine parameters using fuzzy matching and evaluates signal health:
* **Confidence Scoring:** Validates channel mapping accuracy (e.g., RPM, Load, Lambda, Knock).
* **Signal Quality Audit:** Detects "Noisy" or suspect signals (flatlines, noise) indicating faulty wiring or sensor degradation.

#### 2️⃣ Automated Operating Mode Analysis
The engine segments data into operational states to isolate transient issues:
* **WOT (Wide Open Throttle):** High-load performance and safety analysis.
* **Acceleration / Cruise / Idle:** Stability and fuel trim evaluation.
* **Heat Soak Detection:** Monitors thermal stress during stationary periods.

#### 3️⃣ Fuel System Forensics
Advanced algorithms to protect your engine's internals:
* **Lean Mixture Alerts:** Real-time identification of dangerous AFR levels during WOT.
* **Injector Duty Cycle (IDC) Limits:** Monitors for saturation (85-95%+).
* **Non-Linear Delivery Analysis:** Correlates Duty Cycle vs Lambda to detect fuel pressure drops.

#### 4️⃣ Ignition & Detonation (Knock) Lab
Surgical precision in detecting combustion instability:
* **Knock Root Cause Analysis:** Determines if detonation is triggered by ignition lead, thermal load, or lean fueling.
* **Burst Tracking:** Monitors knock frequency per RPM range.

---

### 📊 Analytics & Predictive Risk

| Feature | Description |
| :--- | :--- |
| **KPI Dashboard** | Real-time tracking of Peak RPM, Peak Knock, Max IDC, and Min Lambda. |
| **Predictive Risk Assessment** | Aggregated risk score (0-100) based on all detected stressors. |
| **Anomaly Detection** | Identifies Load spikes, Lambda deviations, and sudden RPM drops. |
| **Correlation Maps** | Statistical analysis of parameter relationships (e.g., RPM ↔ Knock). |

---

### 🌐 Deployment & Usage

#### ☁️ Cloud Access (SaaS)
Run the analysis instantly on any device via browser:  
👉 [**Open LZTuned Pro Web App**](https://lztuned-pro.streamlit.app/)

#### 💻 Local Installation
For offline use on diagnostic laptops:
```bash
# Clone the repository
git clone [https://github.com/luiszavoianu/lztuned-pro.git](https://github.com/luiszavoianu/lztuned-pro.git)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run lztuned_enterprise.py
