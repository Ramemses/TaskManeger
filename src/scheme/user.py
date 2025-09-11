from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr


class CreateUser(UserBase):
    is_active: bool
    password: bytes


class RegistrationUser(UserBase):
    password1: str
    password2: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[bytes] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    hashed_password: bytes

    class Config:
        from_attributes = True


