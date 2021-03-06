"""Added set_name in question_set

Revision ID: 314d6c8a5075
Revises: f11a0b9d5c5b
Create Date: 2018-09-26 00:04:04.641441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '314d6c8a5075'
down_revision = 'f11a0b9d5c5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sets', sa.Column('set_name', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sets', 'set_name')
    # ### end Alembic commands ###
