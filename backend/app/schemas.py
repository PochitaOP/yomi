from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    message: str

class MessageIn(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    user_id: int
    user : UserOut
    time_created: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
