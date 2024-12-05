USE meteo;

-- Insert random sensor data for existing sensors from the sensors table
-- We are generating sensor data with random timestamps for each sensor

-- Insert data for temperature sensors
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, NOW(), 'temperature', ROUND(RAND() * (35.0 - 20.0) + 20.0, 2), 'Celsius' FROM sensors WHERE type = 'temperature';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 1 MINUTE), 'temperature', ROUND(RAND() * (35.0 - 20.0) + 20.0, 2), 'Celsius' FROM sensors WHERE type = 'temperature';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 2 MINUTE), 'temperature', ROUND(RAND() * (35.0 - 20.0) + 20.0, 2), 'Celsius' FROM sensors WHERE type = 'temperature';

-- Insert data for humidity sensors
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, NOW(), 'humidity', ROUND(RAND() * (90.0 - 30.0) + 30.0, 2), '%' FROM sensors WHERE type = 'humidity';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 1 MINUTE), 'humidity', ROUND(RAND() * (90.0 - 30.0) + 30.0, 2), '%' FROM sensors WHERE type = 'humidity';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 2 MINUTE), 'humidity', ROUND(RAND() * (90.0 - 30.0) + 30.0, 2), '%' FROM sensors WHERE type = 'humidity';

-- Insert data for wind sensors
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, NOW(), 'wind', ROUND(RAND() * (15.0 - 0.0) + 0.0, 2), 'm/s' FROM sensors WHERE type = 'wind';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 1 MINUTE), 'wind', ROUND(RAND() * (15.0 - 0.0) + 0.0, 2), 'm/s' FROM sensors WHERE type = 'wind';
INSERT INTO sensors_data (sensor_id, station_code, date, type, measurement, unit)
SELECT id, station_code, DATE_ADD(NOW(), INTERVAL 2 MINUTE), 'wind', ROUND(RAND() * (15.0 - 0.0) + 0.0, 2), 'm/s' FROM sensors WHERE type = 'wind';
