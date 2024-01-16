"""dwdw

Revision ID: 19d076580b37
Revises: 3cfb6aba7be5
Create Date: 2024-01-12 14:33:45.358202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19d076580b37'
down_revision = '3cfb6aba7be5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_authenticated')
        batch_op.drop_column('is_active')
        batch_op.drop_column('is_anonymous')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_anonymous', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('is_authenticated', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
