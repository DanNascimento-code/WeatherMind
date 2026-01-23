# Re-export weather service functions for convenient importing
from .weather import (
    get_current_weather_for_location,
    get_forecast_for_location,
)

__all__ = [
    "get_forecast_for_location",
    "get_current_weather_for_location",
]
