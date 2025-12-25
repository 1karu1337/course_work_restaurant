from pydantic import BaseModel, ConfigDict
from typing import Optional

class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantRead(RestaurantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)