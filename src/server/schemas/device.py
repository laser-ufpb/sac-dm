from pydantic import BaseModel


class DeviceSchema(BaseModel):
    device_code: str