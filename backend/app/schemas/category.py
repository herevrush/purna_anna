import uuid
from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    parent_id: Optional[uuid.UUID] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None


class CategoryRead(CategoryBase):
    id: uuid.UUID
    parent_id: Optional[uuid.UUID] = None
    model_config = {"from_attributes": True}
