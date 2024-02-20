"""add wallet balance

Revision ID: b4add78963f1
Revises: 4f3a958d16ed
Create Date: 2024-01-22 15:31:21.060653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4add78963f1'
down_revision: Union[str, None] = '4f3a958d16ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
