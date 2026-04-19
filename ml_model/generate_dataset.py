import pandas as pd
import numpy as np

np.random.seed(42)
samples = []

# -----------------------------------------------
# Authorized Devices (known, stable, nearby)
# -----------------------------------------------
for _ in range(300):
    rssi_mean = np.clip(
        np.random.uniform(-70, -40) + np.random.normal(0, 1),
        -100, 0
    )
    rssi_std = np.random.uniform(1, 5)
    packet_rate = np.random.uniform(0.5, 2.5)
    duration = np.random.uniform(5000, 30000)
    known = 1
    samples.append([rssi_mean, rssi_std, packet_rate, duration, known, "Authorized"])

# -----------------------------------------------
# Suspicious Devices (unknown, high burst activity)
# -----------------------------------------------
for _ in range(300):
    rssi_mean = np.clip(
        np.random.uniform(-80, -45) + np.random.normal(0, 2),
        -100, 0
    )
    rssi_std = np.random.uniform(5, 20)
    packet_rate = np.random.uniform(3.0, 10.0)
    duration = np.random.uniform(1000, 10000)
    known = 0
    samples.append([rssi_mean, rssi_std, packet_rate, duration, known, "Suspicious"])

# -----------------------------------------------
# Unknown Devices (weak, brief appearance)
# -----------------------------------------------
for _ in range(300):
    rssi_mean = np.clip(
        np.random.uniform(-90, -60) + np.random.normal(0, 1.5),
        -100, 0
    )
    rssi_std = np.random.uniform(3, 10)
    packet_rate = np.random.uniform(0.1, 1.5)
    duration = np.random.uniform(500, 5000)
    known = 0
    samples.append([rssi_mean, rssi_std, packet_rate, duration, known, "Unknown"])

# -----------------------------------------------
# Create DataFrame
# -----------------------------------------------
df = pd.DataFrame(samples, columns=[
    "rssi_mean", "rssi_std", "packet_rate",
    "duration", "known", "label"
])

# Shuffle
df = df.sample(frac=1).reset_index(drop=True)

# Save
df.to_csv("training_data.csv", index=False)

print(f" Dataset created: {len(df)} samples\n")
print("Class Distribution:")
print(df["label"].value_counts(), "\n")
print("Preview:")
print(df.head(10))