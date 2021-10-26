"""create major table

Revision ID: 111f49027561
Revises: 72df805dff48
Create Date: 2021-10-26 15:52:12.611795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '111f49027561'
down_revision = '72df805dff48'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'major',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, unique=True),
        sa.Column('name', sa.String(80), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table('major')
