
def calculate_evidence(features, device_status):

    evidence = []
    score = 0

    # ==========================================
    # 1. DEVICE IDENTITY
    # ==========================================

    if device_status == "UNKNOWN":

        score += 1

        evidence.append(
            "Device is not registered in the known-device profile."
        )


    # ==========================================
    # 2. PERSISTENCE
    # ==========================================

    if features["persistence_seconds"] > 300:

        score += 1

        evidence.append(
            "Device has remained observable for more than 5 minutes."
        )


    # ==========================================
    # 3. REPEATED OBSERVATIONS
    # ==========================================

    if features["observation_count"] >= 20:

        score += 1

        evidence.append(
            "Device has been observed repeatedly."
        )


    # ==========================================
    # 4. RSSI VARIATION
    # ==========================================

    if features["rssi_std"] >= 5:

        score += 1

        evidence.append(
            "Device shows noticeable variation in signal strength."
        )


    # ==========================================
    # FINAL ASSESSMENT
    # ==========================================

    # Known devices are treated as low concern
    # because they have already been identified
    # and enrolled by the user.

    if device_status == "KNOWN":

        assessment = "LOW CONCERN"

    elif score <= 1:

        assessment = "LOW CONCERN"

    elif score == 2:

        assessment = "MODERATE CONCERN"

    else:

        assessment = "REQUIRES INVESTIGATION"


    return {
        "score": score,
        "assessment": assessment,
        "evidence": evidence
    }

