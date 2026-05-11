from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db, get_current_active_user
from app.models.cart import CartItem
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemRead, CartItemUpdate

router = APIRouter()


@router.get("/", response_model=List[CartItemRead])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(CartItem).filter(CartItem.user_id == current_user.id).all()


@router.post("/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id, CartItem.product_id == item_in.product_id)
        .first()
    )
    if existing:
        existing.quantity += item_in.quantity
        db.commit()
        db.refresh(existing)
        return existing
    item = CartItem(user_id=current_user.id, **item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/items/{item_id}", response_model=CartItemRead)
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = item_in.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
