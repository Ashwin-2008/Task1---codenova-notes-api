from datetime import datetime, timezone

from app.database import get_connection
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


def current_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def row_to_note(row) -> Note:
    return Note(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def list_notes() -> list[Note]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM notes ORDER BY id"
        ).fetchall()

    return [row_to_note(row) for row in rows]


def get_note(note_id: int) -> Note | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()

    return row_to_note(row) if row else None


def create_note(data: NoteCreate) -> Note:
    now = current_time()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notes (title, content, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (data.title, data.content, now, now),
        )

        row = connection.execute(
            "SELECT * FROM notes WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return row_to_note(row)


def update_note(
    note_id: int,
    data: NoteUpdate,
) -> Note | None:
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()

        if existing is None:
            return None

        connection.execute(
            """
            UPDATE notes
            SET title = ?, content = ?, updated_at = ?
            WHERE id = ?
            """,
            (data.title, data.content, current_time(), note_id),
        )

        row = connection.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()

    return row_to_note(row)


def delete_note(note_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,),
        )

    return cursor.rowcount > 0