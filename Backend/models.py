from pydantic import BaseModel
from typing import Optional


class DeviceObservation(BaseModel):

    session_id: str
    device_id: str
    rssi: int
    timestamp: str
    device_type: Optional[str] = None