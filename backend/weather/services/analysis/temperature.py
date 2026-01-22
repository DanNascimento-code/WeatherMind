from typing import List, Dict, Union


def analyze_temperature(temperatures: List[float]) -> Dict[str, Union[str, float]]:
    if not temperatures or len(temperatures) < 2:
        return {
            "trend": "insufficient_data",
            "variation": "insufficient_data",
            "stability": "insufficient_data",
            "min": None,
            "max": None,
            "average": None,
            "amplitude": None,
        }

    first = temperatures[0]
    last = temperatures[-1]

    # 1. Tendência
    if last > first:
        trend = "up"
    elif last < first:
        trend = "down"
    else:
        trend = "stable"

    # 2. Variação (amplitude térmica)
    amplitude = max(temperatures) - min(temperatures)

    if amplitude < 2:
        variation = "low"
    elif amplitude <= 5:
        variation = "moderate"
    else:
        variation = "high"

    # 3. Estabilidade
    deltas = [
        abs(temperatures[i] - temperatures[i - 1])
        for i in range(1, len(temperatures))
    ]

    average_delta = sum(deltas) / len(deltas)

    if average_delta < 1:
        stability = "stable"
    else:
        stability = "unstable"

    # 4. Métricas estatísticas
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    average_temp = sum(temperatures) / len(temperatures)

    return {
        "trend": trend,
        "variation": variation,
        "stability": stability,
        "min": round(min_temp, 2),
        "max": round(max_temp, 2),
        "average": round(average_temp, 2),
        "amplitude": round(amplitude, 2),
    }
