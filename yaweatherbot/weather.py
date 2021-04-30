import requests
from consts import API_URL, TEMPLATE
from config import API_KEY


def get_weather_forecast(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    resp = requests.get(API_URL, params=params)
    if not resp.ok:
        raise ValueError("Something went wrong, try another time")
    forecast = resp.json()['main']
    temp_max = forecast['temp_max']
    temp_min = forecast['temp_min']
    feels_like = forecast['feels_like']
    precipitation = resp.json()['weather'][0]['main'] + ":" + (resp.json()['weather'][0].get('description') or "")
    return TEMPLATE.format(temp_min, temp_max, feels_like, precipitation)
