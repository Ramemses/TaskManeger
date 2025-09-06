from pydantic import BaseModel, EmailStr,  ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr


class CreateUser(UserBase):

    is_active:bool
    password: bytes

class UserRegister(UserBase):
    password1: str
    password2: str
    

class UserUpdate(BaseModel):
    username: Optional[str] = None
    emial: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserToken(UserBase):
    is_active: bool

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime


    class Config:
        from_attributes = True