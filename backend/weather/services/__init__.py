from collections import defaultdict
from datetime import datetime
from django.conf import settings
from ..clients import OpenWeatherClient


def get_forecast_for_location(*, location):
    if not location.latitude or not location.longitude:
        return []

    client = OpenWeatherClient()
    data = client.get_forecast(
        lat=location.latitude,
        lon=location.longitude,
        api_key=settings.WEATHER_API_KEY,
    )

    grouped_by_day = defaultdict(list)

    for item in data["list"]:
        date = datetime.fromtimestamp(item["dt"]).date()
        grouped_by_day[date].append(item)

    forecast = []

    for date, items in grouped_by_day.items():
        temps = [i["main"]["temp"] for i in items]
        descriptions = [i["weather"][0]["description"] for i in items]

        forecast.append({
            "date": date,
            "avg_temp": round(sum(temps) / len(temps), 1),
            "description": descriptions[0],
        })

    return forecast


def get_current_weather_for_location(*, location):
    if not location.latitude or not location.longitude:
        return None

    client = OpenWeatherClient()
    data = client.get_current_weather(
        lat=location.latitude,
        lon=location.longitude,
        api_key=settings.WEATHER_API_KEY,
    )

    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
    }


__all__ = [
    "get_forecast_for_location",
    "get_current_weather_for_location",
]
