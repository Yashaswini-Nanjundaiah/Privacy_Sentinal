from fastapi import FastAPI
from pydantic import BaseModel
from models import DeviceObservation
import pandas as pd
import os
import json

from device_manager import get_device_info
from behaviour_engine import calculate_device_features
from evidence_engine import calculate_evidence


app = FastAPI(title="Privacy Sentinel")


DATA_FILE = "../data/observations.csv"
DEVICE_FILE = "../data/devices.json"


class DeviceEnrollment(BaseModel):
    device_id: str
    name: str
    type: str


@app.get("/health")
def health_check():

    return {
        "status": "running"
    }


@app.post("/scan")
def receive_scan(observation: DeviceObservation):

    # ==========================================
    # CREATE NEW OBSERVATION
    # ==========================================

    new_data = pd.DataFrame([{

        "session_id": observation.session_id,

        "device_id": observation.device_id,

        "rssi": observation.rssi,

        "timestamp": observation.timestamp,

        "device_type": observation.device_type

    }])


    # ==========================================
    # DEVICE IDENTITY
    # ==========================================

    device_info = get_device_info(
        observation.device_id
    )


    if device_info:

        device_name = device_info["name"]

        device_status = "KNOWN"

    else:

        device_name = "Unknown"

        device_status = "UNKNOWN"


    # ==========================================
    # SAVE OBSERVATION
    # ==========================================

    if os.path.exists(DATA_FILE):

        if os.path.getsize(DATA_FILE) == 0:

            new_data.to_csv(
                DATA_FILE,
                index=False
            )

        else:

            new_data.to_csv(
                DATA_FILE,
                mode="a",
                header=False,
                index=False
            )

    else:

        new_data.to_csv(
            DATA_FILE,
            index=False
        )


    # ==========================================
    # LOAD OBSERVATIONS
    # ==========================================

    observations = pd.read_csv(
        DATA_FILE
    )


    # ==========================================
    # BEHAVIOUR ANALYSIS
    # ==========================================

    features = calculate_device_features(
        observation.device_id,
        observation.session_id,
        observations
    )


    # ==========================================
    # EVIDENCE ANALYSIS
    # ==========================================

    evidence_result = calculate_evidence(
        features,
        device_status
    )


    # ==========================================
    # LOG
    # ==========================================

    print(
        f"{observation.timestamp} | "
        f"{observation.session_id} | "
        f"{device_name} | "
        f"{observation.rssi} dBm | "
        f"{device_status} | "
        f"{evidence_result['assessment']}"
    )


    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "status": "received",

        "session_id": observation.session_id,

        "device_id": observation.device_id,

        "device_name": device_name,

        "device_status": device_status,

        "assessment": evidence_result["assessment"],

        "score": evidence_result["score"],

        "evidence": evidence_result["evidence"]

    }


@app.get("/devices")
def get_devices():

    # ==========================================
    # CHECK DATA FILE
    # ==========================================

    if not os.path.exists(DATA_FILE):

        return []


    if os.path.getsize(DATA_FILE) == 0:

        return []


    # ==========================================
    # LOAD OBSERVATIONS
    # ==========================================

    observations = pd.read_csv(
        DATA_FILE
    )


    if observations.empty:

        return []


    # ==========================================
    # DEVICE LIST
    # ==========================================

    devices = []


    for device_id in observations["device_id"].unique():

        device_info = get_device_info(
            device_id
        )


        if device_info:

            device_name = device_info["name"]

            device_status = "KNOWN"

        else:

            device_name = "Unknown"

            device_status = "UNKNOWN"


        # ======================================
        # MOST RECENT SESSION FOR THIS DEVICE
        # ======================================

        device_data = observations[
            observations["device_id"] == device_id
        ].copy()


        latest_session = device_data.iloc[-1]["session_id"]


        # ======================================
        # SESSION-SPECIFIC FEATURES
        # ======================================

        features = calculate_device_features(
            device_id,
            latest_session,
            observations
        )


        # ======================================
        # EVIDENCE
        # ======================================

        evidence_result = calculate_evidence(
            features,
            device_status
        )


        # ======================================
        # LATEST OBSERVATION
        # ======================================

        latest_observation = device_data.iloc[-1]


        # ======================================
        # DEVICE RESPONSE
        # ======================================

        devices.append({

            "device_id": device_id,

            "device_name": device_name,

            "device_status": device_status,

            "session_id": latest_session,

            "latest_rssi": int(
                latest_observation["rssi"]
            ),

            "last_seen": features["last_seen"],

            "first_seen": features["first_seen"],

            "observation_count": features[
                "observation_count"
            ],

            "average_rssi": float(
                features["average_rssi"]
            ),

            "rssi_std": float(
                features["rssi_std"]
            ),

            "assessment": evidence_result[
                "assessment"
            ],

            "score": evidence_result[
                "score"
            ],

            "evidence": evidence_result[
                "evidence"
            ]

        })


    return devices


