from pydantic import BaseModel


class SACDMSchema(BaseModel):
    device_id: int
    value: float
    timestamp: str
    label: str