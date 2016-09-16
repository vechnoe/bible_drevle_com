"""Init

Revision ID: 15204a4fbb42
Revises: 
Create Date: 2016-09-15 17:58:23.131787

"""

# revision identifiers, used by Alembic.
revision = '15204a4fbb42'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('books',
        sa.Column('book_slug', sa.String(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('title_slavonic', sa.Text(), nullable=True),
        sa.Column('in_bible_list', sa.Boolean(), nullable=True),
        sa.Column('book_ending', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('book_slug'),
    )
    op.create_table('chapters',
        sa.Column('book_slug', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['book_slug'], ['books.book_slug'], ),
        sa.PrimaryKeyConstraint('book_slug', 'id')
    )
    op.create_table('pericopes',
        sa.Column('book_slug', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['book_slug'], ['books.book_slug'], ),
        sa.PrimaryKeyConstraint('book_slug', 'id')
    )


def downgrade():
    op.drop_table('books')
    op.drop_table('chapters')
    op.drop_table('pericopes')

