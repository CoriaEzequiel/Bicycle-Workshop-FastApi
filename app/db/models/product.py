from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120))
    overview: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50))
    size: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(50))
    stock: Mapped[bool] = mapped_column(Boolean, default=True)
    price: Mapped[float] = mapped_column(Float)

    # futura relación con órdenes/pedidos, podría usar:
    # orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")
