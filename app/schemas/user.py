from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from app.schemas.role import RoleRead

class UserBase(BaseModel):
    auth0_sub: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class UserRead(UserBase):
    id: int
    roles: List[RoleRead] = []
    model_config = ConfigDict(from_attributes=True)
