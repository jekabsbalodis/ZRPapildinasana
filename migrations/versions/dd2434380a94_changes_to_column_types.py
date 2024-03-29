"""Changes to column types

Revision ID: dd2434380a94
Revises: bb48781d968e
Create Date: 2023-10-13 14:46:32.060431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd2434380a94'
down_revision = 'bb48781d968e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('added_medication', schema=None) as batch_op:
        batch_op.alter_column('atcCode',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('prohibitedClass',
               existing_type=sa.TEXT(),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('notesLV',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('sportsINCompetitionLV',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('sportsOUTCompetitionLV',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('notesEN',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('sportsINCompetitionEN',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('sportsOUTCompetitionEN',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.drop_index('ix_added_medication_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('added_medication', schema=None) as batch_op:
        batch_op.create_index('ix_added_medication_name', ['name'], unique=False)
        batch_op.alter_column('sportsOUTCompetitionEN',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('sportsINCompetitionEN',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('notesEN',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('sportsOUTCompetitionLV',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('sportsINCompetitionLV',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('notesLV',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('prohibitedClass',
               existing_type=sa.String(length=10),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('atcCode',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###
