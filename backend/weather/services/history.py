
from weather.models import WeatherRecord

def get_city_history(city, limit=5):
    return WeatherRecord.objects.filter(
        city=city.strip().lower()
    ).order_by("-created_at")[:limit]

