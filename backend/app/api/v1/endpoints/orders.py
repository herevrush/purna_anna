from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db, get_current_active_user
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderRead

router = APIRouter()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user_id=current_user.id, total=total, status="pending")
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
        db.delete(item)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
