from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def temperature_insight_view(request):
    """
    Analisa a variação de temperatura ao longo do tempo.
    Neste passo, os dados ainda são simulados.
    """

    # Simulação de dados históricos (ex: últimas horas ou dias)
    temperatures = [22, 23, 25, 28, 27, 26]

    delta = temperatures[-1] - temperatures[0]

    if delta > 2:
        trend = "subiu"
    elif delta < -2:
        trend = "caiu"
    else:
        trend = "estável"

    insight = {
        "trend": trend,
        "variation": delta,
        "data_points": len(temperatures),
    }

    return Response(insight, status=status.HTTP_200_OK)

