import uuid
from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductRead


class CartItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(CartItemBase):
    id: uuid.UUID
    user_id: uuid.UUID
    product: Optional[ProductRead] = None
    model_config = {"from_attributes": True}
