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
