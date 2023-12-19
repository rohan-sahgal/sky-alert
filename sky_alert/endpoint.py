from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
import datetime
from protocol import SunData

load_dotenv()

app = FastAPI()


@app.get('/healthz')
def healthz():
    return 'OK'

@app.get('/openweather_sun_data')
def sun_data(lat: int = 0, lon: int = 0) -> SunData:

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        "lat": lat,
        "lon": lon,
        "appid": os.environ["OPENWEATHER_API_KEY"]
    }

    api_url = os.environ["OPENWEATHER_API_URL"]

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
        print("Request Error")
        return 400
    
    except KeyError as e:
        print("Key Error")
        return 400
    
    except Exception as e:
        print("Internal Server Error")
        return 500

from typing import Dict
...
def get_sunrise_sunset_from_json(json_data: Dict[str, str]) -> SunData:

    sunrise = None
    sunset = None

    # Check for key existence at different levels
    if 'current' in json_data and isinstance(json_data['current'], dict):
        current_data = json_data['current']
        sunrise = current_data.get('sunrise')
        sunset = current_data.get('sunset')

    # Perform the necessary operations if sunrise and sunset are available
    if sunrise and sunset:
        sunrise_datetime = datetime.datetime.utcfromtimestamp(sunrise)
        sunset_datetime = datetime.datetime.utcfromtimestamp(sunset)
        return SunData(sunrise_datetime, sunset_datetime)

    else:
        
        # Handle missing keys or structure change
        # Perform necessary actions like setting default values or logging the issue
        print("Error: Change in API response - consult documentation")
        return None
