"""add priority and due_date to tasks

Revision ID: 7409d109fa97
Revises: 14591b10d9ba
Create Date: 2026-10-22 16:08:25.644099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7409d109fa97'
down_revision: Union[str, Sequence[str], None] = '14591b10d9ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tasks', sa.Column('priority', sa.String(length=10), server_default='medium', nullable=False))
    op.add_column('tasks', sa.Column('due_date', sa.Date(), nullable=True))
    op.create_check_constraint(
        'check_task_priority',
        'tasks',
        "priority IN ('low', 'medium', 'high')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('check_task_priority', 'tasks', type_='check')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')
