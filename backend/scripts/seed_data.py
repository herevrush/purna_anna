#!/usr/bin/env python3
"""Seed the database with initial categories, products, and a demo user."""

import os
import sys
import uuid
from decimal import Decimal

from passlib.context import CryptContext
from sqlalchemy import create_engine, text
import hashlib

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/purna"
)

pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

CATEGORIES = [
    {"id": str(uuid.uuid4()), "name": "Produce", "slug": "produce", "description": "Fresh fruits and vegetables"},
    {"id": str(uuid.uuid4()), "name": "Dairy", "slug": "dairy", "description": "Milk, cheese, eggs, and more"},
    {"id": str(uuid.uuid4()), "name": "Bakery", "slug": "bakery", "description": "Freshly baked breads and pastries"},
    {"id": str(uuid.uuid4()), "name": "Meat", "slug": "meat", "description": "Fresh and frozen meats"},
    {"id": str(uuid.uuid4()), "name": "Beverages", "slug": "beverages", "description": "Drinks and juices"},
]

# Build a slug→id lookup for product FK assignment
_cat = {c["slug"]: c["id"] for c in CATEGORIES}

def _slugify(name: str) -> str:
    """Convert a product/category name to a URL-safe slug."""
    import re
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


PRODUCTS = [
    # Produce
    {"id": str(uuid.uuid4()), "name": "Organic Bananas", "slug": "organic-bananas", "description": "Bunch of ripe organic bananas", "price": Decimal("1.49"), "stock_quantity": 200, "category_id": _cat["produce"], "image_url": None, "is_active": True},
    {"id": str(uuid.uuid4()), "name": "Baby Spinach", "slug": "baby-spinach", "description": "Pre-washed baby spinach, 5oz bag", "price": Decimal("3.99"), "stock_quantity": 80, "category_id": _cat["produce"], "image_url": None, "is_active": True},
    # Dairy
    {"id": str(uuid.uuid4()), "name": "Whole Milk", "slug": "whole-milk", "description": "Organic whole milk, 1 gallon", "price": Decimal("5.49"), "stock_quantity": 60, "category_id": _cat["dairy"], "image_url": None, "is_active": True},
    {"id": str(uuid.uuid4()), "name": "Cheddar Cheese", "slug": "cheddar-cheese", "description": "Sharp cheddar, 8oz block", "price": Decimal("4.29"), "stock_quantity": 90, "category_id": _cat["dairy"], "image_url": None, "is_active": True},
    # Bakery
    {"id": str(uuid.uuid4()), "name": "Sourdough Loaf", "slug": "sourdough-loaf", "description": "Classic sourdough, whole loaf", "price": Decimal("6.99"), "stock_quantity": 30, "category_id": _cat["bakery"], "image_url": None, "is_active": True},
    {"id": str(uuid.uuid4()), "name": "Blueberry Muffins", "slug": "blueberry-muffins", "description": "Pack of 4 blueberry muffins", "price": Decimal("4.49"), "stock_quantity": 40, "category_id": _cat["bakery"], "image_url": None, "is_active": True},
    # Meat
    {"id": str(uuid.uuid4()), "name": "Chicken Breast", "slug": "chicken-breast", "description": "Boneless skinless chicken breast, 1 lb", "price": Decimal("7.99"), "stock_quantity": 50, "category_id": _cat["meat"], "image_url": None, "is_active": True},
    {"id": str(uuid.uuid4()), "name": "Ground Beef 80/20", "slug": "ground-beef-80-20", "description": "Fresh ground beef, 1 lb", "price": Decimal("6.49"), "stock_quantity": 45, "category_id": _cat["meat"], "image_url": None, "is_active": True},
    # Beverages
    {"id": str(uuid.uuid4()), "name": "Orange Juice", "slug": "orange-juice", "description": "100% fresh squeezed orange juice, 52 fl oz", "price": Decimal("5.99"), "stock_quantity": 70, "category_id": _cat["beverages"], "image_url": None, "is_active": True},
    {"id": str(uuid.uuid4()), "name": "Sparkling Water", "slug": "sparkling-water", "description": "Unsweetened sparkling water, 12-pack", "price": Decimal("8.99"), "stock_quantity": 100, "category_id": _cat["beverages"], "image_url": None, "is_active": True},
]

password = "demo1234"
hashed_pw  = hashlib.sha256(password.encode()).hexdigest()

DEMO_USER = {
    "id": str(uuid.uuid4()),
    "email": "demo@purna.dev",
    "hashed_password": pwd_context.hash(hashed_pw),
    "full_name": "Demo User",
    "is_active": True,
}


def seed(engine) -> None:
    with engine.begin() as conn:
        # Categories
        for cat in CATEGORIES:
            conn.execute(
                text(
                    "INSERT INTO categories (id, name, slug, description) "
                    "VALUES (:id, :name, :slug, :description) "
                    "ON CONFLICT (slug) DO NOTHING"
                ),
                cat,
            )
        print(f"  ✓ {len(CATEGORIES)} categories")

        # Products
        for prod in PRODUCTS:
            conn.execute(
                text(
                    "INSERT INTO products "
                    "(id, name, slug, description, price, stock_quantity, category_id, image_url, is_active) "
                    "VALUES (:id, :name, :slug, :description, :price, :stock_quantity, :category_id, :image_url, :is_active) "
                    "ON CONFLICT DO NOTHING"
                ),
                prod,
            )
        print(f"  ✓ {len(PRODUCTS)} products")

        # Demo user
        conn.execute(
            text(
                "INSERT INTO users (id, email, hashed_password, full_name, is_active) "
                "VALUES (:id, :email, :hashed_password, :full_name, :is_active) "
                "ON CONFLICT (email) DO NOTHING"
            ),
            DEMO_USER,
        )
        print(f"  ✓ demo user ({DEMO_USER['email']})")


def main() -> None:
    print(f"Connecting to {DATABASE_URL} ...")
    engine = create_engine(DATABASE_URL)
    print("Seeding data...")
    seed(engine)
    print("Done.")


if __name__ == "__main__":
    main()
