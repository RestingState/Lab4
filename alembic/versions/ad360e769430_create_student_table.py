"""create student table

Revision ID: ad360e769430
Revises: a0897ba427e5
Create Date: 2021-10-26 15:56:37.077454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad360e769430'
down_revision = 'a0897ba427e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'student',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, unique=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('major_id', sa.Integer(), sa.ForeignKey('major.id')),
        sa.Column('rating', sa.Integer(), nullable=False),
    )


def downgrade():
    op.drop_table('student')
