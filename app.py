from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.note import NoteCreate, NoteUpdate, NoteResponse
from services.note_service import (
    get_notes,
    create_note,
    get_note,
    update_note,
    delete_note,
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "NoteHub API is running"}


@app.get("/notes", response_model=list[NoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    return get_notes(db)


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note(db, note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


@app.post("/notes", response_model=NoteResponse)
def create_new_note(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note(
        db,
        note.title,
        note.content,
        note.author,
    )


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db),
):
    updated_note = update_note(
        db,
        note_id,
        note.title,
        note.content,
    )

    if updated_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return updated_note


@app.delete("/notes/{note_id}")
def delete_existing_note(
    note_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_note(db, note_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return {"message": "Note deleted successfully"}
