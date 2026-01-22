"""
Temperature Insight Views Module

This module provides REST API endpoints for analyzing temperature trends and patterns
for a specific city based on historical weather data.

Functions:
    temperature_insight_view: API endpoint that generates temperature insights for a city.

Endpoints:
    GET /api/insights/temperature-trend/ - Retrieve temperature trend analysis
        
        Query Parameters:
            city (str, required): The city name for which to retrieve temperature insights
                Example: ?city=London
        
        Response (200 OK):
            {
                "city": str,
                "trend": str,
                "average_temp": float,
                "temperature_range": dict,
                ...additional insight data
            }
        
        Error Responses:
            400 Bad Request: Missing or invalid 'city' parameter
            422 Unprocessable Entity: Insufficient data for trend analysis (< 2 records)
        
        Example:
            GET /api/insights/temperature-trend/?city=London
            
            Returns temperature trend analysis including average temperature,
            temperature range, and trend direction based on recent data.

Workflow:
    1. Validate that the 'city' query parameter is provided
    2. Fetch and update the latest weather data for the city
    3. Retrieve recent historical temperature records
    4. Validate that sufficient data exists (minimum 2 records)
    5. Generate temperature insights and trends
    6. Return the analysis as JSON
"""

from rest_framework.decorators import api_view  # Decorator to define a function-based API view with specific HTTP methods
from rest_framework.response import Response  # DRF response object for API responses
from rest_framework import status  # HTTP status codes for responses

from weather.services.weather_service import (  # Weather service functions
    fetch_weather,  # Updates and persists current weather data for a city
    get_recent_temperatures_for_city,  # Retrieves recent temperature history
)
from weather.services.insights.temperature_insight import (  # Temperature analysis service
    build_temperature_insight,  # Generates insights and trends from temperature data
)


@api_view(["GET"])  # Only accept GET HTTP requests
def temperature_insight_view(request):
    # Extract the city name from query parameters (e.g., ?city=London)
    city = request.query_params.get("city")

    # Validate that the city parameter was provided
    if not city:
        return Response(
            {"error": "The 'city' parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Fetch and update weather data to ensure current information is persisted to database
    fetch_weather(city)

    # Retrieve the recent temperature records for the specified city
    temperatures = get_recent_temperatures_for_city(city)

    # Validate that sufficient historical data exists for trend analysis (minimum 2 records)
    if len(temperatures) < 2:
        return Response(
            {"error": "Insufficient data for temperature trend analysis"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # Generate temperature insights and trends based on the historical data
    insight = build_temperature_insight(temperatures)

    # Return the city name along with the generated insight data
    return Response(
        {
            "city": city,
            **insight,  # Unpack the insight dictionary into the response
        },
        status=status.HTTP_200_OK,
    )
