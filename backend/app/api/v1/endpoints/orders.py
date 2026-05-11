import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_active_user
from app.models.cart import CartItem
from app.models.user import User
from app.schemas.order import OrderRead
from app.services.order_service import checkout as svc_checkout, list_orders as svc_list, get_order as svc_get

router = APIRouter()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return svc_checkout(db, current_user.id, cart_items)


@router.get("/", response_model=List[OrderRead])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return svc_list(db, current_user.id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    order = svc_get(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
