from .db.db import get_connection


def save_message(chat_id: int, role: str, content: str) -> int:
    """Guarda un mensaje en la base de datos y devuelve su id.

    Args:
        chat_id: id del chat al que pertenece el mensaje.
        role:    'user' o 'assistant' (valores que espera la API de Anthropic).
        content: texto del mensaje.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO message (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content),
        )
        return cursor.lastrowid


def get_messages(chat_id: int) -> list[dict]:
    """Devuelve el historial de un chat en formato listo para la API de Anthropic.

    Cada elemento tiene las claves 'role' y 'content', en orden cronológico.
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT role, content FROM message WHERE chat_id = ? ORDER BY created_at ASC",
            (chat_id,),
        ).fetchall()
        return [{"role": row["role"], "content": row["content"]} for row in rows]


def delete_messages(chat_id: int) -> None:
    """Elimina todos los mensajes de un chat (útil para /limpiar si se persiste)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM message WHERE chat_id = ?", (chat_id,))
