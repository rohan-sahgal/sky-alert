from dataclasses import dataclass
import datetime

@dataclass
class SunData:
    """Class for sunrise and sunset times."""
    sunrise: datetime.datetime
    sunset: datetime.datetime
