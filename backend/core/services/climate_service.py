
import requests

from django.conf import settings
from django.core.cache import cache

from core.exceptions.climate import (
    CityNotFoundError,
    ClimateAPIAuthError,
    ClimateAPIUnavailableError,
)


class ClimateService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    CACHE_TIMEOUT = 60 * 10  # 10 minutos

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

    def get_weather_by_city(self, city: str) -> dict:
        cache_key = self._get_cache_key(city)

        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=5
            )
        except requests.RequestException:
            raise ClimateAPIUnavailableError(
                "Não foi possível conectar à API climática"
            )

        if response.status_code == 401:
            raise ClimateAPIAuthError("Chave de API inválida")

        if response.status_code == 404:
            raise CityNotFoundError(f"Cidade '{city}' não encontrada")

        if response.status_code != 200:
            raise ClimateAPIUnavailableError(
                "Erro inesperado ao consultar o clima"
            )

        data = response.json()
        normalized_data = self._normalize_weather_data(data)

        cache.set(
            cache_key,
            normalized_data,
            timeout=self.CACHE_TIMEOUT
        )

        return normalized_data

    def _get_cache_key(self, city: str) -> str:
        return f"weather:{city.lower().strip().replace(' ', '_')}"

    def _normalize_weather_data(self, data: dict) -> dict:
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

