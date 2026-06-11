import google.generativeai as genai
from utils.config import GEMINI_API_KEY

class PilotoAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno.")
        
        genai.configure(api_key=GEMINI_API_KEY)

        self.system_instruction = (
            "Sos un profesor de programación y tu nombre es Piloto. "
            "Respondés siempre en español y con un tono conciso, amigable pero profesional. "
            "Tu tarea es sólo responder preguntas relacionadas a la programación. "
            "Si te preguntan algo fuera de ese tema o quieren conversar de otra cosa, "
            "amablemente redirigís la conversación a tu especialidad y le solicitas al usuario que haga una pregunta de programación. "
            "Nunca entregues código que pueda ser dañino para la pc o el usuario."
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=self.system_instruction
        )

    def iniciar_sesion_chat(self, historial_previo=None):
        historial = historial_previo if historial_previo else []
        return self.model.start_chat(history=historial)

    def obtener_respuesta(self, chat_session, mensaje_usuario):
        respuesta = chat_session.send_message(mensaje_usuario)
        return respuesta.text
