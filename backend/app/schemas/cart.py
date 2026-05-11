from pydantic import BaseModel
from typing import Optional

from app.schemas.product import ProductRead


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(CartItemBase):
    id: int
    user_id: int
    product: Optional[ProductRead] = None

    model_config = {"from_attributes": True}
