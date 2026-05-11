import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_active_user
from app.models.cart import CartItem
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemRead, CartItemUpdate
from app.services.cart_service import get_cart as svc_get_cart, add_item, update_item, remove_item

router = APIRouter()


@router.get("/", response_model=List[CartItemRead])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return svc_get_cart(db, current_user.id)


@router.post("/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return add_item(db, current_user.id, item_in)


@router.put("/items/{item_id}", response_model=CartItemRead)
def update_cart_item(
    item_id: uuid.UUID,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return update_item(db, item, item_in.quantity)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    remove_item(db, item)
