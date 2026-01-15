import requests
from django.conf import settings


class WeatherServiceError(Exception):
    pass


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

    def get_current_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        response = requests.get(self.BASE_URL, params=params, timeout=5)

        if response.status_code != 200:
            raise WeatherServiceError(
                f"Erro ao buscar clima: {response.status_code}"
            )

        data = response.json()
        return self._normalize_current_weather(data)

    def _normalize_current_weather(self, data: dict) -> dict:
        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }