# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient and pkg-config
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port 8000 to access the Python app
EXPOSE 8000

# Set the environment variables for the MySQL connection
ENV DB_HOST=mysql
ENV DB_PORT=3306
ENV DB_USER=test_user
ENV DB_PASSWORD=TestProject123!
ENV DB_NAME=meteo

# Set another environment variables
ENV BASE_URL=http://127.0.0.1:8000/api

# Command to run your application
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
