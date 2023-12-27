import datetime
from typing import Any
from sky_alert.protocol import SunData, MoonData


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


def get_moonrise_moonset_from_json(json_data: dict[str, Any]) -> MoonData:
    moonrise, moonset, moonphase = None, None, None

    # Check for key existence at different levels
    if "current" in json_data and isinstance(json_data["current"], dict):
        current_data = json_data["daily"][0]
        moonrise = current_data.get("moonrise")
        moonset = current_data.get("moonset")
        moonphase = current_data.get("moon_phase")

    # Perform the necessary operations if moonrise and moonset are available
    if moonrise and moonset and moonphase:
        moonrise_datetime = datetime.datetime.utcfromtimestamp(moonrise)
        moonset_datetime = datetime.datetime.utcfromtimestamp(moonset)
        return MoonData(moonrise_datetime, moonset_datetime, moonphase)

        # Handle missing keys or structure change
        # Perform necessary actions like setting default values or logging the issue
    raise KeyError(
        "Moonrise/moonset/moonphase data from OpenWeather does not match expected format."
    )
