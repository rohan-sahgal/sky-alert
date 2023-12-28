import os
import requests
import datetime
from typing import Any
from sky_alert.protocol import SunData, MoonData, OpenweatherResponse

from dotenv import load_dotenv

load_dotenv()


class OpenweatherService:
    def __init__(self) -> None:
        self.most_recent_weather: dict[tuple[str, str], Any] = {}

    def populate_for_coord(self, lat: str, lon: str) -> OpenweatherResponse:
        headers = {
            "Content-Type": "application/json",
        }

        params: dict[str, str] = {
            "lat": lat,
            "lon": lon,
            "appid": os.environ["OPENWEATHER_API_KEY"],
        }

        api_url = os.environ["OPENWEATHER_API_URL"]

        res = requests.get(api_url, params=params, headers=headers)

        if 200 <= res.status_code <= 299:
            json_data = res.json()
            self.most_recent_weather[(lat, lon)] = json_data
            return OpenweatherResponse(res.status_code, "Success...")

        elif res.status_code == 401:
            return OpenweatherResponse(res.status_code, "Error: Unauthorized")

        elif res.status_code == 404:
            return OpenweatherResponse(res.status_code, "Error: Resource not found")

        else:
            return OpenweatherResponse(res.status_code, "Error: Internal server error")

    def get_sunrise_sunset_from_json(self, lat: str, lon: str) -> SunData:
        sunrise, sunset = None, None

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

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

        raise KeyError(
            "Sunrise/sunset data from OpenWeather does not match expected format."
        )

    def get_moonrise_moonset_from_json(self, lat: str, lon: str) -> MoonData:
        moonrise, moonset, moon_phase = None, None, None

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

        # Check for key existence at different levels
        if "current" in json_data and isinstance(json_data["current"], dict):
            current_data = json_data["daily"][0]
            moonrise = current_data.get("moonrise")
            moonset = current_data.get("moonset")
            moon_phase = current_data.get("moon_phase")

        # Perform the necessary operations if moonrise/moonset/mooon phase are available
        if moonrise and moonset and moon_phase:
            moonrise_datetime = datetime.datetime.utcfromtimestamp(moonrise)
            moonset_datetime = datetime.datetime.utcfromtimestamp(moonset)
            return MoonData(moonrise_datetime, moonset_datetime, moon_phase)

        raise KeyError(
            "Moonrise/moonset/moon phase data from OpenWeather does not match expected format."
        )

    def update_most_recent_weather(self, lat: str, lon: str) -> None:
        if (lat, lon) not in self.most_recent_weather:
            res = self.populate_for_coord(lat=lat, lon=lon)

            if not (200 <= res.status_code <= 299):
                raise Exception(f"Error: {res.status_code}, {res.message}")
