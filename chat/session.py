import persistance
from agent import PilotoAgent

class ChatSessionManager:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.agent = PilotoAgent()
        self.chat_session = None
        self.load_session()

    def load_session(self):
        db_messages = persistance.get_messages(self.chat_id)
        self.chat_session = self.agent.iniciar_sesion_chat(db_messages)

    def send_message(self, text: str) -> str:
        persistance.save_message(self.chat_id, "user", text)
        response = self.agent.obtener_respuesta(self.chat_session, text)
        persistance.save_message(self.chat_id, "assistant", response)
        return response

    def clear_history(self):
        persistance.delete_messages(self.chat_id)
        self.chat_session = self.agent.iniciar_sesion_chat([])
