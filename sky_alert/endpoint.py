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

@app.get('/sundata')
def sun_data(lat=0, lon=0):

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

    sundata = SunData(sunrise, sunset)

    print(sundata)

    return sundata

