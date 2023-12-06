"""empty message

Revision ID: d3eec3ba2ce6
Revises: b70eb8201a46
Create Date: 2023-12-06 15:50:32.741485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3eec3ba2ce6'
down_revision = 'b70eb8201a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('searched_medication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doping', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('searched_medication', schema=None) as batch_op:
        batch_op.drop_column('doping')

    # ### end Alembic commands ###
