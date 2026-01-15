from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.insights.comfort import thermal_comfort_insight
from core.serializers.insight_serializers import ThermalComfortInsightSerializer

class ThermalComfortInsightView(APIView):
    """
    Endpoint responsável por expor o insight de conforto térmico.
    """

    def get(self, request):
        # Neste momento, os dados climáticos ainda são simulados.
        # No próximo passo eles virão de um serviço real.
        weather_data = {
            "temperature": 28,
            "humidity": 75,
            "wind_speed": 2.5
        }

        insight = thermal_comfort_insight(weather_data)

        serializer = ThermalComfortInsightSerializer(data=insight)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
