"""task_results table

Revision ID: d52eddcde7dd
Revises: 1c6507d5d36c
Create Date: 2025-09-09 11:44:12.036902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd52eddcde7dd'
down_revision: Union[str, Sequence[str], None] = '1c6507d5d36c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "task_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=False), nullable=True),
        sa.UniqueConstraint("task_id"),
    )
    op.create_index("ix_task_results_task_id", "task_results", ["task_id"])
    op.create_index("ix_task_results_status", "task_results", ["status"])

def downgrade():
    op.drop_index("ix_task_results_status", table_name="task_results")
    op.drop_index("ix_task_results_task_id", table_name="task_results")
    op.drop_table("task_results")
