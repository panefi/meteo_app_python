CREATE_SENSOR_DATA = """
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
VALUES (%s, %s, %s, %s, %s, %s)
"""