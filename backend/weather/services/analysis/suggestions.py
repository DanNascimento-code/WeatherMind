from typing import Dict, List


def suggest_actions_from_temperature(
    analysis: Dict[str, str],
    impact: str,
) -> List[str]:
    trend = analysis.get("trend")
    variation = analysis.get("variation")
    stability = analysis.get("stability")

    if trend == "insufficient_data":
        return ["Aguarde mais dados para receber sugestões climáticas."]

    suggestions = []

    # Sugestões baseadas na variação
    if variation == "high":
        suggestions.append(
            "Considere se preparar para variações de temperatura ao longo do dia."
        )
    elif variation == "moderate":
        suggestions.append(
            "Leve em conta possíveis mudanças térmicas durante o período."
        )

    # Sugestões baseadas na estabilidade
    if stability == "unstable":
        suggestions.append(
            "Tenha uma opção extra de roupa para lidar com mudanças rápidas de clima."
        )
    else:
        suggestions.append(
            "As condições estáveis favorecem o planejamento de atividades externas."
        )

    # Sugestões baseadas na tendência
    if trend == "up":
        suggestions.append(
            "Roupas mais leves podem ser mais confortáveis."
        )
    elif trend == "down":
        suggestions.append(
            "Uma camada adicional de roupa pode ser útil."
        )

    return suggestions


