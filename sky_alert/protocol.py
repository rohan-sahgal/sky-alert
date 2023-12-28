from dataclasses import dataclass
import datetime


@dataclass
class SunData:
    """Class for sunrise and sunset times."""

    sunrise: datetime.datetime
    sunset: datetime.datetime


@dataclass
class MoonData:
    """Class for moonrise and moonset times."""

    moonrise: datetime.datetime
    moonset: datetime.datetime
    moonphase: float


@dataclass
class CloudData:
    """Class for cloud cover percentage over the next 24 hours (inclusive of current hour)"""

    cloud_cover: list[int]


@dataclass
class OpenweatherResponse:
    """Class for generic responses"""

    status_code: int
    message: str
