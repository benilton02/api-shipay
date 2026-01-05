"""create users table and seed initial data

Revision ID: 7d0ceb273b23
Revises:
Create Date: 2026-01-04 16:01:01.230010
"""

from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, Boolean, DateTime


# revision identifiers, used by Alembic.
revision: str = '7d0ceb273b23'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ============================
    # Tables
    # ============================

    op.create_table(
        'claims',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'user_claims',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('claim_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id']),
        sa.PrimaryKeyConstraint('user_id', 'claim_id'),
        sa.UniqueConstraint('user_id', 'claim_id', name='user_claims_un')
    )

    # ============================
    # Seed data
    # ============================

    roles_table = table(
        'roles',
        column('id', Integer),
        column('description', String),
    )

    claims_table = table(
        'claims',
        column('id', Integer),
        column('description', String),
        column('active', Boolean),
    )

    users_table = table(
        'users',
        column('id', Integer),
        column('name', String),
        column('email', String),
        column('password', String),
        column('role_id', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
    )

    user_claims_table = table(
        'user_claims',
        column('user_id', Integer),
        column('claim_id', Integer),
    )

    # --- Roles ---
    op.bulk_insert(
        roles_table,
        [
            {"id": 1, "description": "admin"},
            {"id": 2, "description": "user"},
        ]
    )

    # --- Claims ---
    op.bulk_insert(
        claims_table,
        [
            {"id": 1, "description": "can_create_users", "active": True},
            {"id": 2, "description": "can_delete_users", "active": False},
        ]
    )

    # --- Default User ---
    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "name": "first_user",
                "email": "user@example.com",
                "password": "f2c3552a77",
                "role_id": 1,
                "created_at": datetime.utcnow(),
                "updated_at": None,
            }
        ]
    )

    # --- User ↔ Claims ---
    op.bulk_insert(
        user_claims_table,
        [
            {"user_id": 1, "claim_id": 1},
            {"user_id": 1, "claim_id": 2},
        ]
    )


def downgrade() -> None:
    op.drop_table('user_claims')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('claims')
