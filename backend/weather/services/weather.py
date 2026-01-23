from collections import defaultdict
from datetime import datetime
from django.conf import settings
from weather.clients import OpenWeatherClient


def get_forecast_for_location(*, location):
    """
    Fetch and format weather forecast data for a given location.
    
    Args:
        location: Location object with latitude and longitude
        
    Returns:
        List of forecast dictionaries with date, avg_temp, and description
    """
    if not location.latitude or not location.longitude:
        return []

    client = OpenWeatherClient()
    data = client.get_forecast(
        lat=location.latitude,
        lon=location.longitude,
        api_key=settings.OPENWEATHER_API_KEY,
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
    """
    Fetch current weather conditions for a given location.
    
    Args:
        location: Location object with latitude and longitude
        
    Returns:
        Dictionary with temperature, feels_like, and description, or None if location missing coordinates
    """
    if not location.latitude or not location.longitude:
        return None

    client = OpenWeatherClient()
    data = client.get_current_weather(
        lat=location.latitude,
        lon=location.longitude,
        api_key=settings.OPENWEATHER_API_KEY,
    )

    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data.get("wind", {}).get("speed", 0),
        "description": data["weather"][0]["description"],
    }
