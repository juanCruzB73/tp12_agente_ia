import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY
from tools.code_runner import ejecutar_codigo
from tools.doc_search import buscar_documentacion

_TOOL_MAP = {
    "ejecutar_codigo": ejecutar_codigo,
    "buscar_documentacion": buscar_documentacion,
}

_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "ejecutar_codigo",
            "description": "Ejecuta un fragmento de código Python y devuelve el output o error producido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "El código Python a ejecutar."
                    }
                },
                "required": ["codigo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_documentacion",
            "description": "Busca la documentación oficial de Python para un módulo, función o clase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "El módulo, función o clase de Python a documentar (ej: 'len', 'os.path', 'list')."
                    }
                },
                "required": ["termino"]
            }
        }
    }
]

SYSTEM_PROMPT = (
    "Sos un profesor de programación y tu nombre es Piloto. "
    "Respondés siempre en español y con un tono conciso, amigable pero profesional. "
    "Tu tarea es sólo responder preguntas relacionadas a la programación. "
    "Si te preguntan algo fuera de ese tema o quieren conversar de otra cosa, "
    "amablemente redirigís la conversación a tu especialidad y le solicitas al usuario que haga una pregunta de programación. "
    "Nunca entregues código que pueda ser dañino para la pc o el usuario. "
    "Cuando el usuario te pida ejecutar código, SIEMPRE usá la herramienta ejecutar_codigo. "
    "Después de ejecutar el código, en tu respuesta SIEMPRE incluí: "
    "1) el código ejecutado dentro de un bloque ```python ... ``` "
    "2) el resultado o error obtenido. "
    "Cuando des ejemplos de código, SIEMPRE incluí el código completo dentro de un bloque ```python ... ```. "
    "Cuando el usuario pregunte sobre una función, módulo o clase de Python usá buscar_documentacion."
)

_FUNCION_PATTERN = re.compile(r'<function=\w+>.*?</function>', re.DOTALL)


def _limpiar_respuesta(texto: str) -> str:
    return _FUNCION_PATTERN.sub('', texto).strip()


class PilotoAgent:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("No se encontró GROQ_API_KEY en las variables de entorno.")
        self.client = Groq(api_key=GROQ_API_KEY)

    def iniciar_sesion_chat(self, historial_previo=None):
        return list(historial_previo or [])

    def generar_titulo(self, nombre: str, primer_mensaje: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": (
                    f"Generá un título corto (máximo 5 palabras, sin comillas ni puntuación final) "
                    f"para una sesión de tutoreo de programación donde el estudiante preguntó: '{primer_mensaje}'. "
                    f"Solo respondé con el título."
                )
            }],
            max_tokens=20,
        )
        return response.choices[0].message.content.strip()

    def obtener_respuesta(self, historial: list, mensaje_usuario: str) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + historial + [{"role": "user", "content": mensaje_usuario}]

        while True:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=_TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            if not msg.tool_calls:
                texto = _limpiar_respuesta(msg.content or "")
                historial.append({"role": "user", "content": mensaje_usuario})
                historial.append({"role": "assistant", "content": texto})
                return texto

            # El modelo quiere llamar una herramienta — la ejecutamos y le devolvemos el resultado
            messages.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in msg.tool_calls
                ]
            })

            for tool_call in msg.tool_calls:
                func = _TOOL_MAP.get(tool_call.function.name)
                args = json.loads(tool_call.function.arguments)
                resultado = func(**args) if func else f"Herramienta '{tool_call.function.name}' no encontrada."
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(resultado),
                })
