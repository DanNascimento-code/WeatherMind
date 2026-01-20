from django.http import JsonResponse
from django.views.decorators.http import require_GET

from weather.services.insights import build_temperature_insight
from weather.services.openweather import get_current_weather_for_city
from weather.services.history import get_temperature_history_for_city

@require_GET
def temperature_insight_view(request):
    city = request.GET.get("city")

    if not city:
        return JsonResponse(
            {"error": "Parâmetro 'city' é obrigatório."},
            status=400,
        )

    try:
        # Histórico de temperaturas (ex: últimas horas/dias)
        temperatures = get_temperature_history_for_city(city)

        insight = build_temperature_insight(temperatures)

        return JsonResponse(
            {
                "city": city,
                "insight": insight,
            },
            status=200,
        )

    except Exception as exc:
        return JsonResponse(
            {"error": str(exc)},
            status=500,
        )
