from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from models.order import OrderStatus

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    table_id: Optional[int] = None
    items: List[OrderItemBase]

class OrderItemRead(BaseModel):
    menu_item_id: int
    quantity: int
    price_at_order: float

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    user_id: int
    table_id: Optional[int]
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)