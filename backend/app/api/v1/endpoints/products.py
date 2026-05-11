import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.deps import get_db, get_current_admin_user
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import (
    list_products as svc_list, get_product as svc_get,
    create_product as svc_create, update_product as svc_update, delete_product as svc_delete,
)

router = APIRouter()


@router.get("/", response_model=List[ProductRead])
def list_products(
    category_id: Optional[uuid.UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return svc_list(db, category_id=category_id, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    product = svc_get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin_user),
):
    return svc_create(db, product_in)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: uuid.UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin_user),
):
    product = svc_get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return svc_update(db, product, product_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin_user),
):
    product = svc_get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    svc_delete(db, product)
