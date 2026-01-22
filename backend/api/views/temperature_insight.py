"""
Temperature Insight API View Module

This module provides REST API endpoints for retrieving and analyzing temperature data for cities.
It integrates historical temperature records with insight generation to provide meaningful analysis.

Key Features:
    - Fetches historical temperature data for specified cities
    - Generates temperature insights based on historical trends
    - Returns comprehensive JSON responses with city and insight information
    - Implements proper HTTP error handling and validation
    - Restricted to GET requests only

Views:
    temperature_insight_view: GET endpoint for retrieving temperature insights

Example:
    GET /api/v1/insights/temperature/?city=São%20Paulo
    Returns: {"city": "São Paulo", "insight": {...temperature analysis...}}
"""

import json
from django.http import HttpResponse  # HTTP response handler for JSON payloads
from django.views.decorators.http import require_GET  # Decorator to restrict HTTP methods to GET

from weather.services.insights.temperature_insight import build_temperature_insight  # Service to generate insight analysis
from weather.services.history import get_city_history  # Service to retrieve historical temperature data


# HTTP method restriction: only GET requests are allowed for this view
@require_GET
def temperature_insight_view(request):
    """
    API endpoint for retrieving temperature insights for a city.

    This view processes GET requests to analyze temperature trends for a specified city.
    It retrieves historical temperature data, generates insights, and returns a comprehensive
    JSON response with the city information and insight analysis.

    Args:
        request (HttpRequest): Django request object containing query parameters

    Query Parameters:
        city (str, required): The name of the city to get temperature insights for

    Returns:
        JsonResponse: JSON response containing:
            - Success (200): {"city": str, "insight": dict}
            - Bad Request (400): {"error": str} - missing city parameter
            - Not Found (404): {"error": str} - no historical data for city
            - Server Error (500): {"error": str} - unexpected error during processing

    Example:
        GET /api/temperature-insight/?city=London
        Response: {
            "city": "London",
            "insight": {
                "average_temp": 15.2,
                "max_temp": 22.5,
                "min_temp": 8.1,
                ...
            }
        }
    """
    # Extract city name from query parameters
    city = request.GET.get("city")

    # Validate that city parameter is provided
    if not city:
        # Return 400 Bad Request if city is missing
        return HttpResponse(
            json.dumps({"error": "Parâmetro 'city' é obrigatório."}, ensure_ascii=False),
            status=400,
            content_type="application/json",
        )

    try:
        # Fetch the 10 most recent temperature records for the specified city
        history_records = get_city_history(city, limit=10)
        
        # Check if historical data exists for the city
        if not history_records:
            # Return 404 Not Found if no data is available
            return HttpResponse(
                json.dumps(
                    {"error": f"Não há dados históricos de temperatura para a cidade de '{city}'."},
                    ensure_ascii=False,
                ),
                status=404,
                content_type="application/json",
            )

        # Extract temperature values from the history records for analysis
        temperatures = [record.temperature for record in history_records]

        # Generate insight analysis based on temperature trends
        insight = build_temperature_insight(temperatures)

        # Get the actual city name from the database record for consistency
        actual_city = history_records[0].city

        # Return successful response with city and insight information
        return HttpResponse(
            json.dumps(
                {
                    "city": actual_city,
                    "insight": insight,
                },
                ensure_ascii=False,
            ),
            status=200,
            content_type="application/json",
        )

    except Exception as exc:
        # Catch any unexpected errors during processing
        # TODO: Uncomment logger when logging is configured
        # logger.error(f"Error generating temperature insight for {city}: {exc}")
        
        # Return 500 Internal Server Error for unexpected exceptions
        return HttpResponse(
            json.dumps(
                {"error": "Ocorreu um erro inesperado ao gerar a análise de temperatura."},
                ensure_ascii=False,
            ),
            status=500,
            content_type="application/json",
        )
