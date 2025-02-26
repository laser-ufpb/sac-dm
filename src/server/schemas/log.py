from pydantic import BaseModel
from typing import Optional


class LogSchema(BaseModel):
    device_id: int
    vehicle_id: int
    condition_id: int
    timestamp: str