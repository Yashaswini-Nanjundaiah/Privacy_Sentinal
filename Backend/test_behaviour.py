import pandas as pd
from behaviour_engine import calculate_device_features


data = pd.read_csv("../data/observations.csv")

device_id = "AA:BB:CC:11:22:33"

features = calculate_device_features(
    device_id,
    data
)

print(features)