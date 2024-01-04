from fastapi import FastAPI
from dotenv import load_dotenv
from sky_alert.protocol import SunData, MoonData, CloudData
from typing import Union
from sky_alert.openweather_service import OpenweatherService
import json

load_dotenv()

app = FastAPI()

ows = OpenweatherService()


@app.get("/healthz")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def healthz() -> str:
    return "OK"


@app.get("/openweather_sun_data")  # type: ignore
def sun_data(lat: str = "0", lon: str = "0") -> Union[SunData, int]:
    return ows.get_sun_data(lat=lat, lon=lon)


@app.get("/openweather_moon_data")  # type: ignore
def moon_data(lat: str = "0", lon: str = "0") -> Union[MoonData, int]:
    return ows.get_moon_data(lat=lat, lon=lon)


@app.get("/openweather_cloud_data")  # type: ignore
def cloud_data(lat: str = "0", lon: str = "0") -> Union[CloudData, int]:
    return ows.get_cloud_data(lat=lat, lon=lon)


@app.get("/get_and_write_openweather_data_to_file")  # type: ignore
def get_and_write_openweather_data_to_file(lat: str = "0", lon: str = "0") -> bool:
    ows.update_most_recent_weather(lat=lat, lon=lon)
    with open("most_recent_weather.json", "w") as f:
        json.dump(ows.most_recent_weather[(lat, lon)], f)
        print("write to file succeeded")
    return True
