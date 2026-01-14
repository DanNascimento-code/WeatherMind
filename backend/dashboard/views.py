from django.shortcuts import render
from locations.selectors import get_default_location
from weather.services import (
    get_current_weather_for_location,
    get_forecast_for_location,
)

def index(request):
    location = get_default_location()
    weather = None
    forecast = []

    if location:
        weather = get_current_weather_for_location(location=location)
        forecast = get_forecast_for_location(location=location)

    context = {
        "location": location,
        "weather": weather,
        "forecast": forecast,
    }

    return render(request, "dashboard/index.html", context)

