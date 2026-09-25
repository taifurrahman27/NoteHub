from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=5)
    author: str = Field(min_length=2)


class NoteUpdate(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=5)


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    