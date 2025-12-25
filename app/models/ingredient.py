from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class MenuItemIngredient(Base):
    """Промежуточная таблица для рецептов (Many-to-Many с данными)"""
    __tablename__ = "menu_item_ingredients"

    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id", ondelete="CASCADE"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True
    )
    # Сколько конкретно этого ингредиента нужно для одного блюда (например, 0.5 кг)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Связи для удобного доступа
    menu_item: Mapped["MenuItem"] = relationship(back_populates="ingredient_links")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="menu_item_links")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False) # г, мл, шт
    stock_quantity: Mapped[float] = mapped_column(Float, default=0.0) # Остаток на складе

    # Связь с рецептами
    menu_item_links: Mapped[list["MenuItemIngredient"]] = relationship(
        back_populates="ingredient"
    )

    def __repr__(self) -> str:
        return f"<Ingredient(name={self.name}, stock={self.stock_quantity})>"