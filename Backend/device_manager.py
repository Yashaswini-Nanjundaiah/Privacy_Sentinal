import json
import os

DEVICE_FILE = "../data/devices.json"


def load_devices():

    if not os.path.exists(DEVICE_FILE):
        return {}

    with open(DEVICE_FILE, "r") as file:
        return json.load(file)


def get_device_info(device_id):

    devices = load_devices()

    return devices.get(device_id)