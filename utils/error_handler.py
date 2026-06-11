import google.api_core.exceptions
import requests

def handle_api_error(error: Exception) -> str:
    if isinstance(error, (google.api_core.exceptions.PermissionDenied, google.api_core.exceptions.Unauthenticated)):
        return "Error: La API Key de Gemini es inválida o no tiene permisos. Por favor, revisá tu archivo .env."
    elif isinstance(error, google.api_core.exceptions.ResourceExhausted):
        return "Error: Se alcanzó el límite de solicitudes (Rate Limit). Esperá un momento e intentalo de nuevo."
    elif isinstance(error, google.api_core.exceptions.DeadlineExceeded):
        return "Error: La solicitud a la API de Gemini excedió el tiempo de espera (Timeout). Intentalo de nuevo."
    elif isinstance(error, (google.api_core.exceptions.ServiceUnavailable, requests.RequestException)):
        return "Error: No se pudo establecer conexión con el servidor. Revisá tu conexión a internet."
    else:
        return f"Error de conexión o API: {str(error)}"
