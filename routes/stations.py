from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Body
from services.stations import srv_create_station_forecast, srv_get_stations, srv_create_station, srv_update_station, srv_delete_station, srv_get_station_data, srv_insert_batch_data
from models.stations import StationForecast, StationQueryParams, Station, StationUpdate, StationDataRequest, BatchData


router = APIRouter(prefix="/api/stations")


@router.post(
    "/forecast",
    summary="Create a station forecast",
    description="Create a forecast for wind, humidity, and temperature for a given station on a specific date.",
    response_description="Forecast created successfully.",
    responses={
        200: {
            "description": "Forecast created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "date": "2024-10-15",
                        "station_code": 1,
                        "forecast": {
                            "wind": {"value": 11, "unit": "m/s"},
                            "humidity": {"value": 60, "unit": "%"},
                            "temperature": {"value": 25, "unit": "Celsius"}
                        }
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
async def create_station_forecast(body: StationForecast):
    """
    Create a forecast for a specific station on a given date.

    The request body should be structured as follows:
    {
        "date": <str>,  // The date for the forecast in YYYY-MM-DD format
        "station_code": <int>,  // The code of the station
        "forecast": {
            "wind": {
                "value": <float>,  // Wind speed value
                "unit": "m/s"
            },
            "humidity": {
                "value": <float>,  // Humidity percentage
                "unit": "%"
            },
            "temperature": {
                "value": <float>,  // Temperature value
                "unit": "Celsius"
            }
        }
    }

    - `date`: The date for which the forecast is being created.
    - `station_code`: The unique code identifying the station.
    - `forecast`: An object containing forecast details for:
      - `wind`: Wind speed and its unit.
      - `humidity`: Humidity level and its unit.
      - `temperature`: Temperature value and its unit.
    """
    try:
        return await srv_create_station_forecast(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    summary="Get stations",
    description="Get all stations with pagination and sorting or the station for a specific city.",
    responses={
        200: {
            "description": "Stations retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "code": 1,
                            "city": "City 1",
                            "latitude": 10.0,
                            "longitude": 20.0,
                            "installation_date": "2024-08-15"
                        },
                        {
                            "code": 2,
                            "city": "City 2",
                            "latitude": 30.0,
                            "longitude": 40.0,
                            "installation_date": "2024-08-15"
                        }
                    ]
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
async def get_stations(params: StationQueryParams = Depends()):
    """
    Get all stations with pagination and sorting or the station for a specific city.

    - If the `city` is provided as a query parameter, the details for that specific station are retrieved.
    - If `city` is not provided, default pagination is applied.
    - Additional query parameters include:
      - `page`: The page number for pagination.
      - `limit`: The number of records per page.
      - `offset`: The number of records to skip before starting to collect the result set.
      - `sort`: The field to sort by (e.g., 'name', 'city').
      - `sort_order`: The order of sorting ('ASC' for ascending, 'DESC' for descending).
    """
    try:
        stations = await srv_get_stations(city=params.city, page=params.page, limit=params.limit, sort=params.sort, sort_order=params.sort_order)
        return stations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/",
    summary="Create a station",
    description="Create a new station.",
    response_description="Station created successfully.",
    responses={
        201: {
            "description": "Station created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "code": 1,
                        "name": "Station 1",
                        "city": "City 1",
                        "latitude": 10.0,
                        "longitude": 20.0
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
async def create_station(station: Station):
    new_station = await srv_create_station(station)
    return new_station


@router.put(
    "/{code}",
    summary="Update a station",
    description="Update an existing station by its city.",
    response_description="Station updated successfully.",
    responses={
        200: {
            "description": "Station updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "city": "City 1",
                        "latitude": 10.0,
                        "longitude": 20.0,
                        "installation_date": "2024-10-15"
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
async def update_station(code: int, station_update: StationUpdate):
    """
    Update an existing station by its code.

    The following fields in the request body are optional:
    - `city`: The city where the station is located.
    - `latitude`: The latitude coordinate of the station.
    - `longitude`: The longitude coordinate of the station.
    - `installation_date`: The date when the station was installed.
    """
    updated_station = await srv_update_station(code, station_update)
    return updated_station


@router.delete(
    "/{code}",
    summary="Delete a station",
    description="Delete an existing station by its code.",
    response_description="Station deleted successfully.",
    responses={
        200: {
            "description": "Station deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Station deleted successfully"
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
async def delete_station(code: str):
    """
    Delete an existing station by its code.
    """
    deleted_station = await srv_delete_station(code)
    return deleted_station


@router.post(
    "/{station_code}",
    summary="Get station data",
    description="Get the meteorological data for a specific station based on filters and pagination.",
    responses={
        200: {
            "description": "Meteorological data retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "date_from": "2022-10-15",
                            "date_to": "2024-10-16",
                            "type": "wind",
                            "page": 1,
                            "limit": 50,
                            "sort": "date",
                            "forecast": False,
                            "summary": True
                        }
                    ]
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
async def get_station_data(station_code: int,
        request: StationDataRequest = Body(
        ..., 
        description="Request body containing filters for retrieving station data. "
                    "Fields include:\n"
                    "- `date_from`: Start date for data retrieval.\n"
                    "- `date_to`: End date for data retrieval.\n"
                    "- `forecast`: Boolean indicating if forecast data should be retrieved.\n"
                    "- `summary`: Boolean: When true the average properties for the given period are retrieved. "
                                  "When false all data are retrieved and pagination is applied.\n"
                    "- `type`: Type of data to retrieve (e.g., 'temperature', 'humidity', 'wind').\n"
                    "- `page`: Page number for pagination.\n"
                    "- `limit`: Number of records per page.\n"
                    "- `sort`: Field to sort by (e.g., 'date', 'type').\n"
    )):
    """
    Retrieve meteorological data for a specific station based on filters and pagination.
    """
    try:
        stations = await srv_get_station_data(station_code, request)
        return stations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{station_code}/batch",
    summary="Receive batch data",
    description="Receive a batch of sensor data for a specific station.",
    response_description="Batch data received successfully.",
    responses={
        200: {
            "description": "Batch data received successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Batch data is being processed."
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
async def receive_batch_data(station_code: int, batch_data: BatchData):
    """
    Receive a batch of sensor data for a specific station.

    The request body should be structured as follows:
    {
      "station_code": <int>,
      "data": [
        {
          "sensor_id": <str>,
          "date": <str>,
          "type": <str>,
          "measurement": <float>,
          "unit": <str>
        },
        ...
      ]
    }

    - `station_code`: The code of the station to which the data belongs.
    - `data`: A list of sensor data entries, each containing:
      - `sensor_id`: The identifier of the sensor.
      - `date`: The date and time of the measurement in ISO 8601 format.
      - `type`: The type of measurement (wind, temperature, humidity).
      - `measurement`: The measured value.
      - `unit`: The unit of the measurement (m/s, Celsius, %).
    """
    if batch_data.station_code != station_code:
        raise HTTPException(status_code=400, detail="Station code mismatch.")

    return await srv_insert_batch_data(batch_data)