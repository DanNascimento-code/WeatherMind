from typing import Dict


def assess_temperature_impact(analysis: Dict[str, str]) -> str:
    trend = analysis.get("trend")
    variation = analysis.get("variation")
    stability = analysis.get("stability")

    if trend == "insufficient_data":
        return "Não é possível avaliar o impacto climático no momento por falta de dados."

    messages = []

    # Impacto da variação
    if variation == "high":
        messages.append(
            "A alta variação de temperatura pode causar desconforto térmico ao longo do período."
        )
    elif variation == "moderate":
        messages.append(
            "A variação moderada de temperatura pode ser perceptível ao longo do dia."
        )
    else:
        messages.append(
            "A baixa variação de temperatura tende a proporcionar maior conforto térmico."
        )

    # Impacto da estabilidade
    if stability == "unstable":
        messages.append(
            "Mudanças bruscas indicam um clima instável, exigindo maior atenção."
        )
    else:
        messages.append(
            "As mudanças graduais indicam um clima mais previsível."
        )

    # Impacto da tendência
    if trend == "up":
        messages.append(
            "A tendência de alta pode resultar em sensação térmica mais elevada."
        )
    elif trend == "down":
        messages.append(
            "A tendência de queda pode resultar em sensação térmica mais amena."
        )

    return " ".join(messages)

