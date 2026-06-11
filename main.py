import sys
import utils.config
import persistance
from chat import ChatSessionManager, handle_command
from utils.error_handler import handle_api_error

def main():
    persistance.init_db()
    user_id = persistance.get_or_create_user("Usuario")
    
    chats = persistance.list_chats(user_id)
    if chats:
        print("Conversaciones disponibles:")
        print("0. Iniciar una nueva conversación")
        for i, chat in enumerate(chats, 1):
            title = chat["title"] if chat["title"] else f"Conversación {chat['id']}"
            print(f"{i}. {title} ({chat['created_at']})")
        
        try:
            choice = input("Seleccione una opción: ").strip()
            idx = int(choice)
            if idx == 0:
                chat_id = persistance.create_chat(user_id, "Nueva conversación")
            elif 1 <= idx <= len(chats):
                chat_id = chats[idx - 1]["id"]
            else:
                print("Opción inválida. Iniciando nueva conversación.")
                chat_id = persistance.create_chat(user_id, "Nueva conversación")
        except ValueError:
            print("Entrada inválida. Iniciando nueva conversación.")
            chat_id = persistance.create_chat(user_id, "Nueva conversación")
    else:
        chat_id = persistance.create_chat(user_id, "Nueva conversación")

    session_manager = ChatSessionManager(chat_id)
    
    print("\n=============================================")
    print("¡Bienvenido a CodeTutor! (Escribí /salir para terminar o /limpiar para reiniciar)")
    print("=============================================\n")

    is_first_message = len(persistance.get_messages(chat_id)) == 0

    while True:
        try:
            user_input = input("Usuario: ").strip()
            if not user_input:
                continue

            if handle_command(user_input, session_manager):
                continue

            response = session_manager.send_message(user_input)
            
            if is_first_message:
                title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                persistance.update_chat_title(chat_id, title)
                is_first_message = False

            print(f"\nPiloto: {response}\n")

        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            sys.exit(0)
        except Exception as e:
            error_msg = handle_api_error(e)
            print(f"\n{error_msg}\n")

if __name__ == "__main__":
    main()