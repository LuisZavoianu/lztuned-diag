LZTuned Architect Pro: Enterprise ECU Diagnostic Suite
LZTuned Architect Pro este o platformă avansată de analiză și diagnosticare a telemetriei motorului, dezvoltată special pentru inginerii de calibrare (tuneri) și echipele de motorsport. Softul transformă logurile brute din ECU în informații acționabile, identificând automat riscurile mecanice și oportunitățile de optimizare a performanței.

Funcționalități Principale
1. Diagnosticare Expert (AI-Driven Oracle)
Analiză Detonație (Knock): Monitorizează senzorii piezo și avertizează vizual în caz de spike-uri de tensiune periculoase.

Safety Lambda: Calculează deviația între bănci (Bank 1 vs Bank 2) și verifică amestecul în sarcină maximă (WOT).

Protecție Hardware: Monitorizează Injector Duty Cycle (IDC) pentru a preveni saturația injectoarelor.

2. Laborator de Inginerie Avansată
Eficiență Volumetrică (VE): Calculează gradul de umplere a cilindrilor pe baza MAF/MAP și a temperaturii aerului.

Heat Soak Recovery: Analizează eficiența intercooler-ului și timpul de recuperare a temperaturii în admisie (IAT).

Clutch Slip Detection: Identifică patinarea ambreiajului prin corelarea matematică între RPM și VSS.

3. Analiză Pull-uri (WOT Analysis)
Izolează automat reprizele de accelerație completă din loguri lungi.

Calculează puterea estimativă la roată (Est. HP) bazată pe masa vehiculului și accelerația longitudinală.

4. Driver DNA & Forensics
Aggression Index: Analizează modul în care pilotul aplică pedala de accelerație (smoothness vs aggression).

Ignition Jitter: Detectează instabilitatea scânteii cauzată de senzori defecti sau interferențe electrice.

🛠️ Tehnologii Utilizate
Python 3.9+

Streamlit: Interfață UI de tip Command Center.

Pandas & NumPy: Procesare matematică de mare viteză.

Plotly: Grafice interactive și overlay-uri de telemetrie.

FPDF2: Generare automată de rapoarte tehnice PDF.

🌐 Unde poate fi rulat?
Aplicația este extrem de versatilă și poate fi accesată în trei moduri:

1. Cloud (Streamlit Community Cloud)
Cea mai rapidă metodă, accesibilă de pe orice dispozitiv (Laptop, Tabletă, Telefon) direct în browser: 👉 lztuned-pro.streamlit.app

2. Local (Development Mode)
Dacă dorești să rulezi softul offline pe laptopul tău de diagnoză:

Clonează repository-ul: git clone https://github.com/username/lztuned-pro.git

Instalează dependențele: pip install -r requirements.txt

Rulează aplicația: streamlit run lztuned_enterprise.py

3. Docker (Enterprise Deployment)
Poate fi containerizat pentru a fi rulat pe servere private sau infrastructuri cloud dedicate pentru echipe mari.

📄 Raportare Enterprise
La finalul fiecărei sesiuni de analiză, softul poate genera un Raport PDF Oficial care include:

Sumarul valorilor de vârf (Peak Values).

Verdictul de siguranță pentru combustibil și aprindere.

Recomandări tehnice pentru ajustarea hărților de avans sau injecție.

Developed by Luis Zavoianu // LZTuned Motorsport Engineering „Data-driven performance for the modern tuner.”

LZTuned Architect Pro: Enterprise ECU Diagnostic Suite
LZTuned Architect Pro is an advanced engine telemetry analysis and diagnostic platform engineered for calibration engineers (tuners) and motorsport teams. The software transforms raw ECU data logs into actionable insights, automatically identifying mechanical risks and performance optimization opportunities.

Live Demo: lztuned-pro.streamlit.app

 Key Features
1. Expert Diagnostics (AI-Driven Oracle)
Knock Analysis: Monitors piezo sensors and provides visual alerts for dangerous voltage spikes and detonation.

Safety Lambda: Calculates Bank-to-Bank deviation (Bank 1 vs. Bank 2) and verifies Air-Fuel Ratio (AFR) stability under Wide Open Throttle (WOT).

Hardware Protection: Tracks Injector Duty Cycle (IDC) to prevent injector saturation and lean-out conditions.

2. Advanced Engineering Lab
Volumetric Efficiency (VE): Calculates cylinder filling percentage based on MAF/MAP, RPM, and Intake Air Temperature.

Heat Soak Recovery: Analyzes intercooler efficiency and the recovery rate of Intake Air Temperature (IAT) after high-load events.

Clutch Slip Detection: Identifies clutch or torque converter slippage through mathematical correlation between Engine RPM and Vehicle Speed (VSS).

3. Pull Analysis (WOT Profiling)
Automatic Pull Isolation: Intelligently extracts full-throttle acceleration runs from long data logs.

Estimated Horsepower: Calculates estimated wheel horsepower (Est. HP) based on vehicle mass and longitudinal acceleration deltas.

4. Driver DNA & Forensics
Aggression Index: Evaluates throttle application "smoothness" vs. "aggression" to help coaching drivers.

Ignition Jitter: Detects ignition timing instability caused by faulty sensors or electrical interference.

🛠️ Tech Stack
Python 3.9+

Streamlit: For the "Command Center" style User Interface.

Pandas & NumPy: For high-speed mathematical data processing.

Plotly: Interactive multi-overlay telemetry charts.

FPDF2: Automated generation of technical PDF diagnostic reports.

🌐 Deployment & Usage
The application is versatile and can be deployed in three ways:

1. Cloud (Streamlit Community Cloud)
The fastest method, accessible from any device (Laptop, Tablet, Phone) directly in your browser: 👉 lztuned-pro.streamlit.app

2. Local Installation (Development Mode)
To run the software offline on your tuning laptop:

Clone the repository:

Bash

git clone https://github.com/yourusername/lztuned-pro.git
Install dependencies:

Bash

pip install -r requirements.txt
Launch the app:

Bash

streamlit run lztuned_enterprise.py
3. Docker (Enterprise)
Can be containerized for private servers or dedicated cloud infrastructure for large racing teams.

📄 Enterprise Reporting
At the end of each session, the software generates an Official PDF Diagnostic Report including:

Peak Value Summary (RPM, Boost, IAT, Knock).

Safety Verdicts for Fueling and Ignition strategies.

Technical recommendations for map adjustments (Timing/Fueling).

⚖️ Disclaimer
This software is intended for off-road/motorsport use only. Tuning an engine based on data analysis carries inherent risks. LZTuned is not responsible for any mechanical failures resulting from the use of this tool.

Developed by Luis Zavoianu // LZTuned Motorsport Engineering "Data-driven performance for the modern tuner."
