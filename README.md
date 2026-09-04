# Privacy Sentinel

### Explainable Wireless Anomaly Monitoring

Privacy Sentinel is a local-first wireless monitoring system that observes nearby wireless environments and analyzes device behaviour over time to identify unfamiliar devices that may require investigation.

## Problem

Wireless environments contain many devices such as phones, televisions, laptops, and other connected devices.

Existing wireless scanning tools can show detected devices and signal strength, but they generally require the user to manually interpret this information.

An unfamiliar device is not necessarily malicious, so simply detecting an unknown device is not sufficient.

Privacy Sentinel aims to provide behavioural context around detected devices and generate an explainable assessment instead of making a direct threat claim.

## Solution

Privacy Sentinel collects wireless observations containing:

- Device identifier
- RSSI (signal strength)
- Timestamp
- Session ID

The system maintains historical observations and calculates behavioural features such as:

- First seen
- Last seen
- Observation count
- Persistence
- Average RSSI
- RSSI variation

These features are combined with device identity information to produce an explainable evidence-based assessment.

## Architecture

    ESP32 / Simulator
            ↓
    Wireless Observations
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

The ESP32 acts as the physical wireless sensing layer and captures wireless observations such as identifiers, RSSI, and timestamps.

The FastAPI backend provides the `/scan` interface through which observations can be submitted to the analytics pipeline.

During software development and testing, a simulator is used to generate controlled observations and evaluate different behavioural scenarios.

The sensing and analytics layers are designed as modular components, allowing the wireless sensing source to communicate with the backend through the same observation interface.

## Evidence-Based Assessment

Privacy Sentinel uses multiple signals rather than relying on a single observation.

The current evidence score considers:

| Evidence | Score |
|---|---:|
| Unknown device | +1 |
| Persistence greater than 5 minutes | +1 |
| At least 20 observations | +1 |
| Noticeable RSSI variation | +1 |

The resulting score is interpreted as:

- **0–1:** Low Concern
- **2:** Moderate Concern
- **3–4:** Requires Investigation

The score represents the amount of behavioural evidence observed by the system. It is **not a probability that a device is malicious or a hidden camera**.

## Current Features

- Wi-Fi/BLE wireless sensing using ESP32
- Wireless observation ingestion through FastAPI
- Session-based observation tracking
- Known and unknown device identification
- Device enrollment
- Historical observation storage
- Behavioural feature extraction
- Persistence analysis
- Observation frequency analysis
- RSSI statistics and variation analysis
- Explainable evidence scoring
- RSSI history visualization
- Live Streamlit dashboard
- Controlled testing through a simulator

## Technology Stack

- **ESP32** — Wireless sensing
- **Python** — Core application logic
- **FastAPI** — Backend API
- **Pandas** — Observation processing and behavioural analysis
- **Streamlit** — Interactive dashboard
- **Pydantic** — Data validation
- **CSV / JSON** — Local observation and device storage
- **Pytest** — Automated testing

## Setup and Installation

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- Git
- pip

The ESP32 is required only for the physical wireless sensing component. The software pipeline can be run independently using the simulator.

### 1. Clone the Repository

    git clone https://github.com/Yashaswini-Nanjundaiah/Privacy_Sentinal.git
    cd Privacy_Sentinal

### 2. Create a Virtual Environment

    python -m venv venv

Activate the virtual environment.

**Windows:**

    venv\Scripts\activate

**Linux / macOS:**

    source venv/bin/activate

### 3. Install Dependencies

    pip install -r Backend/requirements.txt

## Running the Application

Privacy Sentinel consists of three software components:

1. FastAPI Backend
2. Wireless Observation Simulator
3. Streamlit Dashboard

Run each component in a separate terminal.

### Terminal 1 — Start FastAPI Backend

From the project root:

    cd Backend
    uvicorn main:app --host 0.0.0.0 --port 8000

The backend will run at:

    http://localhost:8000

FastAPI documentation is available at:

    http://localhost:8000/docs

### Terminal 2 — Start the Simulator

Open a new terminal in the project root:

    python simulator.py

The simulator generates controlled wireless observations and sends them to the FastAPI backend.

### Terminal 3 — Start the Streamlit Dashboard

Open another terminal in the project root:

    streamlit run Frontend/app.py

The dashboard will be available at:

    http://localhost:8501

## Hardware Sensing

The ESP32 acts as the physical wireless sensing layer.

It can scan the nearby wireless environment and capture observations such as:

- Wireless identifier
- RSSI
- Timestamp

The ESP32 sensing layer can provide observations to the FastAPI backend through the `/scan` interface using the observation format expected by the backend.

The ESP32 is a wireless sensing component and is not intended to function as a universal RF detector.

## Project Structure

    Privacy_Sentinal/
    │
    ├── Backend/
    │   ├── main.py
    │   ├── models.py
    │   ├── device_manager.py
    │   ├── behaviour_engine.py
    │   ├── evidence_engine.py
    │   ├── test_behaviour.py
    │   ├── test_evidence.py
    │   └── requirements.txt
    │
    ├── Frontend/
    │   └── app.py
    │
    ├── data/
    │   ├── devices.json
    │   └── evaluation/
    │       ├── test_01_known.csv
    │       ├── test_02_temporary.csv
    │       └── test_03_variable_rssi.csv
    │
    ├── simulator.py
    │
    └── README.md

## Testing

The project includes automated tests for the behavioural and evidence engines using Pytest.

Run the tests from the project root:

    pytest

Controlled simulator scenarios are also used to evaluate how the system responds to different wireless behaviours, including:

- Known devices
- Unknown devices
- Persistent observations
- Temporary observations
- Variable RSSI behaviour

This allows the analytics and evidence logic to be tested independently of the physical sensing hardware.

## Limitations

Privacy Sentinel does not directly detect hidden cameras.

The current prototype identifies and analyzes observable wireless entities and prioritizes unfamiliar persistent devices for further investigation.

An unknown device is not necessarily malicious. The system therefore provides an evidence-based concern assessment rather than declaring a device to be a threat.

RSSI is treated as behavioural evidence rather than an exact distance or location measurement because signal strength is affected by environmental conditions, interference, device orientation, and physical obstacles.

Standard ESP32 wireless scanning capabilities also impose limitations on the types of devices and RF information that can be observed.

## Future Scope

Potential future improvements include:

- Additional wireless sensing hardware
- More advanced behavioural modelling
- Long-term baseline learning
- Improved anomaly detection
- Multi-sensor correlation
- Persistent databases for larger deployments
- Remote monitoring and centralized deployment
- Additional wireless protocols and sensing capabilities

## Disclaimer

Privacy Sentinel is a privacy-monitoring and anomaly-assessment prototype.

Its assessments are intended to help users identify wireless observations that may deserve further investigation. They should not be interpreted as definitive proof of malicious activity, surveillance equipment, or security threats.
