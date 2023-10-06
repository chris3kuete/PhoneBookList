"""empty message

Revision ID: b4d92336de8f
Revises: 6e1fc0979b8c
Create Date: 2023-10-04 22:04:15.304615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4d92336de8f'
down_revision = '6e1fc0979b8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('list_tbl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_saved', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('list_tbl', schema=None) as batch_op:
        batch_op.drop_column('date_saved')

    # ### end Alembic commands ###
