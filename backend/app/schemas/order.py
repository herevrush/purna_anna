import uuid
from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal


class OrderItemRead(OrderItemBase):
    id: uuid.UUID
    order_id: uuid.UUID
    model_config = {"from_attributes": True}


class OrderBase(BaseModel):
    status: str = "pending"
    total: Decimal


class OrderRead(OrderBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    items: List[OrderItemRead] = []
    model_config = {"from_attributes": True}
