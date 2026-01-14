import requests

class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, *, lat, lon, api_key):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        response = requests.get(
            f"{self.BASE_URL}/weather",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_forecast(self, *, lat, lon, api_key):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        response = requests.get(
            f"{self.BASE_URL}/forecast",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

