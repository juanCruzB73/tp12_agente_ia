import sys
import utils.config
import persistance
from chat import ChatSessionManager, handle_command
from utils.error_handler import handle_api_error


def main():
    persistance.init_db()
    user_id = persistance.get_default_user()

    chats = persistance.list_chats(user_id)
    if chats:
        print("Conversaciones disponibles:")
        print("0. Iniciar una nueva conversación")
        for i, chat in enumerate(chats, 1):
            title = chat["title"] if chat["title"] else f"Conversación {chat['id']}"
            ultima = persistance.get_last_session(chat["id"])
            if ultima:
                print(f"{i}. {title}  (última sesión: {ultima['started_at']})")
            else:
                print(f"{i}. {title}  (creada: {chat['created_at']})")

        try:
            choice = input("Seleccione una opción: ").strip()
            idx = int(choice)
            if idx == 0:
                chat_id = persistance.create_chat(user_id, None)
            elif 1 <= idx <= len(chats):
                chat_id = chats[idx - 1]["id"]
            else:
                print("Opción inválida. Iniciando nueva conversación.")
                chat_id = persistance.create_chat(user_id, None)
        except ValueError:
            print("Entrada inválida. Iniciando nueva conversación.")
            chat_id = persistance.create_chat(user_id, None)
    else:
        chat_id = persistance.create_chat(user_id, None)

    session_manager = ChatSessionManager(chat_id)
    session_id = persistance.start_session(chat_id)

    print("\n=============================================")
    print("¡Bienvenido a CodeTutor! (Escribí /salir para terminar o /limpiar para reiniciar)")
    print("=============================================\n")

    is_first_message = len(persistance.get_messages(chat_id)) == 0
    nombre = persistance.get_user(user_id)["name"]

    if is_first_message:
        print("\n=============================================")
        print("¡Bienvenido a CodeTutor! Tu Agente para aprender Programación!")
        print("Comando utiles durante nuestras sesiones: /salir para terminar | /limpiar para reiniciar")
        print("Antes de empezar, ¿cómo te gustaría que te llame?")
        print("=============================================\n")
        nombre_input = input("Usuario: ").strip()
        if nombre_input:
            nombre = nombre_input
            persistance.update_user_name(user_id, nombre)
        print(f"\nPiloto: ¡Hola {nombre}! ¿En qué te puedo ayudar hoy?\n")
    else:
        chat_info = persistance.get_chat(chat_id)
        if chat_info and chat_info["title"]:
            print(f"[Sesión: {chat_info['title']}]\n")

    try:
        while True:
            try:
                user_input = input("Usuario: ").strip()
                if not user_input:
                    continue

                if handle_command(user_input, session_manager):
                    continue

                response = session_manager.send_message(user_input)

                if is_first_message:
                    titulo = session_manager.agent.generar_titulo(nombre, user_input)
                    titulo_completo = f"{nombre} — {titulo}"
                    persistance.update_chat_title(chat_id, titulo_completo)
                    print(f"\n[Sesión: {titulo_completo}]")
                    is_first_message = False

                print(f"\nPiloto: {response}\n")

            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                sys.exit(0)
            except Exception as e:
                error_msg = handle_api_error(e)
                print(f"\n{error_msg}\n")
    finally:
        persistance.end_session(session_id, chat_id)


if __name__ == "__main__":
    main()
