"""Update is_admin field

Revision ID: b1895c63b6ba
Revises: ab37ba517241
Create Date: 2024-05-16 16:25:55.756950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1895c63b6ba'
down_revision = 'ab37ba517241'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
