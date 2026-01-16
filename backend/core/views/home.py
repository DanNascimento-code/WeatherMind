from django.shortcuts import render
from weather.models import WeatherRecord
from core.services.climate_service import ClimateService
from core.exceptions.climate import ClimateServiceError


def home(request):
    city = request.GET.get("city")
    weather_data = None
    error_message = None
    history = []

    if city:
        service = ClimateService()

        try:
            weather_data = service.get_weather_by_city(city)
            
            # Salvar o registro no banco de dados
            WeatherRecord.objects.create(
                city=weather_data["city"],
                country=weather_data.get("country", ""),
                temperature=weather_data["temperature"],
                feels_like=weather_data["feels_like"],
                humidity=weather_data["humidity"],
                condition=weather_data["condition"],
            )
        except ClimateServiceError as error:
            error_message = str(error)
        
        # Buscar histórico apenas da cidade consultada
        history = WeatherRecord.objects.filter(
            city__iexact=city
        ).order_by('-created_at')[:10]

    context = {
        "weather": weather_data,
        "error": error_message,
        "history": history,
    }

    return render(request, "core/home.html", context)






