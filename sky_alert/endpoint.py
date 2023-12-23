import requests
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import datetime
from sky_alert.protocol import SunData
from typing import Any, Union
from fastapi import HTTPException

load_dotenv()

app = FastAPI()


@app.get("/healthz")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def healthz() -> str:
    return "OK"


@app.get("/openweather_sun_data")  # type: ignore
# https://stackoverflow.com/questions/75347974/mypy-untyped-decorator-makes-function-main-untyped-for-fastapi-routes
def sun_data(lat: str = "0", lon: str = "0") -> Union[SunData, int]:
    headers = {
        "Content-Type": "application/json",
    }

    params: dict[str, str] = {
        "lat": lat,
        "lon": lon,
        "appid": os.environ["OPENWEATHER_API_KEY"],
    }

    api_url = os.environ["OPENWEATHER_API_URL"]

    try:
        res = requests.get(api_url, params=params, headers=headers)

        if 200 <= res.status_code <= 299:
            json_data = res.json()
            sun_data = get_sunrise_sunset_from_json(json_data)
            return sun_data

        elif res.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized access.")
        elif res.status_code == 404:
            raise HTTPException(status_code=404, detail="Resource not found.")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error.")

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request Error: {e}")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Key Error: {e}")


def get_sunrise_sunset_from_json(json_data: dict[str, Any]) -> SunData:
    sunrise, sunset = None, None

    # Check for key existence at different levels
    if "current" in json_data and isinstance(json_data["current"], dict):
        current_data = json_data["current"]
        sunrise = current_data.get("sunrise")
        sunset = current_data.get("sunset")

    # Perform the necessary operations if sunrise and sunset are available
    if sunrise and sunset:
        sunrise_datetime = datetime.datetime.utcfromtimestamp(sunrise)
        sunset_datetime = datetime.datetime.utcfromtimestamp(sunset)
        return SunData(sunrise_datetime, sunset_datetime)

        # Handle missing keys or structure change
        # Perform necessary actions like setting default values or logging the issue
    raise KeyError(
        "Sunrise/sunset data from OpenWeather does not match expected format."
    )
