from .db.db import get_connection


def create_chat(user_id: int, title: str = None) -> int:
    """Crea un nuevo chat para el usuario y devuelve su id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO chat (user_id, title) VALUES (?, ?)", (user_id, title)
        )
        return cursor.lastrowid


def list_chats(user_id: int) -> list[dict]:
    """Devuelve todos los chats de un usuario, del más reciente al más antiguo."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM chat WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def get_chat(chat_id: int) -> dict | None:
    """Devuelve un chat por id, o None si no existe."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM chat WHERE id = ?", (chat_id,)
        ).fetchone()
        return dict(row) if row else None


def update_chat_title(chat_id: int, title: str) -> None:
    """Actualiza el título de un chat (útil para asignarlo con el primer mensaje)."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE chat SET title = ? WHERE id = ?", (title, chat_id)
        )


def delete_chat(chat_id: int) -> None:
    """Elimina un chat y todos sus mensajes (CASCADE)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM chat WHERE id = ?", (chat_id,))
