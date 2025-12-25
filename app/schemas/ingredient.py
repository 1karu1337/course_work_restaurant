from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class IngredientBase(BaseModel):
    name: str
    unit: str
    stock_quantity: float = 0.0

class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class RecipeLinkCreate(BaseModel):
    menu_item_id: int
    ingredient_id: int
    amount: float

class RecipeRead(BaseModel):
    ingredient_id: int
    ingredient_name: str
    amount: float
    unit: str
    model_config = ConfigDict(from_attributes=True)