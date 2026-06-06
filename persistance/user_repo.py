from .db.db import get_connection


def create_user(name: str) -> int:
    """Crea un usuario nuevo y devuelve su id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO user (name) VALUES (?)", (name,)
        )
        return cursor.lastrowid


def get_user(user_id: int) -> dict | None:
    """Devuelve un usuario por id, o None si no existe."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None


def get_or_create_user(name: str) -> int:
    """Devuelve el id del primer usuario con ese nombre, o lo crea si no existe."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM user WHERE name = ? LIMIT 1", (name,)
        ).fetchone()
        if row:
            return row["id"]
        cursor = conn.execute("INSERT INTO user (name) VALUES (?)", (name,))
        return cursor.lastrowid
