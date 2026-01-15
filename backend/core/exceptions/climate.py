
class ClimateServiceError(Exception):
    """Erro genérico do serviço climático"""
    pass


class CityNotFoundError(ClimateServiceError):
    """Cidade não encontrada na API"""
    pass


class ClimateAPIAuthError(ClimateServiceError):
    """Erro de autenticação com a API climática"""
    pass


class ClimateAPIUnavailableError(ClimateServiceError):
    """API climática indisponível"""
    pass
