import serial
import csv
from collections import defaultdict, deque
import numpy as np

SERIAL_PORT = 'COM3'
BAUD_RATE = 115200
WINDOW_SIZE = 20
OUTPUT_FILE = "training_data.csv"

AUTHORIZED_MACS = {
    "AA:BB:CC:DD:EE:FF"  # Add your authorized MACs here
}

device_history = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))

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

def collect():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print("📡 Collecting data... Press Ctrl+C to stop\n")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rssi_mean", "rssi_std", "packet_rate",
            "duration", "known", "label"
        ])

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
                    label = "Authorized" if mac in AUTHORIZED_MACS else "Suspicious"
                    writer.writerow(features + [label])
                    f.flush()
                    print(f" Saved → {mac} | {label}")

            except KeyboardInterrupt:
                print("\n Data collection stopped")
                break
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    collect()