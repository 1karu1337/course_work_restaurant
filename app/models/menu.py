from typing import List, Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Связь: Одна категория -> Много блюд
    items: Mapped[List["MenuItem"]] = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Category(name={self.name})>"

class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Внешний ключ на категорию
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    
    # Обратная связь
    category: Mapped["Category"] = relationship("Category", back_populates="items")

    def __repr__(self) -> str:
        return f"<MenuItem(name={self.name}, price={self.price})>"