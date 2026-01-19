from typing import List, Dict


def analyze_temperature(temperatures: List[float]) -> Dict[str, str]:
    if not temperatures or len(temperatures) < 2:
        return {
            "trend": "insufficient_data",
            "variation": "insufficient_data",
            "stability": "insufficient_data",
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

    return {
        "trend": trend,
        "variation": variation,
        "stability": stability,
    }
