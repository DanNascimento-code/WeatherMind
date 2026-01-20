
import requests
from django.conf import settings
from weather.models import WeatherRecord
from typing import List
from django.utils import timezone
from datetime import timedelta


def get_weather_by_city(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }

    response = requests.get(url, params=params)
    data = response.json()

    return {
        "city": data["name"].strip().lower(),
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"] if data.get("weather") else "indefinido",
    }



def save_weather_record(data):
    
    WeatherRecord.objects.create(
        city=data["city"],
        country=data["country"],
        temperature=data["temperature"],
        feels_like=data["feels_like"],
        humidity=data["humidity"],
        condition=data["condition"],
    )


def fetch_weather(city):
  
    weather_data = get_weather_by_city(city)
    save_weather_record(weather_data)

    return weather_data



def get_recent_temperatures_for_city(
    city: str,
    hours: int = 24,
) -> List[float]:
    """
    Retorna temperaturas registradas nas últimas X horas.
    """

    since = timezone.now() - timedelta(hours=hours)

    records = (
        WeatherRecord.objects
        .filter(city=city.strip().lower(), created_at__gte=since)
        .order_by("created_at")
    )

    return [record.temperature for record in records]


