from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    category_id: int

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemRead(MenuItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)