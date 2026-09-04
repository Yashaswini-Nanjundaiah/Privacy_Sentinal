from behaviour_engine import calculate_device_features
from evidence_engine import calculate_evidence
import pandas as pd

data = pd.read_csv("../data/observations.csv")

device_id = "AA:BB:CC:11:22:33"

features = calculate_device_features(
    device_id,
    data
)

result = calculate_evidence(
    features,
    "KNOWN"
)

print("\nEvidence Result")
print("----------------")
print("Score:", result["score"])
print("Assessment:", result["assessment"])

print("\nEvidence:")
for item in result["evidence"]:
    print("-", item)