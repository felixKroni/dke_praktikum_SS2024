"""create table

Revision ID: ab37ba517241
Revises: 
Create Date: 2024-04-29 16:29:11.101641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab37ba517241'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('triebwagen',
    sa.Column('maxZugkraft', sa.Integer(), nullable=False),
    sa.Column('wagennummer', sa.String(), nullable=False),
    sa.Column('spurweite', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('wagennummer')
    )
    with op.batch_alter_table('triebwagen', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_triebwagen_spurweite'), ['spurweite'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('wagen',
    sa.Column('wagennummer', sa.String(), nullable=False),
    sa.Column('spurweite', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('wagennummer')
    )
    with op.batch_alter_table('wagen', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_wagen_spurweite'), ['spurweite'], unique=False)

    op.create_table('zug',
    sa.Column('zug_nummer', sa.String(), nullable=False),
    sa.Column('zug_name', sa.String(), nullable=False),
    sa.Column('triebwagen_nr', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['triebwagen_nr'], ['triebwagen.wagennummer'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('zug_nummer'),
    sa.UniqueConstraint('triebwagen_nr')
    )
    op.create_table('personenwagen',
    sa.Column('sitzanzahl', sa.Integer(), nullable=False),
    sa.Column('maximalgewicht', sa.Integer(), nullable=False),
    sa.Column('zug_nummer', sa.String(length=255), nullable=True),
    sa.Column('wagennummer', sa.String(), nullable=False),
    sa.Column('spurweite', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['zug_nummer'], ['zug.zug_nummer'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('wagennummer')
    )
    with op.batch_alter_table('personenwagen', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_personenwagen_spurweite'), ['spurweite'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personenwagen', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_personenwagen_spurweite'))

    op.drop_table('personenwagen')
    op.drop_table('zug')
    with op.batch_alter_table('wagen', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_wagen_spurweite'))

    op.drop_table('wagen')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('triebwagen', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_triebwagen_spurweite'))

    op.drop_table('triebwagen')
    # ### end Alembic commands ###
