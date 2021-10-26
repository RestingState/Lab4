"""create student_mark table

Revision ID: 65d29ecad37e
Revises: ad360e769430
Create Date: 2021-10-26 15:58:33.734637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d29ecad37e'
down_revision = 'ad360e769430'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'student_mark',
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('student.id'), primary_key=True),
        sa.Column('mark_id', sa.Integer(), sa.ForeignKey('mark.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('student_mark')
