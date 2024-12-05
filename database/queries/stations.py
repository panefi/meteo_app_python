CREATE_FORECAST = """
INSERT INTO forecast (date, station_code, type, measurement, unit)
VALUES (%s, %s, %s, %s, %s);
"""

GET_STATIONS = """
SELECT * FROM stations
{filter_condition}
ORDER BY {sort_column} {sort_order}
LIMIT %s OFFSET %s;
"""

INSERT_STATION = """
INSERT INTO stations (city, latitude, longitude, installation_date)
VALUES (%s, %s, %s, %s);
"""

DELETE_STATION = """
DELETE FROM stations WHERE code = %s;
"""

GET_STATION_DATA = """
SELECT * FROM sensors_data WHERE station_code = %s
{filter_condition}
ORDER BY {sort_column} {sort_order}
LIMIT %s OFFSET %s;
"""

GET_FORECAST = """
SELECT *
FROM forecast
WHERE station_code = %s AND type IN ('humidity', 'temperature', 'wind') AND date = %s;
"""

GET_STATION_DATA_SUMMARY = """
SELECT type, AVG(measurement) AS average_value
FROM sensors_data
WHERE station_code = %s
GROUP BY type;
"""

CREATE_BATCH_SENSOR_DATA = """
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
VALUES (%s, %s, %s, %s, %s, %s)
"""
