import uuid
from typing import List
from sqlalchemy.orm import Session
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate


def get_cart(db: Session, user_id: uuid.UUID) -> List[CartItem]:
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


def add_item(db: Session, user_id: uuid.UUID, item_in: CartItemCreate) -> CartItem:
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id, CartItem.product_id == item_in.product_id
    ).first()
    if existing:
        existing.quantity += item_in.quantity
        db.commit()
        db.refresh(existing)
        return existing
    item = CartItem(user_id=user_id, **item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: CartItem, quantity: int) -> CartItem:
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def remove_item(db: Session, item: CartItem) -> None:
    db.delete(item)
    db.commit()


def clear_cart(db: Session, user_id: uuid.UUID) -> None:
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
