import os
import requests
from datetime import datetime, timedelta
from typing import Any
from sky_alert.protocol import SunData, MoonData, CloudData, OpenweatherResponse
from sky_alert.constants import HOURS_IN_DAY


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
            return OpenweatherResponse(
                status_code=res.status_code, message="Success..."
            )

        elif res.status_code == 401:
            return OpenweatherResponse(
                status_code=res.status_code, message="Error: Unauthorized"
            )

        elif res.status_code == 404:
            return OpenweatherResponse(
                status_code=res.status_code, message="Error: Resource not found"
            )

        else:
            return OpenweatherResponse(
                status_code=res.status_code, message="Error: Internal server error"
            )

    def get_sun_data_today(self, lat: str, lon: str) -> SunData:
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
            sunrise_datetime = datetime.utcfromtimestamp(sunrise)
            sunset_datetime = datetime.utcfromtimestamp(sunset)
            return SunData(sunrise=sunrise_datetime, sunset=sunset_datetime)

        raise KeyError(
            "Sunrise/sunset data from OpenWeather does not match expected format."
        )

    def get_sun_data_next_day(self, lat: str, lon: str) -> SunData:
        sunrise, sunset = None, None

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

        # Check for key existence at different levels
        if "daily" in json_data and isinstance(json_data["daily"], list):
            current_data = json_data["daily"]
            sunrise = current_data[1].get("sunrise")
            sunset = current_data[1].get("sunset")

        # Perform the necessary operations if sunrise and sunset are available
        if sunrise and sunset:
            sunrise_datetime = datetime.utcfromtimestamp(sunrise)
            sunset_datetime = datetime.utcfromtimestamp(sunset)
            return SunData(sunrise=sunrise_datetime, sunset=sunset_datetime)

        raise KeyError(
            "Sunrise/sunset data from OpenWeather does not match expected format."
        )

    def get_moon_data_today(self, lat: str, lon: str) -> MoonData:
        moonrise, moonset, moon_phase = None, None, None

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

        # Check for key existence at different levels
        if "daily" in json_data and isinstance(json_data["daily"], list):
            current_data = json_data["daily"][0]
            moonrise = current_data.get("moonrise")
            moonset = current_data.get("moonset")
            moon_phase = current_data.get("moon_phase")

        # Perform the necessary operations if moonrise/moonset/mooon phase are available
        if all((moonrise, moonset, moon_phase)) is not None:
            moonrise_datetime = datetime.utcfromtimestamp(moonrise)
            moonset_datetime = datetime.utcfromtimestamp(moonset)
            return MoonData(
                moonrise=moonrise_datetime,
                moonset=moonset_datetime,
                moonphase=moon_phase,
            )

        raise KeyError(
            "Moonrise/moonset/moon phase data from OpenWeather does not match expected format."
        )

    def get_moon_data_next_day(self, lat: str, lon: str) -> MoonData:
        moonrise, moonset, moon_phase = None, None, None

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

        # Check for key existence at different levels
        if "daily" in json_data and isinstance(json_data["daily"], list):
            current_data = json_data["daily"][1]
            moonrise = current_data.get("moonrise")
            moonset = current_data.get("moonset")
            moon_phase = current_data.get("moon_phase")

        # Perform the necessary operations if moonrise/moonset/mooon phase are available
        if all((moonrise, moonset, moon_phase)) is not None:
            moonrise_datetime = datetime.utcfromtimestamp(moonrise)
            moonset_datetime = datetime.utcfromtimestamp(moonset)
            return MoonData(
                moonrise=moonrise_datetime,
                moonset=moonset_datetime,
                moonphase=moon_phase,
            )

        raise KeyError(
            "Moonrise/moonset/moon phase data from OpenWeather does not match expected format."
        )

    def get_cloud_data_24_hours(self, lat: str, lon: str) -> CloudData:
        """Get the following 24 hours of cloud data (current hour inclusive)."""

        cloud_data = []

        self.update_most_recent_weather(lat=lat, lon=lon)

        json_data = self.most_recent_weather[(lat, lon)]

        # Check for key existence at different levels
        if "hourly" in json_data and isinstance(json_data["hourly"], list):
            current_data = json_data["hourly"]
            for i in range(HOURS_IN_DAY):
                current_hourly_cloud_data = current_data[i].get("clouds")
                if current_hourly_cloud_data is not None:
                    cloud_data.append(current_hourly_cloud_data)
                else:
                    raise KeyError(
                        "Cloud data from OpenWeather does not match expected format!"
                    )
            return CloudData(cloud_cover=cloud_data)

        raise KeyError("Cloud data from OpenWeather does not match expected format.")

    def update_most_recent_weather(self, lat: str, lon: str) -> None:
        if (lat, lon) not in self.most_recent_weather:
            res = self.populate_for_coord(lat=lat, lon=lon)

            if not (200 <= res.status_code <= 299):
                raise Exception(f"Error: {res.status_code}, {res.message}")

    def print_relevant_weather(self, lat: str, lon: str) -> None:
        sun_data_today = self.get_sun_data_today(lat=lat, lon=lon)
        sun_data_next_day = self.get_sun_data_next_day(lat=lat, lon=lon)
        moon_data_today = self.get_moon_data_today(lat=lat, lon=lon)
        moon_data_next_day = self.get_moon_data_next_day(lat=lat, lon=lon)
        cloud_data_24_hours = self.get_cloud_data_24_hours(lat=lat, lon=lon)
        print(sun_data_today)
        print(sun_data_next_day)
        print(moon_data_today)
        print(moon_data_next_day)
        print(cloud_data_24_hours)

    def check_next_24_hours(self, lat: str, lon: str) -> list[datetime]:
        intervals = []
        curr_dt = datetime.now()  # current datetime
        curr_dt_top_of_hour = curr_dt.replace(microsecond=0, second=0, minute=0)
        for i in range(0, HOURS_IN_DAY):
            hour_i = curr_dt_top_of_hour + timedelta(hours=i)
            if self.sun_criteria_valid(hour_i, lat, lon):
                # and self.moon_criteria_valid(hour_i, lat, lon) and self.cloud_criteria_valid(hour_i, lat, lon):
                intervals.append(hour_i)

        return intervals

    def sun_criteria_valid(self, hour: int, lat: str, lon: str):
        # Check if any time interval given falls between a sunset -> sunrise interval

        sun_data_today = self.get_sun_data_today(
            lat=lat, lon=lon
        )  # not necessarily today or tomorrow, generalize function to check any period
        sun_data_next_day = self.get_sun_data_next_day(lat=lat, lon=lon)

        sunrise_today = sun_data_today.sunrise
        sunset_today = sun_data_today.sunset
        sunrise_next_day = sun_data_next_day.sunrise
        sunset_next_day = sun_data_next_day.sunset

        return (
            (hour < sunrise_today)
            or (sunset_today < hour < sunrise_next_day)
            or (sunset_next_day < hour)
        )

    def moon_criteria_valid():
        return False
        # Check if falls between moonset -> moonrise interval
        # If check fails, check moon phase
        # If moon phase below threshold, return True
        # Else, return False
        # Else, return True

    def cloud_criteria_valid():
        return False
        # TODO: Rework such that we get new 24 hour range when the hour changes

        # Check if current time interval has cloud level below threshold
        # If so, return True
        # Else, return False
