from pydantic import BaseModel, ConfigDict

class TableBase(BaseModel):
    number: int
    capacity: int
    restaurant_id: int

class TableCreate(TableBase):
    pass

class TableRead(TableBase):
    id: int

    model_config = ConfigDict(from_attributes=True)