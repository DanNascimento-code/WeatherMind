from django.http import JsonResponse
from django.views.decorators.http import require_GET

from weather.services.insights import build_temperature_insight
from weather.services.history import get_city_history


@require_GET
def temperature_insight_view(request):
    """
    Provides temperature insights for a given city based on historical weather data.

    This view fetches recent temperature records for the specified city,
    generates a detailed analysis, and returns it as a JSON response.
    """
    city = request.GET.get("city")

    if not city:
        return JsonResponse(
            {"error": "Parâmetro 'city' é obrigatório."},
            status=400,
        )

    try:
        # Fetch temperature history from the database
        history_records = get_city_history(city, limit=10)
        if not history_records:
            return JsonResponse(
                {
                    "error": f"Não há dados históricos de temperatura para a cidade de '{city}'.",
                },
                status=404,
            )

        # Extract temperature values from records
        temperatures = [record.temperature for record in history_records]

        # Build the temperature insight
        insight = build_temperature_insight(temperatures)

        return JsonResponse(
            {
                "city": city,
                "insight": insight,
            },
            status=200,
        )

    except Exception as exc:
        # Log the exception details for debugging purposes
        # logger.error(f"Error generating temperature insight for {city}: {exc}")
        return JsonResponse(
            {"error": "Ocorreu um erro inesperado ao gerar a análise de temperatura."},
            status=500,
        )
