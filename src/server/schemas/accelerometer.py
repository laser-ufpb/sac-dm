from pydantic import BaseModel


class AccelerometerSchema(BaseModel):
    device_id: str
    label: str
    ACx: float
    ACy: float
    ACz: float
    timestamp: str