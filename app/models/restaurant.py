from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)

    # Связь: Один ресторан -> Много столов
    tables: Mapped[List["Table"]] = relationship("Table", back_populates="restaurant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Restaurant(name={self.name})>"

class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False) # Номер стола в заведении
    capacity: Mapped[int] = mapped_column(Integer, default=2)    # Вместимость (чел)
    
    # Внешний ключ на ресторан
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    
    # Обратная связь
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="tables")

    def __repr__(self) -> str:
        return f"<Table(number={self.number}, restaurant_id={self.restaurant_id})>"