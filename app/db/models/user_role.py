# app/db/models/user_role.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from app.db.base import Base
from app.db.models import User

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), primary_key=True)

    
    user: Mapped["User"] = relationship("User", back_populates="roles")