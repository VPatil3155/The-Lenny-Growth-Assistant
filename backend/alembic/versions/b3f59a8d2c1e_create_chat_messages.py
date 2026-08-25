"""create chat messages.

Revision ID: b3f59a8d2c1e
Revises: e204b61ea5c7
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b3f59a8d2c1e"
down_revision: Union[str, Sequence[str], None] = "e204b61ea5c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["session_id"], ["chat_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="ck_chat_messages_role",
        ),
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
