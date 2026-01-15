from django.shortcuts import render

from core.services.climate_service import ClimateService
from core.exceptions.climate import ClimateServiceError


def home(request):
    city = request.GET.get("city")
    weather_data = None
    error_message = None

    if city:
        service = ClimateService()

        try:
            weather_data = service.get_weather_by_city(city)
        except ClimateServiceError as error:
            error_message = str(error)

    context = {
        "weather": weather_data,
        "error": error_message,
    }

    return render(request, "core/home.html", context)



