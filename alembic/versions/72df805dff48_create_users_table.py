"""create users table

Revision ID: 72df805dff48
Revises: 
Create Date: 2021-10-26 15:35:51.670480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72df805dff48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, unique=True),
        sa.Column('full_name', sa.String(64), nullable=False),
        sa.Column('login', sa.String(24), nullable=False, unique=True),
        sa.Column('password', sa.String(48), nullable=False),
        sa.Column('email', sa.String(80), nullable=False, unique=True)
    )


def downgrade():
    op.drop_table('users')
