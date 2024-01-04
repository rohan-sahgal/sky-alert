from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Type


class SunData(BaseModel):  # type: ignore
    """Class for sunrise and sunset times."""

    sunrise: datetime
    sunset: datetime


class MoonData(BaseModel):  # type: ignore
    """Class for moonrise and moonset times."""

    moonrise: datetime
    moonset: datetime
    moonphase: float


class CloudData(BaseModel):  # type: ignore
    """Class for cloud cover percentage over the next 24 hours (inclusive of current hour)"""

    cloud_cover: list[int]


class OpenweatherResponse(BaseModel):  # type: ignore
    """Class for generic responses"""

    status_code: int
    message: str

    @field_validator("status_code")
    def status_code_must_be_valid(cls: Type["OpenweatherResponse"], value: int) -> int:
        if not (100 <= value <= 599):
            raise ValueError("status_code must be a valid HTTP status code (100-599)")
        return value
