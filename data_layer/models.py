from pydantic import BaseModel


class GPS(BaseModel):
    timestamp: float
    latitude: float
    longitude: float
    elevation: float
    accuracy: float
    bearing: float
    speed_meters_per_second: float
    satellites: int
    hdop: float
    vdop: float
    pdop: float
    distance_meters: float
    elapsed_time_seconds: float
