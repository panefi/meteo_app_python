CREATE DATABASE IF NOT EXISTS meteo;

USE meteo;

CREATE TABLE stations (
    code INT AUTO_INCREMENT PRIMARY KEY,        -- Auto-incrementing primary key
    city VARCHAR(100) NOT NULL,                 -- City where the station is located
    latitude DECIMAL(9, 6) NOT NULL,            -- Latitude of the station
    longitude DECIMAL(9, 6) NOT NULL,           -- Longitude of the station
    installation_date DATE NOT NULL             -- Date of installation
);

ALTER TABLE stations
ADD CONSTRAINT unique_city UNIQUE (city);


CREATE TABLE sensors (
    id CHAR(36) PRIMARY KEY,  -- Manually provided UUID (36 characters)
    station_code INT NOT NULL,  -- Must match the data type of `code` in stations
    type ENUM('temperature', 'humidity', 'wind') NOT NULL,  -- Only allows these values
    CONSTRAINT fk_station_code FOREIGN KEY (station_code) REFERENCES stations(code)
        ON DELETE RESTRICT  -- Prevent station deletion if sensors exist
);

CREATE TABLE sensors_data (
    sensor_id CHAR(36) NOT NULL,  -- References the sensor's UUID from the sensors table
    station_code INT NOT NULL,    -- References the station's code from the stations table
    date DATETIME NOT NULL,       -- Date and time of the measurement
    type ENUM('temperature', 'humidity', 'wind') NOT NULL,  -- Type of measurement
    measurement DECIMAL(10, 2) NOT NULL,  -- The measured value
    unit VARCHAR(10) NOT NULL,    -- Unit of measurement (e.g., °C, %, m/s)
    PRIMARY KEY (sensor_id, date)  -- Composite primary key: sensor and timestamp
);

ALTER TABLE sensors_data 
ADD CONSTRAINT fk_sensor_id FOREIGN KEY (sensor_id) REFERENCES sensors(id)
    ON DELETE RESTRICT;

ALTER TABLE sensors_data 
ADD CONSTRAINT chk_unit2 CHECK (
    (type = 'wind' AND unit = 'm/s') OR
    (type = 'temperature' AND unit = 'Celsius') OR
    (type = 'humidity' AND unit = '%')
);

CREATE TABLE forecast (
    date DATETIME NOT NULL,             -- Date and time of the forecast
    station_code INT NOT NULL,          -- References the station's code from the stations table
    type ENUM('temperature', 'humidity', 'wind') NOT NULL,  -- Type of forecast
    measurement DECIMAL(10, 2) NOT NULL,  -- The forecasted value
    unit VARCHAR(10) NOT NULL           -- Unit of measurement (e.g., °C, %, m/s)
);

ALTER TABLE forecast
ADD PRIMARY KEY (date, station_code, type);

ALTER TABLE forecast
ADD CONSTRAINT chk_unit1 CHECK (
    (type = 'wind' AND unit = 'm/s') OR
    (type = 'temperature' AND unit = 'Celsius') OR
    (type = 'humidity' AND unit = '%')
);

ALTER TABLE forecast
ADD CONSTRAINT fk_forecast_station_code
FOREIGN KEY (station_code) REFERENCES stations(code)
ON DELETE RESTRICT;
