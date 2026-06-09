import google.generativeai as genai
import os

class PilotoAgent:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno.")
        
        genai.configure(api_key=api_key)

        # System prompt
        self.system_instruction = (
            "Sos un profesor de programación y tu nombre es Piloto. "
            "Respondés siempre en español y con un tono conciso, amigable pero profesional. "
            "Tu tarea es sólo responder preguntas relacionadas a la programación. "
            "Si te preguntan algo fuera de ese tema o quieren conversar de otra cosa, "
            "amablemente redirigís la conversación a tu especialidad y le solicitas al usuario que haga una pregunta de programación. "
            "Nunca entregues código que pueda ser dañino para la pc o el usuario."
        )

        # Inicializar el modelo Gemini 1.5 Flash
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.system_instruction
        )

    # Si hay historial lo carga, si no empieza vacío
    def iniciar_sesion_chat(self, historial_previo=None):
        historial = historial_previo if historial_previo else []
        return self.model.start_chat(history=historial)

    def obtener_respuesta(self, chat_session, mensaje_usuario):
        respuesta = chat_session.send_message(mensaje_usuario)
        return respuesta.text