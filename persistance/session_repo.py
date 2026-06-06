from .db.db import get_connection


def start_session(chat_id: int = None) -> int:
    """Registra el inicio de una nueva sesión y devuelve su id.

    Args:
        chat_id: id del chat que se retoma, o None si es una conversación nueva.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO session (chat_id) VALUES (?)", (chat_id,)
        )
        return cursor.lastrowid


def end_session(session_id: int, chat_id: int = None) -> None:
    """Marca el fin de una sesión guardando la hora de cierre.

    Args:
        session_id: id de la sesión a cerrar.
        chat_id:    id del chat activo al cierre (por si se asignó durante la sesión).
    """
    with get_connection() as conn:
        conn.execute(
            """UPDATE session
               SET ended_at = datetime('now', 'localtime'),
                   chat_id  = COALESCE(?, chat_id)
               WHERE id = ?""",
            (chat_id, session_id),
        )


def get_session(session_id: int) -> dict | None:
    """Devuelve una sesión por id, o None si no existe."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(row) if row else None


def list_sessions() -> list[dict]:
    """Devuelve todas las sesiones registradas, de la más reciente a la más antigua."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM session ORDER BY started_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
