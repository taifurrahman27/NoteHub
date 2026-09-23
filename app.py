from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


@app.get("/notes")
def get_all_notes():
    return get_notes()


@app.get("/notes/{note_id}")
def get_single_note(note_id: int):
    note = get_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


class NoteCreate(BaseModel):
    title: str
    content: str
    author: str


@app.post("/notes")
def create_new_note(note: NoteCreate):
    return create_note(
        note.title,
        note.content,
        note.author,
    )


class NoteUpdate(BaseModel):
    title: str
    content: str


@app.put("/notes/{note_id}")
def update_existing_note(note_id: int, note: NoteUpdate):
    return update_note(
        note_id,
        note.title,
        note.content,
    )


@app.delete("/notes/{note_id}")
def delete_existing_note(note_id: int):
    return delete_note(note_id)
