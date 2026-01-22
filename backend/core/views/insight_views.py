
"""
Thermal Comfort Insight Views Module

This module provides REST API endpoints for thermal comfort analysis based on weather conditions.

Classes:
    ThermalComfortInsightView: APIView that calculates and returns thermal comfort insights.

Endpoints:
    GET /api/insights/thermal-comfort/ - Retrieve thermal comfort insight data
        
        Query Parameters:
            None (currently uses simulated data)
        
        Response (200 OK):
            {
                "comfort_level": str,
                "recommendation": str,
                "temperature": float,
                "humidity": int,
                "wind_speed": float
            }
        
        Example:
            GET /api/insights/thermal-comfort/
            
            Returns thermal comfort analysis including comfort level assessment
            and personalized recommendations for the given weather conditions.

Note:
    Weather data is currently simulated. Integration with real weather services
    is planned for future releases.
"""




from rest_framework.views import APIView  # Base class for creating API views with HTTP method handlers
from rest_framework.response import Response  # DRF response object for API responses
from rest_framework import status  # HTTP status codes for responses

from core.insights.comfort import thermal_comfort_insight  # Service function to calculate thermal comfort insights
from core.serializers.insight_serializers import ThermalComfortInsightSerializer  # Serializer for validating and formatting thermal comfort data
from core.services.climate_service import ClimateService  # Service to fetch real weather data from OpenWeatherMap API
from core.exceptions.climate import CityNotFoundError, ClimateAPIUnavailableError  # Custom exceptions for weather API errors

class ThermalComfortInsightView(APIView):
    """
    API endpoint that exposes thermal comfort insights based on weather conditions.
    """

    def get(self, request):
        # Extract city name from query parameters (required for fetching real weather data)
        city = request.GET.get("city")
        
        # Validate that city parameter is provided
        if not city:
            return Response(
                {"error": "O parâmetro 'city' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Initialize the ClimateService to fetch real weather data from OpenWeatherMap API
            climate_service = ClimateService()
            
            # Fetch real weather data for the specified city
            # This returns normalized data: {city, temperature, feels_like, humidity, condition, wind_speed}
            api_weather_data = climate_service.get_weather_by_city(city)
            
            # Transform API response to format expected by thermal_comfort_insight function
            weather_data = {
                "temperature": api_weather_data["temperature"],  # Temperature in Celsius from API
                "humidity": api_weather_data["humidity"],  # Humidity percentage from API
                "wind_speed": api_weather_data["wind_speed"]  # Wind speed in m/s from API
            }
            
        except CityNotFoundError:
            # Return 404 if the city is not found in the weather API
            return Response(
                {"error": f"Cidade '{city}' não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ClimateAPIUnavailableError as e:
            # Return 503 if the weather API is unavailable or unreachable
            return Response(
                {"error": "Serviço climático indisponível no momento."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            # Return 500 for any other unexpected errors
            return Response(
                {"error": "Erro ao recuperar dados climáticos."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Generate thermal comfort insight based on the real weather data
        insight = thermal_comfort_insight(weather_data)

        # Validate the insight data using the serializer
        serializer = ThermalComfortInsightSerializer(data=insight)
        serializer.is_valid(raise_exception=True)

        # Return the validated insight data with HTTP 200 OK status
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
