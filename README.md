# ⚙️ Digital Twin Prescriptive Maintenance Platform

> **Real-time telemetry + predictive analytics** to eliminate unplanned downtime before it happens.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D9970?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen?style=flat-square)]()

---

## 📌 Overview

This platform implements a **Digital Twin** for heavy vehicle tire systems — a live virtual replica of a physical asset, continuously updated with real-time sensor telemetry. Instead of reacting to failures, it prescribes intervention *before* failure occurs.

```
Sensor Data (PSI / °C / km)  →  Risk Engine  →  Prescriptive Action  →  Cost Avoidance
```

**Core Problem Solved:**  
Unplanned asset failures cost $1,200–$5,000+ per event in downtime, emergency labour, and secondary damage. This platform converts reactive maintenance into a **proactive, data-driven workflow**.

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND (UI Layer)                 │
│   ┌───────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│   │  3D Model     │  │  Telemetry Gauges│  │  Prescriptive   │ │
│   │  Viewer       │  │  (PSI/°C/km)     │  │  Analytics      │ │
│   │  (model-viewer│  │                  │  │  + Metrics      │ │
│   │   Web Comp.)  │  │                  │  │                 │ │
│   └───────────────┘  └──────────────────┘  └─────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                       BUSINESS LOGIC LAYER                       │
│                                                                  │
│   predict_wear_and_status()      calculate_business_metrics()   │
│   ┌──────────────────────────┐   ┌──────────────────────────┐  │
│   │ Multi-factor Risk Engine │   │ ROI / Cost Avoidance     │  │
│   │  · Pressure analysis     │   │  · Fuel efficiency Δ     │  │
│   │  · Temperature analysis  │   │  · Uptime projection     │  │
│   │  · Mileage wear model    │   │  · Maintenance savings   │  │
│   └──────────────────────────┘   └──────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                       DATA / SIMULATION LAYER                    │
│                                                                  │
│   generate_simulation_data()  →  Pandas DataFrame               │
│   · Realistic pressure decay curve (0.08–0.25 PSI/interval)     │
│   · Temperature co-variance with pressure and mileage           │
│   · Stochastic mileage accumulation (250–600 km/interval)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Risk Engine — How It Works

The core of the platform is a **multi-factor weighted risk scorer** (`predict_wear_and_status`).

| Factor | Threshold | Risk Points Added |
|---|---|---|
| Pressure | < 28 PSI (critical under-inflation) | +3 |
| Pressure | > 38 PSI (blowout risk) | +3 |
| Pressure | < 29 PSI or > 36 PSI (early warning) | +2 |
| Temperature | > 85°C (rubber degradation) | +3 |
| Temperature | > 75°C (warning) | +2 |
| Mileage | > 40,000 km (end of service life) | +2 |
| Mileage | > 35,000 km (warning) | +1 |

**Status thresholds:**

```python
risk_score >= 6  →  🛑 CRITICAL: IMMINENT FAILURE RISK
risk_score >= 4  →  ⚠️  HIGH RISK: MAINTENANCE REQUIRED
risk_score >= 2  →  🔶 WARNING: ELEVATED RISK
risk_score  < 2  →  ✅ NORMAL OPERATING STATE
```

---

## 📊 Business Metrics Engine

The `calculate_business_metrics()` function translates sensor data into financial impact.

**Fuel Efficiency Model:**
- Under-inflation: `−0.5% per PSI below 30` (rolling resistance increases)
- Slight over-inflation (≤ 3 PSI above 35): `+0.7% per PSI` (reduced deformation)
- Extreme over-inflation: `−1.5% per PSI above threshold` (contact patch deformation)
- High temperature: `−0.2% per °C above 70°C`

**Cost Avoidance by Status:**

| Status | Cost Avoided | Uptime | Risk Score |
|---|---|---|---|
| 🟢 Normal | $1,800 | 98.2% | 15–25 |
| 🟡 Warning | $2,400 | 96.5% | 35–50 |
| 🟠 High Risk | $3,600 | 94.0% | 60–75 |
| 🔴 Critical | $4,800 | 89.0% | 85–98 |

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.9+
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Areebrizz/Digital-Twin-Project.git
cd Digital-Twin-Project

# Install dependencies
pip install streamlit pandas numpy plotly

# Run the app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 🖥️ Dashboard Walkthrough

```
┌──────────────────────────────────────────────────────┐
│  DIGITAL TWIN VISUALIZATION   │  REAL-TIME TELEMETRY │
│  · 3D rotating vehicle model  │  · Pressure gauge    │
│  · Status glow (green→red)    │  · Temperature gauge │
│                               │  · Mileage gauge     │
├───────────────────────────────┼──────────────────────┤
│  PRESCRIPTIVE ANALYTICS       │  I/O SIMULATOR       │
│  · Action recommendation      │  · Mileage slider    │
│  · Lead time to failure       │  · Pressure slider   │
│  · Performance metrics        │  · Temperature slider│
├───────────────────────────────┴──────────────────────┤
│  ASSET HEALTH TREND ANALYSIS  │  STRATEGIC ROI       │
│  · Dual-axis Plotly chart     │  · Uptime uplift     │
│  · Pressure decay + temp rise │  · Cost avoidance    │
│  · Critical threshold lines   │  · Fuel savings      │
└──────────────────────────────────────────────────────┘
```

**Use the I/O Simulator** (right panel) to test scenarios:
- Drag pressure below 28 PSI → watch status escalate to 🛑 CRITICAL
- Push temperature above 85°C → triggers RUBBER DEGRADATION warning
- Set mileage > 40,000 km → END OF SERVICE LIFE alert activates

---

## 📁 Project Structure

```
Digital-Twin-Project/
│
├── app.py                          # Main Streamlit application
├── offorad_vehicle_tires.glb       # 3D tire model (Google Model Viewer)
└── README.md
```

---

## ⚙️ Key Constants Reference

```python
# Pressure (PSI)
OPTIMAL_PRESSURE_RANGE     = (30.0, 35.0)
WEAR_THRESHOLD_PRESSURE    = 28.0   # Critical under-inflation
OVERPRESSURE_THRESHOLD     = 38.0   # Critical over-inflation / blowout risk

# Temperature (°C)
OPTIMAL_TEMP_RANGE         = (45.0, 70.0)
TEMP_ALERT_THRESHOLD       = 75.0
CRITICAL_TEMP_THRESHOLD    = 85.0   # Rubber degradation onset

# Mileage (km)
MILEAGE_ALERT_THRESHOLD    = 35_000
HIGH_MILEAGE_THRESHOLD     = 40_000  # Typical tire service life

# Cost Model ($)
BASE_MAINTENANCE_COST      = 1_200
TIRE_REPLACEMENT_COST      = 800
DAILY_OPERATIONAL_COST     = 1_200   # Per day of downtime
CATASTROPHIC_FAILURE_COST  = 5_000
```

---

## 🛣️ Potential Extensions

- [ ] **Live IoT integration** — replace sliders with MQTT/WebSocket sensor feeds
- [ ] **Fleet dashboard** — multi-asset overview with aggregate risk scoring
- [ ] **ML wear model** — replace heuristic risk engine with trained regression model
- [ ] **Alert notifications** — SMS/email triggers on status escalation
- [ ] **Historical logging** — persist telemetry to database for trend analysis
- [ ] **Multi-component twins** — extend beyond tires to brakes, suspension, engine

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built as part of the Erasmus Meta 4.0 research initiative · Digital Twin Prescriptive Maintenance</sub>
</p>
