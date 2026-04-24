"""create accounts table

Revision ID: e13fc19ff6b6
Revises: 5b43f9a57773
Create Date: 2026-04-06 16:50:33.784129

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e13fc19ff6b6"
down_revision: Union[str, Sequence[str], None] = "5b43f9a57773"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("accounts")
