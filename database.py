from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.note import Note

DATABASE_URL = "postgresql+psycopg://postgres:REMOVED_PASSWORD@localhost/notehub"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base.metadata.create_all(engine)




def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


with SessionLocal() as db:
    note = Note(
        title="Database Test",
        content="This note is stored in PostgreSQL.",
        author="Taifur",
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    print(note.id)

