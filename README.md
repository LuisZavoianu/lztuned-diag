
<img width="643" height="109" alt="image" src="https://github.com/user-attachments/assets/b43f767a-ad7e-44b5-8d13-9e949a80adcf" />

LZTuned Architect Pro: Enterprise ECU Diagnostic Suite
LZTuned Architect Pro is an advanced engine telemetry analysis and diagnostic platform engineered for calibration engineers (tuners) and motorsport teams. The software transforms raw ECU data logs into actionable insights, automatically identifying mechanical risks and performance optimization opportunities.

Live Demo: lztuned-pro.streamlit.app

 Key Features
1. Expert Diagnostics (AI-Driven Oracle)
Knock Analysis: Monitors piezo sensors and provides visual alerts for dangerous voltage spikes and detonation.
<img width="1352" height="188" alt="image" src="https://github.com/user-attachments/assets/fa267a3b-ffe3-4fec-91b3-4190da3697d9" />
<img width="1403" height="249" alt="image" src="https://github.com/user-attachments/assets/354c38fc-ebbd-47f9-ad93-584f93c2a614" />

Safety Lambda: Calculates Bank-to-Bank deviation (Bank 1 vs. Bank 2) and verifies Air-Fuel Ratio (AFR) stability under Wide Open Throttle (WOT).

Hardware Protection: Tracks Injector Duty Cycle (IDC) to prevent injector saturation and lean-out conditions.
<img width="1512" height="247" alt="image" src="https://github.com/user-attachments/assets/ef05e190-4bbb-474a-8040-acecd75f63b9" />

2. Advanced Engineering Lab
Volumetric Efficiency (VE): Calculates cylinder filling percentage based on MAF/MAP, RPM, and Intake Air Temperature.
<img width="418" height="242" alt="image" src="https://github.com/user-attachments/assets/8c26afcd-37ee-4a85-a66e-4e4f3987c160" />

Heat Soak Recovery: Analyzes intercooler efficiency and the recovery rate of Intake Air Temperature (IAT) after high-load events.
<img width="1397" height="191" alt="image" src="https://github.com/user-attachments/assets/dc102f1e-25f0-4559-a575-c24e28f68c3b" />

Clutch Slip Detection: Identifies clutch or torque converter slippage through mathematical correlation between Engine RPM and Vehicle Speed (VSS).

3. Pull Analysis (WOT Profiling)
Automatic Pull Isolation: Intelligently extracts full-throttle acceleration runs from long data logs.

Estimated Horsepower: Calculates estimated wheel horsepower (Est. HP) based on vehicle mass and longitudinal acceleration deltas.

4. Driver DNA & Forensics
Aggression Index: Evaluates throttle application "smoothness" vs. "aggression" to help coaching drivers.

Ignition Jitter: Detects ignition timing instability caused by faulty sensors or electrical interference.

Tech Stack
Python 3.9+

Streamlit: For the "Command Center" style User Interface.

Pandas & NumPy: For high-speed mathematical data processing.

Plotly: Interactive multi-overlay telemetry charts.

FPDF2: Automated generation of technical PDF diagnostic reports.

Deployment & Usage
The application is versatile and can be deployed in three ways:

1. Cloud (Streamlit Community Cloud)
The fastest method, accessible from any device (Laptop, Tablet, Phone) directly in your browser: 👉 lztuned-pro.streamlit.app

2. Local Installation (Development Mode)
To run the software offline on your tuning laptop:

Clone the repository:

Bash

git clone https://github.com/luiszavoianu/lztuned-pro.git
Install dependencies:

Bash

pip install -r requirements.txt
Launch the app:

Bash

streamlit run lztuned_enterprise.py
3. Docker (Enterprise)
Can be containerized for private servers or dedicated cloud infrastructure for large racing teams.

Enterprise Reporting
At the end of each session, the software generates an Official PDF Diagnostic Report including:

Peak Value Summary (RPM, Boost, IAT, Knock).

Safety Verdicts for Fueling and Ignition strategies.

Technical recommendations for map adjustments (Timing/Fueling).

Disclaimer
This software is intended for off-road/motorsport use only. Tuning an engine based on data analysis carries inherent risks. LZTuned is not responsible for any mechanical failures resulting from the use of this tool.

Developed by Luis Zavoianu // LZTuned Motorsport Engineering "Data-driven performance for the modern tuner."
