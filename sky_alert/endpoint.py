from fastapi import FastAPI
from dotenv import load_dotenv
from sky_alert.protocol import SunData, MoonData
from typing import Union
from sky_alert.openweather_service import OpenweatherService

load_dotenv()

app = FastAPI()

ows = OpenweatherService()


@app.get("/healthz")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def healthz() -> str:
    return "OK"


@app.get("/openweather_sun_data")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def sun_data(lat: str = "0", lon: str = "0") -> Union[SunData, int]:
    return ows.get_sunrise_sunset_from_json(lat=lat, lon=lon)


@app.get("/openweather_moon_data")  # type: ignore
def moon_data(lat: str = "0", lon: str = "0") -> Union[MoonData, int]:
    return ows.get_moonrise_moonset_from_json(lat=lat, lon=lon)
