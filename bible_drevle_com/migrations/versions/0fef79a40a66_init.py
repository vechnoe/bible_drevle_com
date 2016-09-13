"""Init

Revision ID: 0fef79a40a66
Revises: 
Create Date: 2016-08-13 15:52:43.617817

"""

# revision identifiers, used by Alembic.
revision = '0fef79a40a66'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('book_slug', sa.String(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('book_slug')
    )
    op.create_table('chapters',
    sa.Column('book_slug', sa.String(), nullable=False),
    sa.Column('chapter_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['book_slug'], ['books.book_slug'], ),
    sa.PrimaryKeyConstraint('book_slug', 'chapter_id')
    )
    op.create_table('verses',
    sa.Column('book_slug', sa.String(), nullable=False),
    sa.Column('chapter_id', sa.Integer(), nullable=False),
    sa.Column('verse_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id', 'book_slug'], ['chapters.chapter_id', 'chapters.book_slug'], ),
    sa.PrimaryKeyConstraint('book_slug', 'chapter_id', 'verse_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verses')
    op.drop_table('chapters')
    op.drop_table('books')
    ### end Alembic commands ###