"""update card model

Revision ID: 4f3a958d16ed
Revises: fbb67df6e1d7
Create Date: 2024-01-22 11:12:01.394898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f3a958d16ed'
down_revision: Union[str, None] = 'fbb67df6e1d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
