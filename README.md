# VitalSync: Smart Hospital Digital Twin
### *Dual-AI Edge Telemetry & Real-Time Root-Cause ICU Disambiguation Engine*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![C++](https://img.shields.io/badge/Firmware-ESP32--S2-red.svg)](https://espressif.com/)
[![Docker](https://img.shields.io/badge/Docker-Mosquitto%20%7C%20InfluxDB-2496ED.svg)](https://www.docker.com/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT%20QoS%201-orange.svg)](https://mqtt.org/)
[![Milestone](https://img.shields.io/badge/MDP%20Review%202-20%25%20Completed-brightgreen.svg)]()

---

## 📌 Executive Summary

Modern Intensive Care Units (ICUs) face a critical crisis: **between 72% and 99% of all bedside medical alarms are clinically non-actionable or false.** This leads to severe sensory desensitization ("alarm fatigue"), sleep disruption for critical patients, and delayed response times during genuine cardiac or respiratory arrests.

Existing ICU monitoring systems treat physiological vitals (heart rate, SpO2) and life-support machine mechanics (ventilator airway pressure, motor current) as isolated data silos. When an airway pressure threshold triggers, nurses cannot distinguish whether:
1. The **patient is deteriorating** (bronchospasm, pulmonary edema), or
2. The **equipment is mechanically failing** (loose breathing tube, humidification water trap blockage, or valve wear).

**VitalSync** solves this fundamental blindspot by building a high-speed, offline edge digital twin that cross-references continuous patient vitals with ventilator pneumatic telemetry, isolating the actual root cause in real time and routing alerts appropriately.

---

## 🗂️ Repository Architecture

```text
VitalSync/
│
├── firmware/
│   └── esp32_sensor_node.ino          # ESP32-S2 sensor telemetry with 50 Hz digital notch filter
│
├── data_pipeline/
│   └── feature_engineering.py        # Pipeline computing 18 rolling temporal & hemodynamic features
│
├── gateway/
│   ├── docker-compose.yml             # Containerized Eclipse Mosquitto broker & InfluxDB v2
│   ├── mosquitto.conf                 # Edge MQTT broker listener and persistence configuration
│   └── test_mqtt_stream.py            # Telemetry serialization & micro-batch schema validator
│
├── models/
│   └── root_cause_engine.py           # 4-State Bivariate Decision Arbitrator matching Slide 8
│
└── README.md                          # Project documentation and Review-2 verification guide
```

---

## 🎯 Review-2 Milestone Deliverables (~20% Completion)

| Module | Review-2 Completed Work | Status |
| :--- | :--- | :---: |
| **Edge Hardware (ECE)** | Wired ESP32-S2 with AD8232 ECG (ADC1), MAX30100 (SpO2/HR), BMP280, and INA219. | ✅ **Done** |
| **Signal Processing** | Implemented 2nd-order 50 Hz digital notch filter on ESP32 to eliminate AC mains powerline hum. | ✅ **Done** |
| **IoT Telemetry** | Micro-batch JSON serialization with guaranteed QoS 1 MQTT delivery over local hospital Wi-Fi. | ✅ **Done** |
| **Data Engineering** | Structured Google Brain Ventilator (100k+ cycles) and MIMIC-IV clinical datasets. | ✅ **Done** |
| **Feature Extraction** | Formulated 18 rolling statistical and hemodynamic features (Shock Index, ROX Index, MAP, variance). | ✅ **Done** |
| **Disambiguation Logic**| 4-State Root-Cause Arbitrator separating equipment faults from clinical emergencies. | ✅ **Done** |

---

## 🧠 The 4-State Root-Cause Disambiguation Logic

Traditional monitors beep loudly regardless of root cause. VitalSync routes every event based on the joint state of both AI streams:

```
                  +-----------------------------------+
                  |  Machine Telemetry (BiLSTM AI)    |
                  |  ΔP = |P_actual - P_predicted|    |
                  +-----------------+-----------------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
    ΔP < 2.0 (Nominal)                                 ΔP >= 2.0 (Fault)
          |                                                   |
   [Check Patient AI]                                  [Check Patient AI]
   Risk >= 60%?                                        Risk >= 60%?
     /        \                                          /        \
   NO          YES                                     NO          YES
   |            |                                       |            |
   v            v                                       v            v
STATE 1      STATE 2                                 STATE 3      STATE 4
GREEN        BLUE                                    AMBER        RED
Nominal      Patient Crisis                          Equipment    Asynchrony
Operation    -> ICU Doctor                           Fault        -> Pulmonologist
(Silent)     (Audible Siren)                         -> Bio-Eng   (Audible Siren)
                                                     (Silent)
```

### Direct Clinical Benefit:
- When a breathing tube pops loose (State 3), **zero loud sirens sound in the ICU room**. A silent maintenance ticket is dispatched directly to biomedical engineering, targeting a **>40% reduction in non-actionable alarms**.

---

## 🚀 Quickstart & Verification

### 1. Test the 18-Feature Extraction Pipeline
```bash
python data_pipeline/feature_engineering.py
```
*Output: Computes Shock Index, Pulse Pressure, 15-minute rolling averages, and rate of change vectors.*

### 2. Test the Root-Cause Disambiguation Engine
```bash
python models/root_cause_engine.py
```
*Output: Simulates all 4 clinical scenarios and validates automatic alert routing.*

### 3. Test MQTT Telemetry Ingestion Schema
```bash
python gateway/test_mqtt_stream.py
```
*Output: Validates JSON payload serialization and timestamp synchronization.*

### 4. Deploy Local Gateway Container (Docker)
```bash
cd gateway
docker compose up -d
```
*Starts local Mosquitto MQTT broker on port `1883` and InfluxDB time-series engine on port `8086`.*

---

## 🎓 Academic Attribution

- **Project:** Major Development Project (MDP) – Review 2 (2026)
- **Institution:** School of Electronics Engineering (SENSE), VIT Chennai
- **Project Domain:** Healthcare IoT, Edge AI, Digital Twin, Biomedical Embedded Systems
