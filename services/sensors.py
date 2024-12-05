from models.sensors import SensorReadingModel
import database.database as database
import database.queries.sensors as sensors_queries
from fastapi import HTTPException


async def srv_create_sensor_reading(sensor_reading: SensorReadingModel):
    """
    Insert a new sensor reading into the sensors_data table
    """
    try:
        async with database.SQLConnection() as db:
            await db.execute_query(
                sensors_queries.CREATE_SENSOR_DATA,
                (
                    sensor_reading.sensor_id,
                    sensor_reading.station_code,
                    sensor_reading.date,
                    sensor_reading.type,
                    sensor_reading.measurement,
                    sensor_reading.unit
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Sensor reading created successfully"}