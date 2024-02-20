"""add card details model

Revision ID: fbb67df6e1d7
Revises: 2f8726d6bdfb
Create Date: 2024-01-22 10:27:08.965580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbb67df6e1d7'
down_revision: Union[str, None] = '2f8726d6bdfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
