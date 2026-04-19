ML Model Usage Guide

This folder contains the Machine Learning pipeline for detecting unauthorized mobile devices.

---

Files Overview

- "data_collection.py" → Collects real-time data from ESP32 and saves it to CSV
- "train_model.py" → Trains the Machine Learning model
- "detect.py" → Runs real-time detection using the trained model

---

Workflow (Step-by-Step)

Follow these steps in order:

---

Step 1: Data Collection

Run:

python data_collection.py

This will:

- Read data from ESP32
- Extract features
- Save data to "training_data.csv"

Stop manually using:

Ctrl + C

---

Step 2: Train the Model

Run:

python train_model.py

This will:

- Load "training_data.csv"
- Train a Random Forest model
- Save model as:

model.pkl

---

Step 3: Real-Time Detection

Run:

python detect.py

This will:

- Read live data from ESP32
- Predict device behavior
- Output results in real time

---

Output Examples

Authorized → AA:BB:CC:DD:EE:FF
Unknown → 3C:71:BF:XX:XX:XX
ALERT → Suspicious Device Detected

---

Important Notes

- Ensure ESP32 is connected via correct COM port
- Update "SERIAL_PORT" in scripts if needed
- Ensure "model.pkl" exists before running detection
- Minimum 5 data points required for prediction

---

Feature Description

Feature    | Description
RSSI Mean  | Average signal strength
RSSI Std   | Signal variation
Packet Rate| Activity level
Duration   | Time persistence
Known Flag | Authorized device indicator

---

Tips

- Collect data in different scenarios (idle, active phone)
- Use multiple ESP32 nodes for better accuracy
- Improve model with more training data

---

Summary

This module implements:

- Real-time data collection
- Feature engineering
- Machine learning classification
- Live device detection

---