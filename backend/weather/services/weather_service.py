"""
Weather Service Module

This module provides core functionality for fetching, storing, and retrieving weather data
from OpenWeatherMap API and the local database.

Functions:
    get_weather_by_city(city: str) -> dict
        Fetches current weather data for a specified city from OpenWeatherMap API.
        
    save_weather_record(data: dict) -> None
        Persists weather data to the database for historical tracking.
    
    fetch_weather(city: str) -> dict
        Fetches weather data from API and saves it to the database in one operation.
    
    get_recent_temperatures_for_city(city: str, hours: int = 24) -> List[float]
        Retrieves temperature readings from the database for a specified time period.

Data Flow:
    1. get_weather_by_city() calls OpenWeatherMap API with city name
    2. API response is parsed and normalized
    3. save_weather_record() stores the data in WeatherRecord model
    4. get_recent_temperatures_for_city() queries historical data

API Details:
    - Provider: OpenWeatherMap (https://openweathermap.org/api)
    - Authentication: API key stored in Django settings (OPENWEATHER_API_KEY)
    - Units: Metric (Celsius, meters/second)
    - Language: Portuguese (pt_br) for condition descriptions
"""

import requests  # HTTP library for making API calls to weather services
from django.conf import settings  # Django configuration for accessing API keys and settings
from weather.models import WeatherRecord  # Database model for storing weather records
from typing import List  # Type hints for function parameters and return values
from django.utils import timezone  # Django utilities for timezone-aware datetime operations
from datetime import timedelta  # For calculating time ranges in queries


def get_weather_by_city(city):
    # OpenWeatherMap API endpoint for current weather data
    url = "https://api.openweathermap.org/data/2.5/weather"
    # API request parameters including city, API key, units, and language
    params = {
        "q": city,  # City name to search for
        "appid": settings.OPENWEATHER_API_KEY,  # API key from Django settings
        "units": "metric",  # Use metric units (Celsius, m/s)
        "lang": "pt_br",  # Response language set to Portuguese (Brazil)
    }

    # Make HTTP GET request to OpenWeatherMap API
    response = requests.get(url, params=params)
    # Parse the JSON response from the API
    data = response.json()

    # Extract and normalize the relevant weather information from the API response
    return {
        "city": data["name"].strip().lower(),  # City name (normalized to lowercase)
        "country": data["sys"]["country"],  # ISO country code
        "temperature": data["main"]["temp"],  # Current temperature in Celsius
        "feels_like": data["main"]["feels_like"],  # Perceived temperature
        "humidity": data["main"]["humidity"],  # Humidity percentage (0-100)
        "condition": data["weather"][0]["description"] if data.get("weather") else "indefinido",  # Weather condition description
    }


def save_weather_record(data):
    # Create a new WeatherRecord instance in the database with the provided weather data
    WeatherRecord.objects.create(
        city=data["city"],  # City name
        country=data["country"],  # Country code
        temperature=data["temperature"],  # Temperature value
        feels_like=data["feels_like"],  # Feels like temperature
        humidity=data["humidity"],  # Humidity percentage
        condition=data["condition"],  # Weather condition description
    )


def fetch_weather(city):
    # Fetch current weather data from the OpenWeatherMap API
    weather_data = get_weather_by_city(city)
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
    
    Args:
        city (str): The city name to retrieve temperatures for
        hours (int): Number of hours to look back (default: 24 hours)
    
    Returns:
        List[float]: List of temperature values ordered chronologically
    """
    # Calculate the start time as current time minus the specified number of hours
    since = timezone.now() - timedelta(hours=hours)

    # Query the database for all weather records matching the city within the time period
    records = (
        WeatherRecord.objects
        .filter(city=city.strip().lower(), created_at__gte=since)  # Filter by city and date range
        .order_by("created_at")  # Sort by creation time (oldest to newest)
    )

    # Extract just the temperature values from the records and return as a list
    return [record.temperature for record in records]


