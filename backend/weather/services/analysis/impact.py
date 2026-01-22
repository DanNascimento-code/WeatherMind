from typing import Dict


def assess_temperature_impact(analysis: Dict[str, str]) -> Dict[str, str]:
    trend = analysis.get("trend")
    variation = analysis.get("variation")
    stability = analysis.get("stability")

    if trend == "insufficient_data":
        return {
            "health": "Não é possível avaliar o impacto na saúde no momento por falta de dados.",
            "comfort": "Não é possível avaliar o conforto no momento por falta de dados."
        }

    health_messages = []
    comfort_messages = []

    # Impacto da variação
    if variation == "high":
        comfort_messages.append(
            "A alta variação de temperatura pode causar desconforto térmico ao longo do período."
        )
        health_messages.append(
            "Variações extremas podem afetar a saúde, especialmente de grupos vulneráveis."
        )
    elif variation == "moderate":
        comfort_messages.append(
            "A variação moderada de temperatura pode ser perceptível ao longo do dia."
        )
        health_messages.append(
            "Variações moderadas geralmente não apresentam risco à saúde."
        )
    else:
        comfort_messages.append(
            "A baixa variação de temperatura tende a proporcionar maior conforto térmico."
        )
        health_messages.append(
            "Temperaturas estáveis favorecem o bem-estar e a saúde."
        )

    # Impacto da estabilidade
    if stability == "unstable":
        health_messages.append(
            "Mudanças bruscas podem indicar risco à saúde e exigem maior atenção."
        )
    else:
        health_messages.append(
            "As mudanças graduais indicam um ambiente mais previsível e seguro."
        )

    # Impacto da tendência
    if trend == "up":
        comfort_messages.append(
            "A tendência de alta pode resultar em sensação térmica mais elevada."
        )
        health_messages.append(
            "Aumento de temperatura pode aumentar risco de desidratação."
        )
    elif trend == "down":
        comfort_messages.append(
            "A tendência de queda pode resultar em sensação térmica mais amena."
        )
        health_messages.append(
            "Redução de temperatura aumenta risco de hipotermia em grupos vulneráveis."
        )

    return {
        "health": " ".join(health_messages),
        "comfort": " ".join(comfort_messages)
    }

