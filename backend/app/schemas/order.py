from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderItemRead(OrderItemBase):
    id: int
    order_id: int

    model_config = {"from_attributes": True}


class OrderBase(BaseModel):
    status: str = "pending"
    total: Decimal


class OrderRead(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemRead] = []

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    pass  # checkout is derived from cart
