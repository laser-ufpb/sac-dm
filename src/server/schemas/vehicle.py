from typing import Optional
from pydantic import BaseModel


class VehicleSchema(BaseModel):
    model: str
    manufacturer: str
    manufacture_year: Optional[int]
    engine_type: Optional[str]
    number_of_engines: Optional[int]
    status_id: Optional[int]