import sys

def handle_command(command: str, session_manager) -> bool:
    cmd = command.strip().lower()
    if cmd == "/salir":
        print("¡Hasta luego!")
        sys.exit(0)
    elif cmd == "/limpiar":
        session_manager.clear_history()
        print("Historial de conversación limpiado.")
        return True
    return False
