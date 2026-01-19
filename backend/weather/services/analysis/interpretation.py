from typing import Dict


def interpret_temperature_analysis(analysis: Dict[str, str]) -> str:
    trend = analysis.get("trend")
    variation = analysis.get("variation")
    stability = analysis.get("stability")

    if trend == "insufficient_data":
        return "Ainda não há dados suficientes para analisar a variação da temperatura."

    # Interpretação da tendência
    if trend == "up":
        trend_text = "A temperatura apresentou uma tendência de alta"
    elif trend == "down":
        trend_text = "A temperatura apresentou uma tendência de queda"
    else:
        trend_text = "A temperatura manteve-se estável"

    # Interpretação da variação
    if variation == "low":
        variation_text = "com pouca variação ao longo do período"
    elif variation == "moderate":
        variation_text = "com variação moderada ao longo do período"
    else:
        variation_text = "com variação acentuada ao longo do período"

    # Interpretação da estabilidade
    if stability == "stable":
        stability_text = "e mudanças graduais entre os dias"
    else:
        stability_text = "e mudanças bruscas entre os registros"

    return f"{trend_text}, {variation_text}, {stability_text}."
