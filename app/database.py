import os
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "notes.db")
).resolve()


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
                    CHECK(length(trim(title)) BETWEEN 1 AND 200),
                content TEXT NOT NULL
                    CHECK(length(content) BETWEEN 1 AND 10000),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)