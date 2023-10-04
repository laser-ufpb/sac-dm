from pydantic import BaseModel


class AccelerometerSchema(BaseModel):
    device_id: str
    ACx: float
    ACy: float
    ACz: float
    timestamp: str
    label: str