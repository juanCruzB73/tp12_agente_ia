import sqlite3
import os

# El archivo .db se guarda en la misma carpeta que este módulo
DB_PATH = os.path.join(os.path.dirname(__file__), "piloto.db")


def get_connection() -> sqlite3.Connection:
    """Devuelve una conexión a SQLite con row_factory y foreign keys activas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Crea las tablas si no existen. Debe llamarse una vez al arrancar la app."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS user (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                created_at TEXT    DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS chat (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                title      TEXT,
                created_at TEXT    DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS message (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id    INTEGER NOT NULL,
                role       TEXT    NOT NULL,
                content    TEXT    NOT NULL,
                created_at TEXT    DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS session (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id    INTEGER,
                started_at TEXT    DEFAULT (datetime('now', 'localtime')),
                ended_at   TEXT,
                FOREIGN KEY (chat_id) REFERENCES chat(id)
            );
        """)
