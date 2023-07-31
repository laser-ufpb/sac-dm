from typing import Optional
from pydantic import BaseModel


class Filter(BaseModel):
    device_id: Optional[str]
    datetime_initial: Optional[str]
    datetime_final: Optional[str]