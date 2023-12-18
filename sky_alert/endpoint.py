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
def sun_data(lat: int = 0, lon: int = 0):

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        "lat": lat,
        "lon": lon,
        "appid": os.environ["OPENWEATHER_API_KEY"]
    }
    
    res = requests.get(os.environ["OPENWEATHER_API_URL"], params=params, headers=headers)

    sunrise = datetime.datetime.utcfromtimestamp(res.json()['current']['sunrise'])
    sunset = datetime.datetime.utcfromtimestamp(res.json()['current']['sunset'])

    sun_data = SunData(sunrise, sunset)

    return sundata

