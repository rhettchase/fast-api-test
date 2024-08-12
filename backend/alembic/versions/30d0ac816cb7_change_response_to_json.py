from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '30d0ac816cb7'
down_revision = '1ffc40f7c40a'
branch_labels = None
depends_on = None

def upgrade():
    # Alter the 'response' column to JSON using the `USING` clause
    op.alter_column(
        'answers', 'response',
        type_=sa.JSON,
        postgresql_using="response::json"
    )

def downgrade():
    # Revert the 'response' column back to TEXT (or any previous type) in the downgrade
    op.alter_column(
        'answers', 'response',
        type_=sa.Text
    )
