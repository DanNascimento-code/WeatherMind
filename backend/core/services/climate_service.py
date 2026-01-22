"""
Climate Service Module

This module provides weather data retrieval and caching functionality for the weathermind application.
It integrates with the OpenWeatherMap API to fetch real-time weather information by city name.

Key Features:
    - Fetches current weather data from OpenWeatherMap API
    - Implements caching mechanism to reduce API calls and improve performance
    - Normalizes API responses into a standardized format
    - Handles authentication and availability errors with custom exceptions
    - Uses metric units and Portuguese language for responses

Classes:
    ClimateService: Main service class for weather operations

Example:
    >>> service = ClimateService()
    >>> weather_data = service.get_weather_by_city("São Paulo")
    >>> print(weather_data["temperature"])  # Get current temperature
"""

import requests  # HTTP requests library for API communication

from django.conf import settings  # Django settings access
from django.core.cache import cache  # Django caching framework

from core.exceptions.climate import (  # Custom climate-related exceptions
    CityNotFoundError,
    ClimateAPIAuthError,
    ClimateAPIUnavailableError,
)


class ClimateService:
    """
    Service class for fetching and managing weather data from OpenWeatherMap API.
    
    This class handles all weather-related operations including API communication,
    response normalization, and data caching to optimize performance.
    
    Attributes:
        BASE_URL (str): OpenWeatherMap API endpoint for current weather data
        CACHE_TIMEOUT (int): Cache expiration time in seconds (600 seconds = 10 minutes)
        api_key (str): OpenWeatherMap API key from Django settings
    """
    # OpenWeatherMap API endpoint for current weather information
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    # Cache duration set to 10 minutes to balance freshness and API call reduction
    CACHE_TIMEOUT = 60 * 10  # 10 minutos

    def __init__(self):
        """Initialize the ClimateService with the API key from settings."""
        self.api_key = settings.OPENWEATHER_API_KEY

    def get_weather_by_city(self, city: str) -> dict:
        """
        Fetch current weather data for a given city.
        
        This method first checks the cache for existing data before making an API call.
        If found in cache, returns cached data. Otherwise, fetches from OpenWeatherMap API,
        normalizes the response, caches it, and returns the normalized data.
        
        Args:
            city (str): City name to fetch weather for
            
        Returns:
            dict: Normalized weather data containing city, temperature, humidity, etc.
            
        Raises:
            CityNotFoundError: If the city is not found by the API
            ClimateAPIAuthError: If the API key is invalid
            ClimateAPIUnavailableError: If the API is unreachable or returns an error
        """
        # Generate cache key based on city name (normalized to handle variations)
        cache_key = self._get_cache_key(city)

        # Check if weather data already exists in cache
        cached_data = cache.get(cache_key)
        if cached_data:
            # Return cached data to avoid unnecessary API calls
            return cached_data

        # Build request parameters for the API call
        params = {
            "q": city,  # City name query parameter
            "appid": self.api_key,  # API authentication key
            "units": "metric",  # Use Celsius instead of Kelvin
            "lang": "pt_br",  # Return descriptions in Portuguese (Brazil)
        }

        try:
            # Make HTTP request to OpenWeatherMap API with 5-second timeout
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=5
            )
        except requests.RequestException:
            # Handle network errors or connection timeouts
            raise ClimateAPIUnavailableError(
                "Não foi possível conectar à API climática"
            )

        # Handle HTTP 401 Unauthorized - invalid API key
        if response.status_code == 401:
            raise ClimateAPIAuthError("Chave de API inválida")

        # Handle HTTP 404 Not Found - city doesn't exist
        if response.status_code == 404:
            raise CityNotFoundError(f"Cidade '{city}' não encontrada")

        # Handle other HTTP errors
        if response.status_code != 200:
            raise ClimateAPIUnavailableError(
                "Erro inesperado ao consultar o clima"
            )

        # Parse JSON response from the API
        data = response.json()
        # Convert API response to standardized format
        normalized_data = self._normalize_weather_data(data)

        # Store normalized data in cache for future requests
        cache.set(
            cache_key,
            normalized_data,
            timeout=self.CACHE_TIMEOUT
        )

        return normalized_data

    def _get_cache_key(self, city: str) -> str:
        """
        Generate a cache key from city name.
        
        Normalizes the city name by converting to lowercase, stripping whitespace,
        and replacing spaces with underscores to create a valid cache key.
        
        Args:
            city (str): Original city name
            
        Returns:
            str: Formatted cache key (e.g., "weather:sao_paulo")
        """
        # Normalize city name: lowercase, trim whitespace, replace spaces with underscores
        return f"weather:{city.lower().strip().replace(' ', '_')}"

    def _normalize_weather_data(self, data: dict) -> dict:
        """
        Transform OpenWeatherMap API response into standardized format.
        
        Extracts relevant weather information from the API response and returns
        only the essential fields needed by the application.
        
        Args:
            data (dict): Raw JSON response from OpenWeatherMap API
            
        Returns:
            dict: Normalized weather data with keys: city, temperature, feels_like,
                  humidity, condition, wind_speed
        """
        return {
            "city": data["name"],  # City name from API response
            "temperature": data["main"]["temp"],  # Current temperature in Celsius
            "feels_like": data["main"]["feels_like"],  # Apparent/feels-like temperature
            "humidity": data["main"]["humidity"],  # Humidity percentage (0-100)
            "condition": data["weather"][0]["description"],  # Weather condition description
            "wind_speed": data["wind"]["speed"],  # Wind speed in m/s
        }

