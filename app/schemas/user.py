from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    auth0_sub: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True