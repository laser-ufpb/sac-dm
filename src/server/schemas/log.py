from pydantic import BaseModel
from typing import Optional


class LogSchema(BaseModel):
    device_id: int
    vehicle_id: int
    status_id: int
    timestamp: str
    axis: str