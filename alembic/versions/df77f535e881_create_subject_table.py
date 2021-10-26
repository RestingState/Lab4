"""create subject table

Revision ID: df77f535e881
Revises: 111f49027561
Create Date: 2021-10-26 15:54:02.391387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df77f535e881'
down_revision = '111f49027561'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'subject',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, unique=True),
        sa.Column('name', sa.String(80), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table('subject')
