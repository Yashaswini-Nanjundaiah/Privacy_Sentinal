import pandas as pd
from behaviour_engine import calculate_device_features


def test_calculate_device_features():
    data = pd.DataFrame([
        {
            "session_id": "TEST_001",
            "device_id": "AA:BB:CC:11:22:33",
            "rssi": -50,
            "timestamp": "2026-09-04T10:00:00",
            "device_type": "Television"
        },
        {
            "session_id": "TEST_001",
            "device_id": "AA:BB:CC:11:22:33",
            "rssi": -52,
            "timestamp": "2026-09-04T10:01:00",
            "device_type": "Television"
        },
        {
            "session_id": "TEST_001",
            "device_id": "AA:BB:CC:11:22:33",
            "rssi": -48,
            "timestamp": "2026-09-04T10:02:00",
            "device_type": "Television"
        }
    ])

    features = calculate_device_features(
        "AA:BB:CC:11:22:33",
        "TEST_001",
        data
    )

    assert features is not None
    assert features["device_id"] == "AA:BB:CC:11:22:33"
    assert features["session_id"] == "TEST_001"
    assert features["observation_count"] == 3
    assert features["persistence_seconds"] == 120
    assert features["min_rssi"] == -52
    assert features["max_rssi"] == -48