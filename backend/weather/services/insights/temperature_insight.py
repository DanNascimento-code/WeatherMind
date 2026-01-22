"""
Temperature Insight Builder Module

This module constructs comprehensive temperature insights by analyzing historical temperature data
and generating actionable recommendations for users.

Functions:
    build_temperature_insight(temperatures: List[float]) -> Dict[str, Any]
        Analyzes temperature data and generates insights, interpretations, impact assessments,
        and actionable suggestions.

Insight Structure:
    The function returns a dictionary containing:
    {
        "analysis": {
            "min": float,
            "max": float,
            "average": float,
            "trend": str,
            ...
        },
        "interpretation": str,          # Human-readable description of temperature patterns
        "impact": {
            "health": str,              # Impact on human health
            "comfort": str,             # Comfort level assessment
            ...
        },
        "suggestions": [str]            # Actionable recommendations for users
    }

Usage Example:
    temperatures = [22.5, 23.1, 24.0, 25.3, 26.1]  # Temperature readings over time
    insight = build_temperature_insight(temperatures)
    
    # Returns comprehensive analysis with trends, interpretations, and recommendations

Dependencies:
    - weather.services.analysis.temperature: Calculates statistical metrics and trends from temperature data
    - weather.services.analysis.interpretation: Converts analysis metrics into human-readable descriptions
    - weather.services.analysis.impact: Evaluates health and comfort impacts from temperature conditions
    - weather.services.analysis.suggestions: Generates actionable recommendations based on analysis and impacts
"""

from typing import List, Dict, Any  # Type hints for list of floats, dictionary with any values, and generic type

from weather.services.analysis.impact import assess_temperature_impact  # Evaluates health and comfort impacts from temperature data
from weather.services.analysis.temperature import analyze_temperature  # Calculates statistical metrics and trends from temperature readings
from weather.services.analysis.interpretation import interpret_temperature_analysis  # Converts analysis metrics into human-readable descriptions
from weather.services.analysis.suggestions import suggest_actions_from_temperature  # Generates actionable recommendations based on temperature analysis    
    



def build_temperature_insight(
    temperatures: List[float],
) -> Dict[str, Any]:
    """
    Build a comprehensive temperature insight from historical temperature readings.
    
    Args:
        temperatures (List[float]): A list of temperature values in chronological order
    
    Returns:
        Dict[str, Any]: A dictionary containing analysis, interpretation, impact, and suggestions
    """
    # Perform statistical analysis on the temperature data to extract metrics and trends
    analysis = analyze_temperature(temperatures)

    # Generate a human-readable interpretation of the temperature patterns and trends
    interpretation = interpret_temperature_analysis(analysis)
    # Assess the potential impact of the temperature conditions on health, comfort, etc.
    impact = assess_temperature_impact(analysis)
    # Generate actionable suggestions and recommendations based on analysis results and impacts
    suggestions = suggest_actions_from_temperature(analysis, impact)

    # Return a comprehensive insight dictionary with all analysis components
    return {
        "analysis": analysis,  # Raw statistical analysis and metrics
        "interpretation": interpretation,  # Human-readable interpretation
        "impact": impact,  # Health, comfort, and other impact assessments
        "suggestions": suggestions,  # Actionable recommendations for the user
    }

