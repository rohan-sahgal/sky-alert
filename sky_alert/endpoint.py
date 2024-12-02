from fastapi import FastAPI
from dotenv import load_dotenv
from sky_alert.protocol import SunData, MoonData, CloudData
from typing import Union
from sky_alert.openweather_service import OpenweatherService
import json
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig("logging.ini")

# Create a logger
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

ows = OpenweatherService()


@app.get("/healthz")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def healthz() -> str:
    return "OK"


@app.get("/openweather_sun_data")  # type: ignore
def sun_data(lat: str = "0", lon: str = "0") -> Union[SunData, int]:
    logger.info("Getting sun data...")
    return ows.get_sun_data(lat=lat, lon=lon)


@app.get("/openweather_moon_data")  # type: ignore
def moon_data(lat: str = "0", lon: str = "0") -> Union[MoonData, int]:
    logger.info("Getting moon data...")
    return ows.get_moon_data(lat=lat, lon=lon)


@app.get("/openweather_cloud_data")  # type: ignore
def cloud_data(lat: str = "0", lon: str = "0") -> Union[CloudData, int]:
    logger.info("Getting cloud data...")
    return ows.get_cloud_data(lat=lat, lon=lon)


@app.get("/get_and_write_openweather_data_to_file")  # type: ignore
def get_and_write_openweather_data_to_file(lat: str = "0", lon: str = "0") -> bool:
    logger.info("writing openweather data to file...")
    ows.update_most_recent_weather(lat=lat, lon=lon)
    with open("most_recent_weather.json", "w") as f:
        json.dump(ows.most_recent_weather[(lat, lon)], f)
        print("write to file succeeded")
    return True
