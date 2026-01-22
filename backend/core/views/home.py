
"""
home view ( / ), responsible to render and pass data context to the main page template
and handle weather search requests.

"""




import json  # For converting Python objects to JSON strings for JavaScript
from django.shortcuts import render 
from weather.models import WeatherRecord  # Database model for storing weather records
from core.services.climate_service import ClimateService  # Service to fetch weather data from external API
from core.exceptions.climate import ClimateServiceError  # Custom exception for climate service errors


def home(request):
    # Extract city from query parameters (e.g., ?city=London)
    city = request.GET.get("city")
    # Initialize variables to hold weather and error data
    weather_data = None
    error_message = None
    history = []
    labels = []
    temperatures = []

    # Process only if a city is provided
    if city:
        # Initialize the climate service to fetch weather data
        service = ClimateService()

        try:
            # Fetch weather data from the external API for the given city
            weather_data = service.get_weather_by_city(city)
            
            # Save the fetched weather record to the database for historical tracking
            WeatherRecord.objects.create(
                city=weather_data["city"],
                country=weather_data.get("country", ""),
                temperature=weather_data["temperature"],
                feels_like=weather_data["feels_like"],
                humidity=weather_data["humidity"],
                condition=weather_data["condition"],
            )
        except ClimateServiceError as error:
            # Capture any climate service errors and store the message to display
            error_message = str(error)
        
        # Fetch the last 10 weather records for the queried city, ordered by most recent first
        history = WeatherRecord.objects.filter(
            city__iexact=city
        ).order_by('-created_at')[:10]

        # Prepare chart data if historical records exist
        if history:
            # Reverse the history to chronological order (oldest to newest) for the chart
            chart_data = reversed(history)
            # Extract formatted timestamps as labels for the x-axis
            labels = [record.created_at.strftime("%d/%m %H:%M") for record in chart_data]
            
            # Re-reverse the history since the previous iterator was consumed
            chart_data = reversed(history)
            # Extract temperatures corresponding to each timestamp for the y-axis
            temperatures = [record.temperature for record in chart_data]

    # Build the context dictionary with all data to pass to the template
    context = {
        "weather": weather_data,
        "error": error_message,
        "history": history,
        "labels": json.dumps(labels),  # Convert labels list to JSON for JavaScript
        "temperatures": json.dumps(temperatures),  # Convert temperatures list to JSON for JavaScript
    }

    # Render the home template with the populated context
    return render(request, "core/home.html", context)






