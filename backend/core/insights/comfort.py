
def thermal_comfort_insight(weather_data: dict) -> dict:
    """
    Gera um insight simples de conforto térmico baseado em regras.
    """

    temperature = weather_data.get("temperature")
    humidity = weather_data.get("humidity")
    wind_speed = weather_data.get("wind_speed")

    if temperature is None or humidity is None:
        return {
            "level": "unknown",
            "summary": "Dados insuficientes para avaliar o conforto térmico",
            "factors": []
        }

    factors = []

    if humidity >= 70:
        factors.append("high_humidity")

    if temperature >= 30:
        factors.append("high_temperature")

    if temperature <= 10:
        factors.append("low_temperature")

    if "high_temperature" in factors and "high_humidity" in factors:
        return {
            "level": "low",
            "summary": "Sensação de calor intenso e abafado",
            "factors": factors
        }

    if "low_temperature" in factors:
        return {
            "level": "low",
            "summary": "Sensação de frio acentuado",
            "factors": factors
        }

    return {
        "level": "moderate",
        "summary": "Condições térmicas razoavelmente confortáveis",
        "factors": factors
    }
