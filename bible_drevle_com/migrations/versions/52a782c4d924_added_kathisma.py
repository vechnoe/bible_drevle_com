"""Added kathisma

Revision ID: 52a782c4d924
Revises: fed0f415374b
Create Date: 2016-09-16 14:21:03.282837

"""

# revision identifiers, used by Alembic.
revision = '52a782c4d924'
down_revision = 'fed0f415374b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kathismas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('title_slavonic', sa.Text(), nullable=True),
    sa.Column('book_slug', sa.String(), nullable=False, server_default='psalms'),
    sa.ForeignKeyConstraint(['book_slug'], ['books.book_slug'], ),
    sa.PrimaryKeyConstraint('id', 'book_slug')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kathismas')
    ### end Alembic commands ###
