from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    name: str = Field(max_length=50, default='Default')
    surname: str = Field(max_length=50, default='Contact')
    email: EmailStr
    phone: str = Field(max_length=50, default='+421000000000')
    born_date: datetime


class ContactResponse(ContactBase):
    name: str
    surname: str
    email: EmailStr
    phone: str
    born_date: datetime

    class Config:
        orm_mode = True


class ContactUpdate(ContactBase):
    done: bool

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr