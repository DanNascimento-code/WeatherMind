
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

class ThermalComfortInsightView(APIView):
    """
    API endpoint that exposes thermal comfort insights based on weather conditions.
    """

    def get(self, request):
        # Simulated weather data (placeholder - will be replaced with real service data)
        weather_data = {
            "temperature": 28,  # Temperature in Celsius
            "humidity": 75,  # Humidity percentage
            "wind_speed": 2.5  # Wind speed in m/s
        }

        # Generate thermal comfort insight based on the weather data
        insight = thermal_comfort_insight(weather_data)

        # Validate the insight data using the serializer
        serializer = ThermalComfortInsightSerializer(data=insight)
        serializer.is_valid(raise_exception=True)

        # Return the validated insight data with HTTP 200 OK status
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
