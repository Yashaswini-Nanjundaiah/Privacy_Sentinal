
import requests
import time
import random
from datetime import datetime


URL = "http://127.0.0.1:8000/scan"


# ==========================================
# SIMULATION SETTINGS
# ==========================================

# Choose the behaviour you want to test:
#
# "PERSISTENT"
# "TEMPORARY"
# "VARIABLE_RSSI"

TEST_MODE = "PERSISTENT"
SESSION_ID = "SESSION_003"

# ==========================================
# DEVICES
# ==========================================

devices = [

    {
        "device_id": "AA:BB:CC:11:22:33",
        "base_rssi": -50,
        "device_type": "Television"
    },

    {
        "device_id": "DD:EE:FF:44:55:66",
        "base_rssi": -70,
        "device_type": None
    },

    {
        "device_id": "11:22:33:44:55:66",
        "base_rssi": -60,
        "device_type": None
    }
]


# ==========================================
# TEMPORARY DEVICE CONTROL
# ==========================================

temporary_start = time.time()


# ==========================================
# SIMULATION LOOP
# ==========================================

while True:

    for device in devices:

        device_id = device["device_id"]


        # --------------------------------------
        # TEMPORARY MODE
        # --------------------------------------

        if (
            TEST_MODE == "TEMPORARY"
            and device_id == "11:22:33:44:55:66"
        ):

            elapsed = time.time() - temporary_start

            # Stop sending the test device
            # after 60 seconds.

            if elapsed > 60:

                continue


        # --------------------------------------
        # RSSI GENERATION
        # --------------------------------------

        if (
            TEST_MODE == "VARIABLE_RSSI"
            and device_id == "11:22:33:44:55:66"
        ):

            # Large signal fluctuations
            # for behavioural testing.

            rssi = device["base_rssi"] + random.randint(
                -15,
                15
            )

        else:

            # Normal small variation.

            rssi = device["base_rssi"] + random.randint(
                -4,
                4
            )


        # --------------------------------------
        # OBSERVATION
        # --------------------------------------

        observation = {

    "session_id": SESSION_ID,

    "device_id": device_id,

    "rssi": rssi,

    "timestamp": datetime.now().isoformat(),

    "device_type": device["device_type"]

}


        # --------------------------------------
        # SEND TO BACKEND
        # --------------------------------------

        try:

            response = requests.post(
                URL,
                json=observation
            )


            print(
                f"{observation['timestamp']} | "
                f"{device_id} | "
                f"{rssi} dBm"
            )


            print(
                "Status code:",
                response.status_code
            )


            print(
                "Response:",
                response.text
            )


        except requests.exceptions.ConnectionError:

            print(
                "FastAPI server is not running!"
            )


        time.sleep(1)
