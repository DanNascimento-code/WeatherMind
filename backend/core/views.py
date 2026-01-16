from django.shortcuts import render
from weather.services.openweather import fetch_weather
from weather.services.history import get_city_history

def home(request):
    city = request.GET.get("city")

    context = {}

    if city:
        weather = fetch_weather(city)
        history = get_city_history(city)

        context["weather"] = weather
        context["history"] = history

    return render(request, "core/home.html", context)


    