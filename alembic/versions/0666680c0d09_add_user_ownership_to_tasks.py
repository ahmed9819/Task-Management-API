"""add user ownership to tasks

Revision ID: 0666680c0d09
Revises: 75350d558a30
Create Date: 2026-08-09 14:16:55.158463

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "0666680c0d09"
down_revision: Union[str, Sequence[str], None] = "75350d558a30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


USER_ID = "4ab4bedf-cee9-418e-a854-8d7de7551879"


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Add user_id temporarily as nullable
    op.add_column(
        "tasks",
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=True,
        ),
    )

    # 2. Assign existing tasks to the development user
    op.execute(
        sa.text(
            """
            UPDATE tasks
            SET user_id = CAST(:user_id AS UUID)
            WHERE user_id IS NULL
            """
        ).bindparams(user_id=USER_ID)
    )

    # 3. Make user_id required
    op.alter_column(
        "tasks",
        "user_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

    # 4. Add index for faster user-based queries
    op.create_index(
        op.f("ix_tasks_user_id"),
        "tasks",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_tasks_user_id"),
        table_name="tasks",
    )

    op.drop_column(
        "tasks",
        "user_id",
    )