@app.get("/observations")
def get_observations():

    # ==========================================
    # CHECK DATA FILE
    # ==========================================

    if not os.path.exists(DATA_FILE):

        return []


    if os.path.getsize(DATA_FILE) == 0:

        return []


    # ==========================================
    # LOAD OBSERVATIONS
    # ==========================================

    observations = pd.read_csv(
        DATA_FILE
    )


    if observations.empty:

        return []


    # ==========================================
    # GET RECENT OBSERVATIONS
    # ==========================================

    observations = observations.tail(30)


    result = []


    for _, row in observations.iterrows():

        device_info = get_device_info(
            row["device_id"]
        )


        if device_info:

            device_name = device_info["name"]

            device_status = "KNOWN"

        else:

            device_name = "Unknown"

            device_status = "UNKNOWN"


        result.append({

            "session_id": row["session_id"],

            "device_id": row["device_id"],

            "device_name": device_name,

            "device_status": device_status,

            "rssi": int(row["rssi"]),

            "timestamp": row["timestamp"]

        })


    result.reverse()


    return result


@app.get("/devices/{device_id}/rssi")
def get_rssi_history(
    device_id: str
):

    # ==========================================
    # CHECK DATA FILE
    # ==========================================

    if not os.path.exists(DATA_FILE):

        return []


    if os.path.getsize(DATA_FILE) == 0:

        return []


    # ==========================================
    # LOAD OBSERVATIONS
    # ==========================================

    observations = pd.read_csv(
        DATA_FILE
    )


    # ==========================================
    # FILTER DEVICE
    # ==========================================

    device_data = observations[
        observations["device_id"] == device_id
    ].copy()


    if device_data.empty:

        return []


    # ==========================================
    # RSSI HISTORY
    # ==========================================

    return [

        {

            "timestamp": row["timestamp"],

            "rssi": int(row["rssi"])

        }

        for _, row in device_data.tail(50).iterrows()

    ]


@app.post("/devices/enroll")
def enroll_device(
    enrollment: DeviceEnrollment
):

    # ==========================================
    # LOAD DEVICE PROFILES
    # ==========================================

    if os.path.exists(DEVICE_FILE):

        with open(
            DEVICE_FILE,
            "r"
        ) as file:

            devices = json.load(file)

    else:

        devices = {}


    # ==========================================
    # ADD / UPDATE DEVICE
    # ==========================================

    devices[enrollment.device_id] = {

        "name": enrollment.name,

        "type": enrollment.type

    }


    # ==========================================
    # SAVE DEVICE PROFILE
    # ==========================================

    with open(
        DEVICE_FILE,
        "w"
    ) as file:

        json.dump(
            devices,
            file,
            indent=4
        )


    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "status": "enrolled",

        "device_id": enrollment.device_id,

        "name": enrollment.name,

        "type": enrollment.type

    }