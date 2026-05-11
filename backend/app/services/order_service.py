import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cart import CartItem
from app.models.order import Order, OrderItem


def checkout(db: Session, user_id: uuid.UUID, cart_items: List[CartItem]) -> Order:
    for item in cart_items:
        if item.product is None:
            raise HTTPException(status_code=422, detail="A product in your cart is no longer available")
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user_id=user_id, total=total, status="pending")
    db.add(order)
    db.flush()
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
        )
        db.add(order_item)
        item.product.stock_quantity -= item.quantity
        db.add(item.product)
        db.delete(item)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
