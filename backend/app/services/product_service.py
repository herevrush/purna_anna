import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session, category_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 20) -> List[Product]:
    q = db.query(Product).filter(Product.is_active.is_(True))
    if category_id is not None:
        q = q.filter(Product.category_id == category_id)
    return q.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: uuid.UUID) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, product_in: ProductUpdate) -> Product:
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
