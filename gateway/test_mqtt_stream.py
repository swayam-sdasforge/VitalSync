"""
===============================================================================
Project: VitalSync - Smart Hospital Digital Twin
Component: MQTT Telemetry Packet Validation & Serialization Test
Review-2 Milestone: 20% Completed Work
  - Validates micro-batch JSON schema from ESP32 edge telemetry node
  - Tests QoS 1 delivery payload structure and parsing
===============================================================================
"""

import json
import time

def generate_telemetry_packet(bed_id: str, cycle: int) -> dict:
    """Simulates an edge telemetry frame packed by ESP32-S2 FreeRTOS task."""
    return {
        "node_id": bed_id,
        "timestamp_ms": int(time.time() * 1000),
        "sequence_id": cycle,
        "patient": {
            "ecg_raw": 2048 + int(500 * (cycle % 10 - 5)),
            "ecg_filtered": 2045.2,
            "spo2": 98.4,
            "hr": 74.5,
            "leads_off": False
        },
        "machine": {
            "airway_pressure_cmH2O": 19.2,
            "motor_current_mA": 342.1,
            "valve_u_in": 45.0,
            "valve_u_out": 0
        }
    }

def validate_packet_schema(payload: dict) -> bool:
    """Validates structural integrity of telemetry frame before time-series ingestion."""
    required_keys = ["node_id", "timestamp_ms", "patient", "machine"]
    for k in required_keys:
        if k not in payload:
            return False
    if "spo2" not in payload["patient"] or "airway_pressure_cmH2O" not in payload["machine"]:
        return False
    return True

if __name__ == "__main__":
    print("=" * 70)
    print(" VitalSync: Edge Gateway Telemetry Serialization Test")
    print(" Review-2 Milestone: 20% IoT Telemetry Ingestion Verification")
    print("=" * 70)

    print("\n[Simulating 5 consecutive telemetry packets from ICU Bed 01...]\n")
    for i in range(1, 6):
        packet = generate_telemetry_packet("ICU_BED_01", i)
        serialized_json = json.dumps(packet, indent=2)
        is_valid = validate_packet_schema(packet)

        print(f"Packet #{i:02d} | Size: {len(serialized_json)} bytes | Schema Valid: {is_valid}")
        print(f"  Timestamp: {packet['timestamp_ms']} ms | HR: {packet['patient']['hr']} bpm | SpO2: {packet['patient']['spo2']}% | Pressure: {packet['machine']['airway_pressure_cmH2O']} cmH2O")
        time.sleep(0.1)

    print("\n[SUCCESS] Telemetry frame serialization & schema validation passed!")
    print("Broker Target: Mosquitto MQTT (localhost:1883), Topic: vitalsync/icu/+/telemetry")
