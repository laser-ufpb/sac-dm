from typing import Optional
from pydantic import BaseModel


class DeviceSchema(BaseModel):
    device_code: str
    status_id: Optional[int]
    vehicle_id: Optional[int]