"""added columns in addedMedication table

Revision ID: ecefb3a2ff96
Revises: 36b571364d47
Create Date: 2023-10-06 12:07:57.676272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecefb3a2ff96'
down_revision = '36b571364d47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('added_medication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('include', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('prohibitedClass', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('added_medication', schema=None) as batch_op:
        batch_op.drop_column('prohibitedClass')
        batch_op.drop_column('include')

    # ### end Alembic commands ###
