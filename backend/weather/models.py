"""
Weather Models Module

This module defines the database models for storing weather data and historical records.
It provides the data structure for persisting weather information fetched from external APIs.

Models:
    WeatherRecord: Stores weather observations for a specific city and timestamp.

Database Schema:
    WeatherRecord:
        - city (str): Name of the city (max 100 characters)
        - country (str): ISO country code (max 10 characters)
        - temperature (float): Current temperature in Celsius
        - feels_like (float): Perceived temperature in Celsius
        - humidity (int): Humidity percentage (0-100)
        - condition (str): Weather condition description (max 100 characters)
        - created_at (datetime): Timestamp when the record was created (auto-set, not modifiable)

Usage:
    # Create a new weather record
    WeatherRecord.objects.create(
        city='London',
        country='GB',
        temperature=15.5,
        feels_like=14.2,
        humidity=72,
        condition='Cloudy'
    )
    
    # Query recent records for a city
    records = WeatherRecord.objects.filter(city='London').order_by('-created_at')[:10]
    
    # Access weather data
    for record in records:
        print(record.temperature, record.condition)
"""

from django.db import models  # Django ORM models for database table definitions and operations


class WeatherRecord(models.Model):
    """
    Database model to store weather observations for a specific city at a point in time.
    
    This model is used to persist weather data fetched from external APIs and provides
    the foundation for historical weather analysis and trend tracking.
    """
    # City name where the weather observation was taken
    city = models.CharField(max_length=100)
    # ISO country code of the city (e.g., 'GB', 'US', 'BR')
    country = models.CharField(max_length=10)

    # Current air temperature in Celsius
    temperature = models.FloatField()
    # Perceived temperature (wind chill/heat index) in Celsius
    feels_like = models.FloatField()
    # Relative humidity as a percentage (0-100)
    humidity = models.IntegerField()

    # Human-readable weather condition description (e.g., 'Sunny', 'Rainy', 'Cloudy')
    condition = models.CharField(max_length=100)

    # Timestamp automatically set to the current date and time when the record is created
    # Cannot be modified after creation (immutable)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human-readable string representation of the weather record."""
        return f"{self.city} - {self.temperature}°C ({self.created_at.date()})"
