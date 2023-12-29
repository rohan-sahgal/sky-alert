from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel


@dataclass
class SunData(BaseModel):
    """Class for sunrise and sunset times."""

    sunrise: datetime
    sunset: datetime


@dataclass
class MoonData(BaseModel):
    """Class for moonrise and moonset times."""

    moonrise: datetime
    moonset: datetime
    moonphase: float


@dataclass
class OpenweatherResponse(BaseModel):
    """Class for generic responses"""

    status_code: int
    message: str
