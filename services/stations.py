from typing import Optional, List
import database.database as database
import database.queries.stations as stations_queries
from models.stations import StationForecast, Station, StationUpdate, StationDataRequest, BatchData
from fastapi import HTTPException
from mysql.connector.errors import IntegrityError
import utils.stations as utils

async def srv_create_station_forecast(station_forecast: StationForecast):
    """
    Create new forecasts for a station (wind, humidity, and temperature)
    """
    try:
        forecast_map = {
            'wind': station_forecast.forecast.wind,
            'humidity': station_forecast.forecast.humidity,
            'temperature': station_forecast.forecast.temperature
        }

        async with database.SQLConnection() as db:
            for forecast_type, forecast_data in forecast_map.items():
                if forecast_data:
                    await db.execute_query(
                        stations_queries.CREATE_FORECAST,
                        (
                            station_forecast.date,
                            station_forecast.station_code,
                            forecast_type,
                            forecast_data.value,
                            forecast_data.unit
                        )
                    )

    except Exception as er:
        raise er

    return station_forecast


async def srv_get_stations(
    city: Optional[str] = None,
    page: Optional[int] = 1,
    limit: Optional[int] = None,
    sort: Optional[str] = "code",
    sort_order: Optional[str] = "ASC"
) -> List[dict]:
    """
    Retrieve stations from the database, optionally filtered by city, with pagination and sorting.
    """
    if limit is None:
        limit = 50

    sort, sort_order = utils.validate_sorting_parameters(sort, sort_order)

    final_query, params = utils.build_stations_query(city, page, limit, sort, sort_order)

    try:
        async with database.SQLConnection() as db:
            return await db.execute_query(final_query, params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


async def srv_create_station(station: Station):
    try:
        async with database.SQLConnection() as db:
            await db.execute_query(
                stations_queries.INSERT_STATION,
                (station.city, station.latitude, station.longitude, station.installation_date)
            )
    except IntegrityError as er:
        raise HTTPException(status_code=409, detail=f"Station with code '{station.code}' already exists")
    except Exception as er:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
    return station


async def srv_update_station(code: int, station_update: StationUpdate):
    """
    Update an existing station by its city name.
    """
    try:
        fields_to_update = utils.validate_station_update_fields(station_update)
        query, params = utils.update_station_in_db(code, fields_to_update)
        try:
            async with database.SQLConnection() as db:
                await db.execute_query(query, params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the station: {str(e)}")

        return {"message": "Station updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


async def srv_delete_station(code: str):
    """
    Delete an existing station by its city name.
    """
    try:
        async with database.SQLConnection() as db:
            await db.execute_query(stations_queries.DELETE_STATION, (code,))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Cannot delete station: associated records exist in other tables.")
    except Exception as er:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": "Station deleted"}


async def srv_get_station_data(station_code: int, request: StationDataRequest):
    """
    Retrieve meteorological data for a specific station based on filters and pagination.
    """
    if request.forecast:
        query, params = utils.get_forecast_for_next_day(station_code)
    else:
        query, params = utils.get_station_data_summary_or_paginated(station_code, request)
    
    try:
        async with database.SQLConnection() as db:
            results = await db.execute_query(query, params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving data: {str(e)}")
    
    return results

async def srv_insert_batch_data(batch_data: BatchData):
    """
    Create a batch of sensor data for a specific station.
    """
    try:
        async with database.SQLConnection() as db:
            errors = 0
            for sensor_data in batch_data.data:
                try:
                    await db.execute_query(
                        stations_queries.CREATE_BATCH_SENSOR_DATA,
                        (
                        sensor_data.sensor_id,
                        batch_data.station_code,
                        sensor_data.date,
                        sensor_data.type,
                        sensor_data.measurement,
                        sensor_data.unit
                    )
                )
                except Exception as e:
                    errors += 1
                    print(f"Error inserting sensor data: {e}. Sensor data: {sensor_data}")
                    continue

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if errors > 0:
        return {"message": f"{errors} errors occured, please check the logs"}
    else:
        return {"message": "Batch data created successfully"}