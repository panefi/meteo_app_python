from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List


class Measurement(BaseModel):
    value: float = Field(..., description="Measurement value")
    unit: str = Field(..., description="Unit of measurement (e.g., m/s, %, Celsius)")


class ForecastData(BaseModel):
    wind: Measurement
    humidity: Measurement
    temperature: Measurement


class StationForecast(BaseModel):
    date: str = Field(..., description="Date of the forecast")
    station_code: int
    forecast: ForecastData


class StationQueryParams(BaseModel):
    city: Optional[str] = Field(default=None, description="The name of the city to filter stations by.")
    page: Optional[int] = Field(default=1, ge=1, description="The page number for pagination (default is 1).")
    limit: Optional[int] = Field(default=50, ge=1, description="The number of records to return per page (default is 50).")
    sort: str = Field(default="code", description="The column to sort the results by (default is 'code').")
    sort_order: str = Field(default="ASC", description="The order to sort the results (default is 'ASC'). Allowed values are 'ASC' and 'DESC'.")


class Station(BaseModel):
    city: str
    latitude: float
    longitude: float
    installation_date: str


class StationUpdate(BaseModel):
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[str] = None


class StationDataRequest(BaseModel):
    date_from: Optional[str] = None # Format: YYYY-MM-DD
    date_to: Optional[str] = None   # Format: YYYY-MM-DD
    type: Optional[str] = None  # Allowed values: "humidity", "temperature", "wind"
    page: Optional[int] = 1
    limit: Optional[int] = 50
    sort: Optional[str] = "date"  # Allowed values: "date", "sensor_type"
    forecast: Optional[bool] = False
    summary: Optional[bool] = False

class SensorData(BaseModel):
    sensor_id: str
    date: datetime
    type: str  # e.g., 'temperature', 'humidity', 'wind'
    measurement: float
    unit: str  # e.g., 'Celsius', '%', 'm/s'

class BatchData(BaseModel):
    station_code: int
    data: List[SensorData]