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
# PROFESSIONAL UI STYLING
# ==========================================

st.markdown(
    """
    <style>

    /* ======================================
       GLOBAL
       ====================================== */

    .stApp {
        background-color: #0b0f14;
        color: #e6edf3;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* ======================================
       HEADER
       ====================================== */

    .system-status {
        padding: 0.5rem 0.9rem;
        border-radius: 999px;

        background-color: #0d2115;
        border: 1px solid #238636;

        color: #3fb950;
        font-size: 0.82rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* ======================================
       HEADINGS
       ====================================== */

    h1,
    h2,
    h3 {
        color: #f0f6fc !important;
    }

    /* ======================================
       METRIC CARDS
       ====================================== */

    div[data-testid="stMetric"] {
        background-color: #111820;
        border: 1px solid #26303a;
        border-radius: 12px;
        padding: 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #8b949e;
    }

    div[data-testid="stMetricValue"] {
        color: #f0f6fc;
    }

    /* ======================================
       DEVICE CARDS
       ====================================== */

    .device-card {
        background-color: #111820;
        border: 1px solid #26303a;
        border-radius: 10px;

        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    .device-time {
        font-size: 0.75rem;
        color: #8b949e;
    }

    .device-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #f0f6fc;
        margin-top: 0.2rem;
    }

    .device-info {
        font-size: 0.82rem;
        color: #8b949e;
        margin-top: 0.25rem;
    }

    /* ======================================
       STATUS BADGES
       ====================================== */

    .status-known {
        display: inline-block;

        padding: 0.25rem 0.6rem;

        border-radius: 999px;

        background-color: #0d2115;
        border: 1px solid #238636;

        color: #3fb950;

        font-size: 0.75rem;
        font-weight: 600;
    }

    .status-unknown {
        display: inline-block;

        padding: 0.25rem 0.6rem;

        border-radius: 999px;

        background-color: #211a0d;
        border: 1px solid #9e6a03;

        color: #d29922;

        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ======================================
       RISK BADGES
       ====================================== */

    .risk-low {
        display: inline-block;

        padding: 0.45rem 0.8rem;

        border-radius: 999px;

        background-color: #0d2115;
        border: 1px solid #238636;

        color: #3fb950;

        font-weight: 700;
    }

    .risk-moderate {
        display: inline-block;

        padding: 0.45rem 0.8rem;

        border-radius: 999px;

        background-color: #211a0d;
        border: 1px solid #9e6a03;

        color: #d29922;

        font-weight: 700;
    }

    .risk-high {
        display: inline-block;

        padding: 0.45rem 0.8rem;

        border-radius: 999px;

        background-color: #2d1215;
        border: 1px solid #da3633;

        color: #f85149;

        font-weight: 700;
    }

    /* ======================================
       EVIDENCE
       ====================================== */

    .evidence-item {
        background-color: #161b22;

        border-left: 3px solid #58a6ff;

        border-radius: 6px;

        padding: 0.65rem 0.8rem;

        margin-bottom: 0.5rem;

        color: #c9d1d9;

        font-size: 0.9rem;
    }

    /* ======================================
       BUTTONS
       ====================================== */

    .stButton > button {
        border-radius: 8px;

        border: 1px solid #30363d;

        background-color: #161b22;

        color: #e6edf3;
    }

    .stButton > button:hover {
        border-color: #58a6ff;
        color: #58a6ff;
    }

    /* ======================================
       INPUTS
       ====================================== */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #111820;
        border-color: #30363d;
    }

    /* ======================================
       RADIO GROUP
       ====================================== */

    div[role="radiogroup"] {
        background-color: #111820;

        border: 1px solid #26303a;

        border-radius: 10px;

        padding: 0.6rem;
    }

    /* ======================================
       DIVIDERS
       ====================================== */

    hr {
        border-color: #26303a !important;
    }

    </style>
    """,
    unsafe_allow_html=True
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


def enroll_device(
    device_id,
    name,
    device_type
):

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

header_col1, header_col2 = st.columns(
    [4, 1]
)


with header_col1:

    st.title(
        "🛡️ Privacy Sentinel"
    )

    st.caption(
        "Wireless Environment Monitor"
    )


with header_col2:

    st.success(
        "● SYSTEM ONLINE"
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
# OVERVIEW
# ==========================================

total_devices = len(devices)

known_devices = sum(
    1
    for device in devices
    if device["device_status"] == "KNOWN"
)

unknown_devices = sum(
    1
    for device in devices
    if device["device_status"] == "UNKNOWN"
)

investigation_devices = sum(
    1
    for device in devices
    if device["assessment"] ==
    "REQUIRES INVESTIGATION"
)


st.subheader(
    "Security Overview"
)


overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(
    4
)


with overview_col1:

    st.metric(
        "Total Devices",
        total_devices
    )


with overview_col2:

    st.metric(
        "Known Devices",
        known_devices
    )


with overview_col3:

    st.metric(
        "Unknown Devices",
        unknown_devices
    )


with overview_col4:

    st.metric(
        "Requires Investigation",
        investigation_devices
    )


st.divider()


# ==========================================
# MAIN LAYOUT
# ==========================================

left, right = st.columns(
    [1, 2]
)


# ==========================================
# LEFT SIDE
# ==========================================

with left:

    st.header(
        "Live Observations"
    )


    # ======================================
    # LIVE OBSERVATIONS
    # ======================================

    if observations:

        for observation in observations:

            timestamp = observation[
                "timestamp"
            ]


            if "T" in timestamp:

                time_only = (
                    timestamp
                    .split("T")[1][:8]
                )

            else:

                time_only = timestamp[:8]


            device_name = observation[
                "device_name"
            ]


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


    # ======================================
    # DEVICE SELECTION
    # ======================================

    st.subheader(
        "Select Device"
    )


    device_names = []


    for device in devices:

        name = device[
            "device_name"
        ]


        if name == "Unknown":

            name = (
                f"Unknown "
                f"({device['device_id'][-5:]})"
            )


        device_names.append(
            name
        )


    selected_name = st.radio(
        "Device",
        device_names
    )


    # ======================================
    # FIND SELECTED DEVICE
    # ======================================

    selected_device = None


    for device in devices:

        display_name = device[
            "device_name"
        ]


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

        identity_col1, identity_col2 = st.columns(
            [3, 1]
        )


        with identity_col1:

            st.subheader(
                device["device_name"]
            )


            st.write(
                f"**Device ID:** "
                f"`{device['device_id']}`"
            )


        with identity_col2:

            if (
                device["device_status"]
                == "KNOWN"
            ):

                st.markdown(
                    """
                    <span class="status-known">
                        KNOWN DEVICE
                    </span>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <span class="status-unknown">
                        UNKNOWN DEVICE
                    </span>
                    """,
                    unsafe_allow_html=True
                )


        st.divider()


        # ==================================
        # KEY METRICS
        # ==================================

        st.subheader(
            "Signal & Activity"
        )


        col1, col2, col3 = st.columns(
            3
        )


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


        history_col1, history_col2, history_col3 = st.columns(
            3
        )


        with history_col1:

            st.write(
                "**First seen**"
            )

            st.caption(
                device["first_seen"]
            )


        with history_col2:

            st.write(
                "**Last seen**"
            )

            st.caption(
                device["last_seen"]
            )


        with history_col3:

            st.write(
                "**Average RSSI**"
            )

            st.caption(
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

            for evidence in device[
                "evidence"
            ]:

                st.markdown(
                    f"""
                    <div class="evidence-item">
                        ✓ {evidence}
                    </div>
                    """,
                    unsafe_allow_html=True
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


        assessment = device[
            "assessment"
        ]


        if assessment == "LOW CONCERN":

            st.markdown(
                """
                <span class="risk-low">
                    🟢 LOW CONCERN
                </span>
                """,
                unsafe_allow_html=True
            )


        elif assessment == "MODERATE CONCERN":

            st.markdown(
                """
                <span class="risk-moderate">
                    🟡 MODERATE CONCERN
                </span>
                """,
                unsafe_allow_html=True
            )


        else:

            st.markdown(
                """
                <span class="risk-high">
                    🔴 REQUIRES INVESTIGATION
                </span>
                """,
                unsafe_allow_html=True
            )


        st.write("")


        st.write(
            f"Evidence score: "
            f"**{device['score']} / 4**"
        )


        # ==================================
        # ENROLL UNKNOWN DEVICE
        # ==================================

        if (
            device["device_status"]
            == "UNKNOWN"
        ):

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