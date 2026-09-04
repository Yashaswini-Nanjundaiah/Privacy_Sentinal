from evidence_engine import calculate_evidence


def test_known_device_low_concern():

    features = {
        "device_id": "AA:BB:CC:11:22:33",
        "session_id": "TEST_001",
        "persistence_seconds": 120,
        "observation_count": 3,
        "rssi_std": 2.5
    }

    result = calculate_evidence(
        features,
        "KNOWN"
    )

    assert result["assessment"] == "LOW CONCERN"
    assert result["score"] == 0
    assert result["evidence"] == []


def test_unknown_persistent_device_requires_investigation():

    features = {
        "device_id": "11:22:33:44:55:66",
        "session_id": "TEST_002",
        "persistence_seconds": 400,
        "observation_count": 25,
        "rssi_std": 6.0
    }

    result = calculate_evidence(
        features,
        "UNKNOWN"
    )

    assert result["score"] == 4
    assert result["assessment"] == "REQUIRES INVESTIGATION"