from fastapi import APIRouter, HTTPException
from models.sensors import SensorReadingModel
from services.sensors import srv_create_sensor_reading

router = APIRouter(prefix="/api")

@router.post(
    "/sensor/reading",
    summary="Create a new sensor reading",
    description="Insert a new reading from a sensor into the database.",
    response_description="Sensor reading created successfully.",
    responses={
        201: {
            "description": "Sensor reading created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Sensor reading created successfully"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid input data format"
                    }
                }
            }
        }
    }
)
async def create_sensor_reading(body: SensorReadingModel):
    """
    Insert a new sensor reading into the database.

    The request body should be structured as follows:
    {
        "sensor_id": <str>,
        "station_code": <int>,
        "date": <str>,
        "type": <str>,  // Type of measurement ("temperature", "wind", "humidity")
        "measurement": <float>,  // Measured value
        "unit": <str>  // Unit of the measurement ("Celsius", "m/s", "%")
    }

    - `sensor_id`: The unique identifier for the sensor.
    - `station_code`: The code of the station where the sensor is located.
    - `date`: The date and time of the reading in ISO 8601 format.
    - `type`: The type of measurement ("temperature", "wind", "humidity").
    - `measurement`: The measured value.
    - `unit`: The unit of the measurement ("Celsius", "m/s", "%").
    """
    try:
        return await srv_create_sensor_reading(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
