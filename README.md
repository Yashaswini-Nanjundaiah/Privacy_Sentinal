# Privacy Sentinel

### Explainable Wireless Anomaly Monitoring

Privacy Sentinel is a local-first wireless monitoring system that observes nearby wireless devices and analyzes their behaviour over time to identify unfamiliar devices that may require investigation.


## Problem

Wireless environments contain many devices such as phones, televisions,
laptops, and other connected devices.

Existing wireless scanning tools can show detected devices and signal
strength, but they generally require the user to manually interpret this
information.

An unfamiliar device is not necessarily malicious, so simply detecting an
unknown device is not sufficient.

Privacy Sentinel aims to provide behavioural context around detected devices
and generate an explainable assessment instead of making a direct threat claim.

## Solution

Privacy Sentinel collects wireless observations containing:

- Device identifier
- RSSI (signal strength)
- Timestamp
- Session ID

The system maintains historical observations and calculates behavioural
features such as:

- First seen
- Last seen
- Observation count
- Persistence
- Average RSSI
- RSSI variation

These features are combined with device identity information to produce an
explainable evidence-based assessment.

## Architecture

ESP32 / Simulator
        ↓
FastAPI Backend
        ↓
Observation Storage
        ↓
Behaviour Engine
        ↓
Evidence Engine
        ↓
Streamlit Dashboard

The ESP32 provides the wireless observations in the hardware sensing layer.
During software development and testing, a simulator is used to generate
controlled observations for evaluating the analytics pipeline.

## Current Features

- Wireless observation ingestion through FastAPI
- Session-based observation tracking
- Known and unknown device identification
- Device enrollment
- Historical observation storage
- Behavioural feature extraction
- Explainable evidence scoring
- RSSI history visualization
- Live Streamlit dashboard
- Controlled testing through a simulator

## Limitations

Privacy Sentinel does not directly detect hidden cameras.

The current prototype identifies and analyzes wireless devices and prioritizes
unfamiliar persistent devices for further investigation.

RSSI is treated as behavioural evidence rather than an exact distance or
location measurement because signal strength is affected by environmental
conditions, interference, device orientation, and physical obstacles.

ESP32 wireless scanning capabilities also impose limitations on the types of
devices and RF information that can be observed.

