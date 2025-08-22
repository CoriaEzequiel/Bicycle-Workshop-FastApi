from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class AppointmentBase(BaseModel):
    user_id: int
    product_id: int
    status: Optional[AppointmentStatus] = AppointmentStatus.PENDING
    reserved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class AppointmentRead(AppointmentBase):
    id: int
    class Config:
        orm_mode = True
