import requests
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import datetime
from sky_alert.protocol import SunData
from typing import Any, Union

load_dotenv()

app = FastAPI()


@app.get("/healthz")  # type: ignore
def healthz() -> str:
    return "OK"


@app.get("/openweather_sun_data")  # type: ignore
def sun_data(lat: str = "0", lon: str = "0") -> Union[SunData, int]:
    headers = {
        "Content-Type": "application/json",
    }

    params: dict[str, str] = {
        "lat": lat,
        "lon": lon,
        "appid": os.environ["OPENWEATHER_API_KEY"],
    }

    api_url = os.environ["OPENWEATHER_API_URL1"]

    try:
        res = requests.get(api_url, params=params, headers=headers)

        if 200 <= res.status_code <= 299:
            json_data = res.json()
            sun_data = get_sunrise_sunset_from_json(json_data)
            return sun_data

        elif res.status_code == 401:
            print("error: Unauthorized")
            return 401

        elif res.status_code == 404:
            print("error: Resource not found")
            return 404

        else:
            print("error: Internal Server Error")
            return 500

    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return 400

    except KeyError as e:
        print(f"Key Error: {e}")
        return 400

    except Exception as e:
        print(f"Internal Server Error: {e}")
        return 500


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
