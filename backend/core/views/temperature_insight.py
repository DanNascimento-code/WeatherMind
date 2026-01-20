from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from weather.services.weather_service import (
    fetch_weather,
    get_recent_temperatures_for_city,
)
from weather.services.insights.temperature_insight import (
    build_temperature_insight,
)


@api_view(["GET"])
def temperature_insight_view(request):
    city = request.query_params.get("city")

    if not city:
        return Response(
            {"error": "Parâmetro 'city' é obrigatório"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Garante dado atualizado e persistido
    fetch_weather(city)

    temperatures = get_recent_temperatures_for_city(city)

    if len(temperatures) < 2:
        return Response(
            {"error": "Dados insuficientes para análise de tendência"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    insight = build_temperature_insight(temperatures)

    return Response(
        {
            "city": city,
            **insight,
        },
        status=status.HTTP_200_OK,
    )
