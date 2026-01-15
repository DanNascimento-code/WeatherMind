from django.shortcuts import render
from core.services.weather_service import WeatherService, WeatherServiceError


def home(request):
    weather = None
    error = None

    if "city" in request.GET:
        city = request.GET.get("city")
        service = WeatherService()

        try:
            weather = service.get_current_weather(city)
        except WeatherServiceError as e:
            error = str(e)

    return render(request, "core/home.html", {
        "weather": weather,
        "error": error,
    })


