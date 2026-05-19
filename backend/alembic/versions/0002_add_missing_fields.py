"""add missing fields

Revision ID: 0002_add_missing_fields
Revises: 0001_initial_schema
Create Date: 2024-01-02 00:00:00.000000

No-op placeholder for teams that already ran the original 0001 scaffold.
Adds the 5 new columns introduced in the corrected 0001:
  - users.full_name
  - users.is_admin
  - users.refresh_token
  - categories.parent_id
  - products.slug
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_add_missing_fields"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users: full_name
    
    #op.add_column("users", sa.Column("full_name", sa.String(), nullable=True))
    

    # users: is_admin
    
    #op.add_column(
    #        "users",
    #        sa.Column("is_admin", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    #    )
   

    # users: refresh_token
    
    #op.add_column("users", sa.Column("refresh_token", sa.String(), nullable=True))
    

    # categories: parent_id (self-referencing FK)
    
    #op.add_column("categories", sa.Column("parent_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
            "fk_categories_parent_id",
            "categories",
            "categories",
            ["parent_id"],
            ["id"],
            ondelete="SET NULL",
        )
    

    # products: slug
    
    #op.add_column("products", sa.Column("slug", sa.String(), nullable=True))
        # Allow NULL during backfill; teams must populate slug before adding NOT NULL constraint.
    


def downgrade() -> None:
    try:
        op.drop_column("products", "slug")
    except Exception:
        pass

    try:
        op.drop_constraint("fk_categories_parent_id", "categories", type_="foreignkey")
        op.drop_column("categories", "parent_id")
    except Exception:
        pass

    try:
        op.drop_column("users", "refresh_token")
    except Exception:
        pass

    try:
        op.drop_column("users", "is_admin")
    except Exception:
        pass

    try:
        op.drop_column("users", "full_name")
    except Exception:
        pass
