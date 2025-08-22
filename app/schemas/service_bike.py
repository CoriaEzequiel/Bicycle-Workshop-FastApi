from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ServiceBikeBase(BaseModel):
    user_id: int
    bike_model: str
    bike_brand: str
    status: Optional[ServiceStatus] = ServiceStatus.PENDING
    reserved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class ServiceBikeCreate(ServiceBikeBase):
    pass

class ServiceBikeUpdate(BaseModel):
    status: Optional[ServiceStatus] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class ServiceBikeRead(ServiceBikeBase):
    id: int
    class Config:
        orm_mode = True
