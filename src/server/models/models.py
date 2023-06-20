from pydantic import BaseModel
from typing import Optional, Union


class Device(BaseModel):
    device_code: str
    time_stamp: Optional[str]


class SACDM(BaseModel):
    device_code: str
    time_stamp: Optional[str]
    value: Optional[float]


class AccelerometerData(BaseModel):
    device_code: str
    time_stamp: Optional[str]
    ACx: Optional[float]
    ACy: Optional[float]
    ACz: Optional[float]


class LoginRequest(BaseModel):
    username: str
    password: str
