from pydantic import BaseModel, EmailStr
from datetime import datetime

# ----- User schemas -----

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# ----- Token schemas -----

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


# Note creation schema
class NoteCreate(BaseModel):
    title: str
    content: str

# Note response schema
class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
