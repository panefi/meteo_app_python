from pydantic import BaseModel
from datetime import datetime


class SensorReadingModel(BaseModel):
    sensor_id: str
    station_code: int
    date: datetime
    type: str
    measurement: float
    unit: str
