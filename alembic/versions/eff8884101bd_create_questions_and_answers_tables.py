"""create questions and answers tables

Revision ID: eff8884101bd
Revises: 
Create Date: 2024-08-03 16:14:32.539671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eff8884101bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Convert existing response data to JSON
    op.alter_column('answers', 'response',
                    existing_type=sa.String(),
                    type_=sa.JSON(),
                    postgresql_using='response::json')
    # ### end Alembic commands ###


def downgrade():
    # Convert JSON back to VARCHAR if needed
    op.alter_column('answers', 'response',
                    existing_type=sa.JSON(),
                    type_=sa.String(),
                    postgresql_using='response::text')
    # ### end Alembic commands ###
