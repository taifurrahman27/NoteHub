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


class NoteCreate(BaseModel):
    title: str
    content: str
    author: str


class NoteUpdate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str


@app.get("/")
def root():
    return {"message": "NoteHub API is running"}


@app.get("/notes", response_model=list[NoteResponse])
def get_all_notes():
    return get_notes()


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int):
    note = get_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


@app.post("/notes", response_model=NoteResponse)
def create_new_note(note: NoteCreate):
    return create_note(
        note.title,
        note.content,
        note.author,
    )


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_existing_note(note_id: int, note: NoteUpdate):
    updated_note = update_note(
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
def delete_existing_note(note_id: int):
    deleted = delete_note(note_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return {"message": "Note deleted successfully"}