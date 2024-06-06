from pydantic import BaseModel
from typing import Optional


class SACDMSchema(BaseModel):
    device_id: int
    value: float
    timestamp: str
    label: str
    vehicle_id: Optional[int]