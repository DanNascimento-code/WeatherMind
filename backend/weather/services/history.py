
"""
Weather History Service Module

This module provides functionality to retrieve historical weather records from the database.
It serves as a data access layer for fetching weather data for specific cities, with support
for limiting the number of results and sorting by most recent records first.

Key Features:
    - Query historical weather records by city name
    - Supports result limiting to retrieve top N records
    - Case-insensitive city name matching (e.g., "São Paulo" matches "são paulo")
    - Returns records sorted by creation date in descending order (newest first)
    - Integrates with Django ORM for efficient database queries

Functions:
    get_city_history(city, limit=5): Retrieves historical weather records for a city

Example:
    >>> from weather.services.history import get_city_history
    >>> records = get_city_history("São Paulo", limit=10)
    >>> for record in records:
    ...     print(f"{record.city}: {record.temperature}°C")
"""

from weather.models import WeatherRecord  # Django model for storing weather data records


def get_city_history(city, limit=5):
    """
    Retrieve historical weather records for a specified city.

    Queries the database for weather records matching the city name, normalizes the city
    name for consistent matching, and returns the most recent records sorted in descending
    order (newest first).

    Args:
        city (str): Name of the city to retrieve weather history for.
                   Case-insensitive matching will be applied.
        limit (int, optional): Maximum number of records to return. Defaults to 5.
                              Can be set to any positive integer.

    Returns:
        QuerySet: Django QuerySet of WeatherRecord objects matching the criteria.
                 Returns up to 'limit' most recent records, ordered newest first.
                 Returns empty QuerySet if no records found for the city.

    Example:
        >>> records = get_city_history("London", limit=10)
        >>> len(records)  # Number of records returned (up to 10)
        >>> records[0].created_at  # Most recent record timestamp
        >>> records[0].temperature  # Temperature value
    """
    # Query WeatherRecord database with case-insensitive city name matching
    # Order by created_at descending to get newest records first
    # Slice the queryset to limit results to the specified number
    return WeatherRecord.objects.filter(
        # Use iexact for case-insensitive matching (e.g., "São Paulo" matches "são paulo")
        city__iexact=city.strip()
    ).order_by("-created_at")[:limit]  # Sort by creation timestamp (newest first) and limit results

