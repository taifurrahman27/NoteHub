from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models.user import User
from schemas.note import NoteCreate, NoteUpdate, NoteResponse
from schemas.user import UserCreate, UserResponse, Token
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)
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


@app.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/notes", response_model=list[NoteResponse])
def get_all_notes(
    db: Session = Depends(get_db),
):
    return get_notes(db)


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_single_note(
    note_id: int,
    db: Session = Depends(get_db),
):
    note = get_note(db, note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


@app.post("/notes", response_model=NoteResponse)
def create_new_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    deleted = delete_note(db, note_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return {"message": "Note deleted successfully"}
