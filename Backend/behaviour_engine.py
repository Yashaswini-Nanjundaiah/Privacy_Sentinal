import pandas as pd


def calculate_device_features(
    device_id,
    session_id,
    observations
):

    # ==========================================
    # FILTER BY DEVICE + SESSION
    # ==========================================

    device_data = observations[
        (observations["device_id"] == device_id)
        &
        (observations["session_id"] == session_id)
    ].copy()


    if device_data.empty:

        return None


    # ==========================================
    # TIMESTAMP PROCESSING
    # ==========================================

    device_data["timestamp"] = pd.to_datetime(
        device_data["timestamp"],
        format="mixed"
    )


    # ==========================================
    # TIME FEATURES
    # ==========================================

    first_seen = device_data["timestamp"].min()

    last_seen = device_data["timestamp"].max()


    # ==========================================
    # OBSERVATION COUNT
    # ==========================================

    observation_count = len(
        device_data
    )


    # ==========================================
    # RSSI FEATURES
    # ==========================================

    average_rssi = device_data["rssi"].mean()

    min_rssi = device_data["rssi"].min()

    max_rssi = device_data["rssi"].max()

    rssi_std = device_data["rssi"].std()


    if pd.isna(rssi_std):

        rssi_std = 0


    # ==========================================
    # PERSISTENCE
    # ==========================================

    persistence_seconds = (
        last_seen - first_seen
    ).total_seconds()


    # ==========================================
    # RETURN FEATURES
    # ==========================================

    return {

        "device_id": device_id,

        "session_id": session_id,

        "first_seen": first_seen.isoformat(),

        "last_seen": last_seen.isoformat(),

        "observation_count": observation_count,

        "persistence_seconds": persistence_seconds,

        "average_rssi": round(
            average_rssi,
            2
        ),

        "min_rssi": min_rssi,

        "max_rssi": max_rssi,

        "rssi_std": round(
            rssi_std,
            2
        )

    }