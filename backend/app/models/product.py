from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
