from typing import List, Dict, Any

from weather.services.analysis import (
    analyze_temperature,
    interpret_temperature_analysis,
    assess_temperature_impact,
    suggest_actions_from_temperature,
)


def build_temperature_insight(
    temperatures: List[float],
) -> Dict[str, Any]:
    analysis = analyze_temperature(temperatures)

    interpretation = interpret_temperature_analysis(analysis)
    impact = assess_temperature_impact(analysis)
    suggestions = suggest_actions_from_temperature(analysis, impact)

    return {
        "analysis": analysis,
        "interpretation": interpretation,
        "impact": impact,
        "suggestions": suggestions,
    }

