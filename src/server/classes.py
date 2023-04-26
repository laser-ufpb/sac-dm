from pydantic import BaseModel
from typing import Optional

# New class for the devices data
class Devices(BaseModel):
    device_code: str
    time_stamp: Optional[str]


# New class for the sac_dm datas
class Sac_dm_data(BaseModel):
    device_code: str
    time_stamp: Optional[str]
    value: Optional[int]


# New class for the accelerometer data
class Accelerometer_data(BaseModel):
    device_code: str
    time_stamp: Optional[str]
    ACx: Optional[float]
    ACy: Optional[float]
    ACz: Optional[float]