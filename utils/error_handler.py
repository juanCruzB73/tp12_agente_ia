from groq import AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError


def handle_api_error(error: Exception) -> str:
    if isinstance(error, AuthenticationError):
        return "Error: La API Key de Groq es inválida. Revisá tu archivo .env."
    elif isinstance(error, RateLimitError):
        return "Error: Se alcanzó el límite de solicitudes. Esperá un momento e intentalo de nuevo."
    elif isinstance(error, APITimeoutError):
        return "Error: La solicitud excedió el tiempo de espera. Intentalo de nuevo."
    elif isinstance(error, APIConnectionError):
        return "Error: No se pudo conectar al servidor. Revisá tu conexión a internet."
    else:
        return f"Error inesperado: {str(error)}"
