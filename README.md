Unauthorized Mobile Device Detection using Wi-Fi & BLE with Machine Learning

A non-intrusive RF intrusion detection system that identifies unauthorized mobile phones in restricted environments by analyzing Wi-Fi and Bluetooth (BLE) signal behavior using ESP32 and Machine Learning.

---

Problem Statement

In sensitive environments such as:

- Prisons
- Examination halls
- Military / secure zones
- Research laboratories

Unauthorized mobile devices can enable:

- Illegal communication
- Data leakage
- Security violations

Conventional detection systems are:

- Expensive
- Intrusive
- Legally restricted (interception-based)

 This project proposes a low-cost, passive detection system that detects device presence and suspicious activity patterns without intercepting communication.

---

Objectives

- Detect unauthorized mobile devices
- Monitor Wi-Fi and Bluetooth activity
- Identify suspicious communication behavior
- Apply Machine Learning for intelligent classification
- Generate real-time alerts

---

System Overview

ESP32 (Wi-Fi + BLE Scan)
        ↓
Data Transmission (Serial / Wi-Fi)
        ↓
PC (Feature Extraction + ML Model)
        ↓
Device Classification
        ↓
  Alert / Logging

---

 Working Principle

1. ESP32 scans wireless signals
   
   - Wi-Fi Promiscuous Mode
   - BLE Scan Mode

2. Captured Data
   
   - MAC Address
   - RSSI (Signal Strength)
   - Timestamp

3. Data Processing on PC
   
   - Feature extraction
   - Behavior analysis

4. Machine Learning Classification
   
   - Authorized
   - Unknown
   - Suspicious

5. Alert Generation
   
   - Real-time detection of suspicious devices
---

   Flow of Usage 

1. Upload ESP32 firmware
2. Open serial (ESP32 running)
3. Run:
   python detect.py
4. See output

---

 Key Features

- Passive detection (no data interception)
- Real-time monitoring
- Low-cost hardware (ESP32)
- ML-based behavioral classification
- Scalable (multi-node support)
- Works even when device is idle

---

Tech Stack

Hardware

- ESP32 (Wi-Fi + BLE)

Software

- Python

Libraries

- scikit-learn
- pandas
- numpy
- pyserial

Concepts

- RF signal analysis
- Feature engineering
- Machine learning

---


Getting Started

1. Install dependencies

pip install -r requirements.txt

2. Train the model

python train_model.py

3. Run real-time detection

python realtime_detection.py

---

Sample Output

ALERT: Suspicious Device Detected
MAC: XX:XX:XX
RSSI: -50 dBm
Status: Active communication suspected

---

Machine Learning Approach

- Algorithms: Random Forest / SVM
- Input Features:
  - RSSI mean
  - RSSI variance
  - Packet rate
  - Time persistence
  - Known/Unknown flag

Instead of fixed thresholds, the model learns behavioral patterns of device activity.

---

Applications

- Prison security systems
- Examination monitoring
- Military communication zones
- Secure industrial facilities
- Smart surveillance systems

---

Limitations

- MAC randomization in modern smartphones
- Cannot detect actual call content
- Cellular-only activity may not always be visible

---

 Future Work

- Multi-node localization system
- Advanced ML models (deep learning)
- Integration with SDR for cellular activity detection
- Cloud-based dashboard

---

 License

Licensed under the MIT License.

---

 Summary

«This project demonstrates a practical RF-based intrusion detection system that leverages wireless signal behavior and machine learning to identify unauthorized mobile devices in real time without violating privacy.»

---

