from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int = 0
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
