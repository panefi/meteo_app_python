from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes.stations import router as stations_router
from routes.sensors import router as sensors_router

app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Use specific origins like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

app = FastAPI(
    title="Meteorological App",
    description="This is a Meteorological Application API that provides various endpoints for managing stations and sensor data.",
    version="1.0.0"
)

app.include_router(stations_router, tags=["stations"])
app.include_router(sensors_router, tags=["sensors"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
