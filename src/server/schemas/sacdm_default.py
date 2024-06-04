from pydantic import BaseModel


class SACDMDefaultSchema(BaseModel):
    vehicle_id: int
    x_mean: float
    x_standard_deviation: float
    y_mean: float
    y_standard_deviation: float
    z_mean: float
    z_standard_deviation: float