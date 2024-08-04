"""Change options to JSON

Revision ID: 1ffc40f7c40a
Revises: eff8884101bd
Create Date: 2024-08-03 16:58:29.753964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ffc40f7c40a'
down_revision: Union[str, None] = 'eff8884101bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Convert existing data from VARCHAR to JSON array
    op.execute(
        """
        ALTER TABLE questions
        ALTER COLUMN options
        TYPE JSON USING options::json
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # Convert JSON back to VARCHAR if needed
    op.alter_column(
        'questions',
        'options',
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        postgresql_using='options::text',
        existing_nullable=True
    )
    # ### end Alembic commands ###
