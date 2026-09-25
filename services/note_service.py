from sqlalchemy import select
from sqlalchemy.orm import Session

from models.note import Note


def get_notes(db: Session):
    return db.scalars(select(Note)).all()


def get_note(db: Session, note_id: int):
    return db.get(Note, note_id)


def create_note(db: Session, title: str, content: str, author: str):
    note = Note(
        title=title,
        content=content,
        author=author,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def update_note(
    db: Session,
    note_id: int,
    title: str,
    content: str,
):
    note = db.get(Note, note_id)

    if note is None:
        return None

    note.title = title
    note.content = content

    db.commit()
    db.refresh(note)

    return note


def delete_note(db: Session, note_id: int):
    note = db.get(Note, note_id)

    if note is None:
        return False

    db.delete(note)
    db.commit()

    return True