import serial
import numpy as np
import joblib
from collections import defaultdict, deque
from datetime import datetime

SERIAL_PORT = 'COM3'
BAUD_RATE = 115200
WINDOW_SIZE = 20
MODEL_PATH = "model.pkl"

AUTHORIZED_MACS = {
    "AA:BB:CC:DD:EE:FF"  # Add your authorized MACs here
}

device_history = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))

# Load trained model
try:
    model = joblib.load(MODEL_PATH)
    print(" Model loaded successfully\n")
except FileNotFoundError:
    print(" model.pkl not found. Run train_model.py first.")
    exit()

def extract_features(history, mac):
    if len(history) < 5:
        return None

    rssi_values = [h[0] for h in history]
    times = [h[1] for h in history]

    rssi_mean = np.mean(rssi_values)
    rssi_std = np.std(rssi_values)
    duration = times[-1] - times[0]
    packet_rate = len(history) / (duration + 1)
    known = 1 if mac in AUTHORIZED_MACS else 0

    return [rssi_mean, rssi_std, packet_rate, duration, known]

def run():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(" Real-time detection started...\n")

    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()

            if not line or line.startswith("TYPE") or line == "READY":
                continue

            parts = line.split(",")
            if len(parts) != 4:
                continue

            dev_type, mac, rssi, ts = parts
            rssi = int(rssi)
            ts = int(ts)

            device_history[mac].append((rssi, ts))
            features = extract_features(device_history[mac], mac)

            if features:
                prediction = model.predict([features])[0]
                time_now = datetime.now().strftime("%H:%M:%S")

                if prediction == "Suspicious":
                    print(f"[{time_now}]  ALERT     → {mac} | RSSI: {rssi} dBm")
                elif prediction == "Authorized":
                    print(f"[{time_now}]  Authorized → {mac} | RSSI: {rssi} dBm")
                else:
                    print(f"[{time_now}]   Unknown   → {mac} | RSSI: {rssi} dBm")

        except KeyboardInterrupt:
            print("\n Detection stopped.")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()