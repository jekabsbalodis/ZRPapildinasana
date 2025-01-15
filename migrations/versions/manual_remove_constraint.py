"""remove atc constraint manually

Revision ID: manual_remove_atc
Revises: 8221f31da55a
Create Date: 2025-01-15 15:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'manual_remove_atc' 
down_revision = '8221f31da55a'
branch_labels = None
depends_on = None

def upgrade():
    # SQLite doesn't support DROP CONSTRAINT
    # Need to:
    # 1. Create new table
    # 2. Copy data
    # 3. Drop old table
    # 4. Rename new table
    
    op.execute("""
        CREATE TABLE notes_fields_new (
            id INTEGER PRIMARY KEY,
            uniqueIdentifier TEXT UNIQUE,
            atcCode VARCHAR(10),
            prohibitedOUTCompetition VARCHAR(15),
            prohibitedINCompetition VARCHAR(15), 
            prohibitedClass VARCHAR(10),
            notesLV TEXT,
            sportsINCompetitionLV TEXT,
            sportsOUTCompetitionLV TEXT,
            notesEN TEXT,
            sportsINCompetitionEN TEXT,
            sportsOUTCompetitionEN TEXT
        )
    """)
    
    op.execute("""
        INSERT INTO notes_fields_new 
        SELECT * FROM notes_fields
    """)
    
    op.execute("DROP TABLE notes_fields")
    op.execute("ALTER TABLE notes_fields_new RENAME TO notes_fields")

def downgrade():
    pass