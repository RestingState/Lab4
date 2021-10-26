"""create mark table

Revision ID: a0897ba427e5
Revises: df77f535e881
Create Date: 2021-10-26 15:55:06.269398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0897ba427e5'
down_revision = 'df77f535e881'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mark',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, unique=True),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('subject.id')),
        sa.Column('grade', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('mark')
