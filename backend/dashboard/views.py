"""
Dashboard Views Module

This module provides views for rendering the main weather dashboard interface.
It retrieves current weather conditions and forecast data for the default user location,
then passes this information to the dashboard template for display.

Key Features:
    - Fetches the default user location with validation
    - Validates location has required geographic coordinates
    - Retrieves current weather data for the location
    - Retrieves weather forecast data for the location
    - Implements comprehensive error handling for missing data and API failures
    - Gracefully handles cases where no location is set or coordinates are missing
    - Returns appropriate error messages to the template for user feedback

Views:
    index: Main dashboard view that displays weather and forecast information
           with built-in error handling and validation

Example:
    GET /dashboard/
    Returns: Rendered dashboard.html with weather data, forecast, and error messages
"""

from django.shortcuts import render  # Django shortcut function to render templates with context

from locations.selectors import get_default_location  # Selector function to retrieve the user's default location
from weather.services.weather import (  # Weather service functions for data retrieval
    get_current_weather_for_location,  # Fetches current weather conditions for a location
    get_forecast_for_location,  # Fetches weather forecast for a location
)
from core.insights.comfort import thermal_comfort_insight  # Generates comfort-based insights from weather data




def index(request):
    """
    Render the main weather dashboard with current conditions and forecast.

    This view retrieves the user's default location and fetches associated weather data
    (current conditions and forecast). Comprehensive error handling ensures graceful
    degradation if location data is missing or API calls fail.

    Args:
        request (HttpRequest): Django request object from the user

    Returns:
        HttpResponse: Rendered dashboard template with weather context containing:
            - location: User's default location object (None if not set)
            - weather: Current weather data for the location (None if unavailable)
            - forecast: Weather forecast list (empty if unavailable)
            - error: Error message string if something went wrong (None if successful)

    Template:
        dashboard/index.html - Displays weather information, forecast, and error messages

    Possible Errors:
        - "No location configured": User has not set a default location
        - "Location missing coordinates": Location exists but lacks latitude/longitude
        - "Unable to fetch weather data": API call failed for current weather
        - "Unable to fetch forecast data": API call failed for forecast
    """
    # Initialize context variables with default empty values
    location = None  # User's default location object
    weather = None  # Current weather conditions
    forecast = []  # Weather forecast data
    insights = None  # Personalized insights based on weather
    error = None  # Error message for template display

    try:
        # Retrieve the user's default location from the database
        location = get_default_location()
        
        # Validate that a default location exists
        if not location:
            # Return early with error message if no location is configured
            error = "No location configured. Please set a default location in your profile."
            context = {
                "location": location,
                "weather": weather,
                "forecast": forecast,
                "error": error,
            }
            return render(request, "dashboard/index.html", context)

        # Validate that the location has required geographic coordinates
        if not location.latitude or not location.longitude:
            # Return early with error message if coordinates are missing
            error = "Location is missing geographic coordinates (latitude/longitude). Please update your location settings."
            context = {
                "location": location,
                "weather": weather,
                "forecast": forecast,
                "error": error,
            }
            return render(request, "dashboard/index.html", context)

        # Attempt to fetch current weather conditions for the location
        try:
            weather = get_current_weather_for_location(location=location)
            # Log if weather data is None (optional - uncomment if logger is configured)
            # if not weather:
            #     logger.warning(f"No weather data returned for location: {location.name}")
        except Exception as weather_error:
            # Log the weather API error (optional - uncomment if logger is configured)
            # logger.error(f"Error fetching current weather: {str(weather_error)}")
            error = "Unable to fetch current weather data. Please try again later."

        # Attempt to fetch weather forecast for the location
        try:
            forecast = get_forecast_for_location(location=location)
            # Log if forecast is empty (optional - uncomment if logger is configured)
            # if not forecast:
            #     logger.warning(f"No forecast data returned for location: {location.name}")
        except Exception as forecast_error:
            # Log the forecast API error (optional - uncomment if logger is configured)
            # logger.error(f"Error fetching forecast: {str(forecast_error)}")
            # Note: Don't override error if weather fetch already failed
            if not error:
                error = "Unable to fetch forecast data. Please try again later."

        # Attempt to generate personalized insights based on current weather
        try:
            if weather:
                insights = thermal_comfort_insight(weather)

                INSIGHT_UI_LEVEL_MAP = {
                    "unknown": "neutral",
                    "moderate": "good",
                    "low": "bad",
                }

                raw_level = insights.get("level", "unknown")
                insights["ui_level"] = INSIGHT_UI_LEVEL_MAP.get(raw_level, "neutral")
        
               
        except Exception as insights_error:
            # Log the insights generation error (optional - uncomment if logger is configured)
            # logger.error(f"Error generating insights: {str(insights_error)}")
            pass  # Continue without insights if generation fails

    except Exception as e:
        # Catch any unexpected errors during location retrieval or processing
        # logger.error(f"Unexpected error in dashboard view: {str(e)}")
        error = "An unexpected error occurred. Please try refreshing the page."

    # Prepare context dictionary with location, weather data, insights, and any error messages
    context = {
        "location": location,  # Location object or None
        "weather": weather,  # Current weather conditions or None
        "forecast": forecast,  # Forecast data list (empty if unavailable)
        "insights": insights,  # Personalized insights or None
        "error": error,  # Error message or None if no errors
    }

    # Render the dashboard template with the prepared context
    return render(request, "dashboard/index.html", context)

