
import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Privacy Sentinel",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# AUTO REFRESH
# ==========================================

st_autorefresh(
    interval=2000,
    key="privacy_sentinel_refresh"
)


# ==========================================
# API CONFIGURATION
# ==========================================

API_URL = "http://127.0.0.1:8000"


# ==========================================
# API FUNCTIONS
# ==========================================

def get_devices():

    try:

        response = requests.get(
            f"{API_URL}/devices",
            timeout=2
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:

        return []

    return []


def get_observations():

    try:

        response = requests.get(
            f"{API_URL}/observations",
            timeout=2
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:

        return []

    return []


def get_rssi_history(device_id):

    try:

        response = requests.get(
            f"{API_URL}/devices/{device_id}/rssi",
            timeout=2
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:

        return []

    return []


def enroll_device(device_id, name, device_type):

    try:

        response = requests.post(
            f"{API_URL}/devices/enroll",
            json={
                "device_id": device_id,
                "name": name,
                "type": device_type
            },
            timeout=2
        )

        return response

    except requests.exceptions.RequestException:

        return None


# ==========================================
# HEADER
# ==========================================

st.title("🛡️ Privacy Sentinel")

st.caption(
    "Wireless Environment Monitor"
)


# ==========================================
# FETCH DATA
# ==========================================

devices = get_devices()

observations = get_observations()


# ==========================================
# NO DEVICES
# ==========================================

if not devices:

    st.warning(
        "No devices detected."
    )

    st.stop()


# ==========================================
# MAIN LAYOUT
# ==========================================

left, right = st.columns([1, 2])


# ==========================================
# LEFT SIDE
# ==========================================

with left:

    st.header("Live Observations")


    # --------------------------------------
    # LIVE OBSERVATIONS
    # --------------------------------------

    if observations:

        for observation in observations:

            timestamp = observation["timestamp"]


            if "T" in timestamp:

                time_only = (
                    timestamp.split("T")[1][:8]
                )

            else:

                time_only = timestamp[:8]


            device_name = (
                observation["device_name"]
            )


            if device_name == "Unknown":

                device_name = (
                    f"Unknown "
                    f"({observation['device_id'][-5:]})"
                )


            st.write(
                f"**{time_only}**  |  "
                f"{device_name}  |  "
                f"{observation['rssi']} dBm  |  "
                f"{observation['device_status']}"
            )


    else:

        st.info(
            "Waiting for observations..."
        )


    st.divider()


    # --------------------------------------
    # DEVICE SELECTION
    # --------------------------------------

    st.subheader(
        "Select Device"
    )


    device_names = []


    for device in devices:

        name = device["device_name"]


        if name == "Unknown":

            name = (
                f"Unknown "
                f"({device['device_id'][-5:]})"
            )


        device_names.append(name)


    selected_name = st.radio(
        "Device",
        device_names
    )


    # --------------------------------------
    # FIND SELECTED DEVICE
    # --------------------------------------

    selected_device = None


    for device in devices:

        display_name = (
            device["device_name"]
        )


        if display_name == "Unknown":

            display_name = (
                f"Unknown "
                f"({device['device_id'][-5:]})"
            )


        if display_name == selected_name:

            selected_device = device

            break


# ==========================================
# RIGHT SIDE
# ==========================================

with right:

    st.header(
        "Device Details"
    )


    if selected_device:

        device = selected_device


        # ==================================
        # DEVICE IDENTITY
        # ==================================

        st.subheader(
            device["device_name"]
        )


        st.write(
            f"**Device ID:** "
            f"`{device['device_id']}`"
        )


        st.write(
            f"**Status:** "
            f"{device['device_status']}"
        )


        st.divider()


        # ==================================
        # KEY METRICS
        # ==================================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Latest RSSI",
                f"{device['latest_rssi']} dBm"
            )


        with col2:

            st.metric(
                "Observations",
                device["observation_count"]
            )


        with col3:

            st.metric(
                "RSSI Variation",
                f"{device['rssi_std']} dBm"
            )


        st.divider()


        # ==================================
        # OBSERVATION HISTORY
        # ==================================

        st.subheader(
            "Observation History"
        )


        st.write(
            f"**First seen:** "
            f"{device['first_seen']}"
        )


        st.write(
            f"**Last seen:** "
            f"{device['last_seen']}"
        )


        st.write(
            f"**Average RSSI:** "
            f"{device['average_rssi']} dBm"
        )


        # ==================================
        # RSSI GRAPH
        # ==================================

        st.divider()


        st.subheader(
            "RSSI Signal History"
        )


        rssi_history = get_rssi_history(
            device["device_id"]
        )


        if rssi_history:

            chart_data = {
                "RSSI (dBm)": [
                    item["rssi"]
                    for item in rssi_history
                ]
            }


            st.line_chart(
                chart_data
            )


        else:

            st.info(
                "Waiting for RSSI observations..."
            )


        st.divider()


        # ==================================
        # EVIDENCE
        # ==================================

        st.subheader(
            "Evidence"
        )


        if device["evidence"]:

            for evidence in device["evidence"]:

                st.write(
                    "•",
                    evidence
                )

        else:

            st.info(
                "No evidence available."
            )


        st.divider()


        # ==================================
        # ASSESSMENT
        # ==================================

        st.subheader(
            "Assessment"
        )


        st.write(
            f"**{device['assessment']}**"
        )


        st.write(
            f"Evidence score: "
            f"**{device['score']}**"
        )


        # ==================================
        # ENROLL UNKNOWN DEVICE
        # ==================================

        if device["device_status"] == "UNKNOWN":

            st.divider()


            st.subheader(
                "Identify This Device"
            )


            st.write(
                "If you have identified this "
                "device, add it to the "
                "known-device profile."
            )


            with st.form(
                "enrollment_form"
            ):

                device_name = st.text_input(
                    "Device Name",
                    placeholder="Example: My Phone"
                )


                device_type = st.selectbox(
                    "Device Type",
                    [
                        "Phone",
                        "Laptop",
                        "Television",
                        "Router",
                        "Tablet",
                        "Smart Speaker",
                        "Other"
                    ]
                )


                submit = st.form_submit_button(
                    "Enroll Device"
                )


                if submit:

                    if not device_name.strip():

                        st.error(
                            "Please enter a "
                            "device name."
                        )

                    else:

                        response = enroll_device(
                            device["device_id"],
                            device_name.strip(),
                            device_type
                        )


                        if response is not None:

                            if response.status_code == 200:

                                st.success(
                                    f"{device_name} "
                                    f"has been enrolled."
                                )


                                st.rerun()


                            else:

                                st.error(
                                    "Enrollment failed: "
                                    f"{response.text}"
                                )

                        else:

                            st.error(
                                "Could not connect "
                                "to backend."
                            )

