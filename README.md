
# Meteorological Application Setup

## Docker Setup

This repository contains the setup for a meteorological backend application using MySQL and FastAPI. To begin, clone the repository using the following command:

```bash
git clone https://github.com/panefi/meteo_app_python.git
```

Follow the instructions below to set up the database and populate it with fake data.

## Docker Setup

The easiest way to run this application is through Docker, which will set up both the FastAPI application and the MySQL database in separate containers.

### Prerequisites
- Docker

### Step 1: Build and Start the Docker Containers

1. **Build the Docker containers**:
   ```bash
   docker-compose build
   ```

2. **Start the containers**:
   ```bash
   docker-compose up
   ```

   This will start both the FastAPI application and the MySQL database in separate containers.

### Step 2: Access the API Documentation

Once the containers are up and running, you can access the FastAPI application. 

The FastAPI application provides an interactive Swagger page for API documentation. You can access it by navigating to:
```
http://127.0.0.1:8000/docs
```

This page gives a detailed overview of the available API endpoints for managing stations and sensors, along with allowed queries and request body structures.

### Step 3: Stopping the Containers

To stop the running containers, use:
```bash
docker-compose down
```

## Local Development Setup

If you prefer to run the application on your local machine without Docker, follow the steps below.

### Prerequisites
- MySQL Server installed
- Python 3.12+ installed
- Required Python packages (listed in `requirements.txt`)

Note: **Virtual Environment (`venv`) is not required when using Docker**. However, for local development, it is recommended to use a virtual environment for package management.

### Step 1: Set Up the MySQL Database

1. Connect to your MySQL database:
   ```bash
   mysql -u [your_username] -p
   ```
   Enter your MySQL password when prompted.

2. Run the `setup.sql` file to create the `meteo` database and the necessary tables:
   ```bash
   source path/to/setup.sql;
   ```

3. Populate the `stations` and `sensors` tables with fake data by running `b_fake_data.sql`:
   ```bash
   source path/to/b_fake_data.sql;
   ```

4. Run the `c_generate_sensor_data.sql` file to generate sensor data for the existing sensors:
   ```bash
   source path/to/c_generate_sensor_data.sql;
   ```

### Step 2: Set Up the Python Environment

1. Clone the repository to your local machine.

2. Create a virtual environment in the project directory (optional but recommended for local development):
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - On Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure the Environment Variables

Create a `.env` file in the project root with your database credentials and API base URL. Use the following template:
```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=[USER_PASSWORD]
DB_PORT=3306
DB_NAME=meteo

BASE_URL=http://127.0.0.1:8000/api
```

### Step 4: Run the FastAPI Application

Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

### Step 5: Access the API

Once the FastAPI application is running, access the API by visiting:
```
http://127.0.0.1:8000/docs
```

---
