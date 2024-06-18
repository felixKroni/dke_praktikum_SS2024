
"""empty message

Revision ID: 3cdf5efc3d8f
Revises: 0451f47a85d6
Create Date: 2024-06-18 22:45:36.379398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cdf5efc3d8f'
down_revision = '0451f47a85d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wartung_mitarbeiter',
    sa.Column('wartung_nr', sa.String(), nullable=False),
    sa.Column('mitarbeiter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mitarbeiter_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['wartung_nr'], ['wartung.wartung_nr'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('wartung_nr', 'mitarbeiter_id')
    )
    with op.batch_alter_table('wartung', schema=None) as batch_op:
        batch_op.drop_constraint('uq_mitarbeiter_time', type_='unique')
        batch_op.create_unique_constraint('uq_mitarbeiter_time', ['start_time'])
        # batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('mitarbeiter_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wartung', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mitarbeiter_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['mitarbeiter_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_constraint('uq_mitarbeiter_time', type_='unique')
        batch_op.create_unique_constraint('uq_mitarbeiter_time', ['mitarbeiter_id', 'start_time'])

    op.drop_table('wartung_mitarbeiter')
    # ### end Alembic commands ###
