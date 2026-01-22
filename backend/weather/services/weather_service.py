"""
Weather Service Module

This module provides core functionality for fetching, storing, and retrieving weather data
from OpenWeatherMap API and the local database using location-based queries.

Functions:
    get_weather_by_location(latitude: float, longitude: float) -> dict
        Fetches current weather data using geographic coordinates from OpenWeatherMap API.
        
    save_weather_record(data: dict) -> None
        Persists weather data to the database for historical tracking.
    
    fetch_and_save_weather(latitude: float, longitude: float) -> dict
        Fetches weather data from API using coordinates and saves it to the database.
    
    get_recent_temperatures_for_city(city: str, hours: int = 24) -> List[float]
        Retrieves temperature readings from the database for a specified time period.

Data Flow:
    1. Location coordinates (latitude, longitude) are provided
    2. get_weather_by_location() calls OpenWeatherMap API with coordinates
    3. API response is parsed and normalized
    4. save_weather_record() stores the data in WeatherRecord model
    5. get_recent_temperatures_for_city() queries historical data by city name

API Details:
    - Provider: OpenWeatherMap (https://openweathermap.org/api)
    - Authentication: API key stored in Django settings (OPENWEATHER_API_KEY)
    - Query Method: Geographic coordinates (latitude, longitude)
    - Units: Metric (Celsius, meters/second)
    - Language: Portuguese (pt_br) for condition descriptions
"""

import requests  # HTTP library for making API calls to weather services
from django.conf import settings  # Django configuration for accessing API keys and settings
from weather.models import WeatherRecord  # Database model for storing weather records
from typing import List, Optional, Dict  # Type hints for function parameters and return values
from django.utils import timezone  # Django utilities for timezone-aware datetime operations
from datetime import timedelta  # For calculating time ranges in queries


def get_weather_by_location(latitude: float, longitude: float) -> Dict:
    """
    Fetch current weather data using geographic coordinates from OpenWeatherMap API.
    
    Args:
        latitude (float): Geographic latitude coordinate
        longitude (float): Geographic longitude coordinate
        
    Returns:
        dict: Normalized weather data with keys: city, country, temperature, feels_like, humidity, condition
        
    Raises:
        requests.RequestException: If API call fails
        ValueError: If coordinates are invalid
        KeyError: If API response is missing expected fields
    """
    # Validate coordinate inputs
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise ValueError("Invalid latitude or longitude coordinates")
    
    # OpenWeatherMap API endpoint for current weather data using coordinates
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # API request parameters including coordinates, API key, units, and language
    params = {
        "lat": latitude,  # Geographic latitude
        "lon": longitude,  # Geographic longitude
        "appid": settings.OPENWEATHER_API_KEY,  # API key from Django settings
        "units": "metric",  # Use metric units (Celsius, m/s)
        "lang": "pt_br",  # Response language set to Portuguese (Brazil)
    }

    try:
        # Make HTTP GET request to OpenWeatherMap API with 5-second timeout
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        
        # Parse the JSON response from the API
        data = response.json()
    except requests.RequestException as e:
        # Re-raise with more context about the API call
        raise requests.RequestException(f"Failed to fetch weather for coordinates ({latitude}, {longitude}): {str(e)}")

    # Extract and normalize the relevant weather information from the API response
    return {
        "city": data["name"].strip().lower(),  # City name (normalized to lowercase)
        "country": data["sys"]["country"],  # ISO country code
        "temperature": data["main"]["temp"],  # Current temperature in Celsius
        "feels_like": data["main"]["feels_like"],  # Perceived temperature
        "humidity": data["main"]["humidity"],  # Humidity percentage (0-100)
        "condition": data["weather"][0]["description"] if data.get("weather") else "indefinido",  # Weather condition description
    }


def save_weather_record(data: Dict) -> None:
    """
    Persist weather data to the database for historical tracking.
    
    Args:
        data (dict): Weather data dictionary containing city, country, temperature, 
                     feels_like, humidity, and condition
    """
    # Create a new WeatherRecord instance in the database with the provided weather data
    WeatherRecord.objects.create(
        city=data["city"],  # City name
        country=data["country"],  # Country code
        temperature=data["temperature"],  # Temperature value
        feels_like=data["feels_like"],  # Feels like temperature
        humidity=data["humidity"],  # Humidity percentage
        condition=data["condition"],  # Weather condition description
    )


def fetch_and_save_weather(latitude: float, longitude: float) -> Dict:
    """
    Fetch current weather data from API using coordinates and save to database.
    
    This combines fetching from the API and persisting to the database in one operation.
    
    Args:
        latitude (float): Geographic latitude coordinate
        longitude (float): Geographic longitude coordinate
        
    Returns:
        dict: The weather data that was fetched and saved
        
    Raises:
        requests.RequestException: If API call fails
        ValueError: If coordinates are invalid
    """
    # Fetch current weather data from the OpenWeatherMap API using coordinates
    weather_data = get_weather_by_location(latitude, longitude)
    
    # Save the fetched weather data to the database for historical tracking
    save_weather_record(weather_data)

    # Return the weather data to the caller
    return weather_data


def get_recent_temperatures_for_city(
    city: str,
    hours: int = 24,
) -> List[float]:
    """
    Retrieve temperature readings from the database for a specified city and time period.
    
    Queries historical weather records stored in the database for a given city
    and returns temperature values from within the specified hour range.
    
    Args:
        city (str): The city name to retrieve temperatures for (will be normalized)
        hours (int): Number of hours to look back (default: 24 hours)
    
    Returns:
        List[float]: List of temperature values ordered chronologically (oldest to newest)
        
    Example:
        >>> temps = get_recent_temperatures_for_city("São Paulo", hours=48)
        >>> print(len(temps))  # Number of temperature readings in past 48 hours
    """
    # Calculate the start time as current time minus the specified number of hours
    since = timezone.now() - timedelta(hours=hours)

    # Query the database for all weather records matching the city within the time period
    records = (
        WeatherRecord.objects
        .filter(city=city.strip().lower(), created_at__gte=since)  # Filter by city (normalized) and date range
        .order_by("created_at")  # Sort by creation time (oldest to newest)
    )

    # Extract just the temperature values from the records and return as a list
    return [record.temperature for record in records]


