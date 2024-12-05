# utils/stations.py
from datetime import datetime, timedelta
from fastapi import HTTPException
import database.database as database
import database.queries.stations as stations_queries


def validate_station_update_fields(station_update):
    """
    Validate the fields in the station update request.
    """
    fields_to_update = station_update.model_dump(exclude_unset=True)
    if not fields_to_update:
        raise HTTPException(status_code=400, detail="No fields to update.")
    
    return fields_to_update


def update_station_in_db(station_code: int, fields_to_update: dict):
    """
    Update the station in the database.
    """
    update_parts = []
    params = []

    for field, value in fields_to_update.items():
        update_parts.append(f"{field} = %s")
        params.append(value)

    params.append(station_code)

    const query = `UPDATE stations SET ${updateParts.join(', ')} WHERE code = ?`;

    return query, params
    


def get_forecast_for_next_day(station_code: int):
    """
    Retrieve the forecast data for the next day for a specific station.
    """
    next_day = (datetime.now() + timedelta(days=1)).date()
    forecast_query = stations_queries.GET_FORECAST
    return forecast_query, (station_code, next_day)



def get_station_data_summary(station_code: int):
    """
    Retrieve the average values for each sensor type for a specific station.
    """
    try:
        with database.SQLConnection() as db:
            summary_query = stations_queries.GET_STATION_DATA_SUMMARY
            summary_result = db.execute_query(summary_query, (station_code,))
            return summary_result  # Return the summary of averages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving summary data: {str(e)}")


def build_paginated_query(station_code: int, request):
    """
    Construct the SQL query for paginated results based on the request parameters.
    """
    query = """SELECT * FROM sensors_data WHERE station_code = %s"""
    params = [station_code]

    if request.date_from:
        query += " AND date >= %s"
        params.append(request.date_from)
    if request.date_to:
        query += " AND date <= %s"
        params.append(request.date_to)

    if request.type:
        if request.type not in ["humidity", "temperature", "wind"]:
            raise HTTPException(status_code=400, detail="Invalid sensor type.")
        query += " AND type = %s"
        params.append(request.type)

    if request.sort in ["date", "type"]:
        query += f" ORDER BY {request.sort}"
    else:
        raise HTTPException(status_code=400, detail="Invalid sort parameter.")

    offset = (request.page - 1) * request.limit
    query += " LIMIT %s OFFSET %s"
    params.extend([request.limit, offset])

    return query, params


def get_station_data_summary_or_paginated(station_code: int, request):
    """
    Retrieve meteorological data for a specific station, either as a summary (average values) or paginated results.
    """
    if request.summary:
        query, params = stations_queries.GET_STATION_DATA_SUMMARY, (station_code,)
    else:
        query, params = build_paginated_query(station_code, request)
    
    return query, params



# def validate_sorting_parameters(sort: str, sort_order: str):
#     """
#     Validate the sorting parameters.
#     """
#     allowed_sort_columns = ["code", "installation_date"]
#     if sort not in allowed_sort_columns:
#         sort = "code"

#     if sort_order not in ["ASC", "DESC"]:
#         sort_order = "ASC"

#     return sort, sort_order


def build_stations_query(city: str, page: int, limit: int, sort: str, sort_order: str):
    """
    Build the SQL query for retrieving stations based on filters and pagination.
    """
    filter_condition = ""
    params = []

    if city:
        filter_condition = "WHERE city = %s"
        params.append(city)

    offset = (page - 1) * limit
    params.extend([limit, offset])

    final_query = f"""
        SELECT * FROM stations {filter_condition}
        ORDER BY {sort} {sort_order}
        LIMIT %s OFFSET %s;
    """

    return final_query, params
