"""Added Psalm

Revision ID: 73759fbaa1f4
Revises: 52a782c4d924
Create Date: 2016-09-16 14:26:15.737777

"""

# revision identifiers, used by Alembic.
revision = '73759fbaa1f4'
down_revision = '52a782c4d924'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('psalms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_slug', sa.String(), nullable=False, server_default='psalms'),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('title_slavonic', sa.Text(), nullable=True),
    sa.Column('kathisma_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['kathisma_id', 'book_slug'], ['kathismas.id', 'kathismas.book_slug'], ),
    sa.PrimaryKeyConstraint('id', 'book_slug', 'kathisma_id')
    )
    op.drop_constraint('chapters_book_slug_fkey', 'chapters', type_='foreignkey')
    op.drop_constraint('kathismas_book_slug_fkey', 'kathismas', type_='foreignkey')
    op.drop_constraint('pericopes_book_slug_fkey', 'pericopes', type_='foreignkey')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('pericopes_book_slug_fkey', 'pericopes', 'books', ['book_slug'], ['book_slug'])
    op.create_foreign_key('kathismas_book_slug_fkey', 'kathismas', 'books', ['book_slug'], ['book_slug'])
    op.create_foreign_key('chapters_book_slug_fkey', 'chapters', 'books', ['book_slug'], ['book_slug'])
    op.drop_table('psalms')
    ### end Alembic commands ###
