"""mod. notesfields

Revision ID: 8221f31da55a
Revises: d3eec3ba2ce6
Create Date: 2025-01-15 15:19:31.741754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8221f31da55a'
down_revision = 'd3eec3ba2ce6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes_fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uniqueIdentifier', sa.Text(), nullable=True))
        batch_op.create_unique_constraint('uq_notes_fields_unique_id', ['uniqueIdentifier'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes_fields', schema=None) as batch_op:
        batch_op.drop_constraint('uq_notes_fields_unique_id', type_='unique')
        batch_op.drop_column('uniqueIdentifier')

    # ### end Alembic commands ###
