"""Added default values

Revision ID: f5c963d13750
Revises: 73759fbaa1f4
Create Date: 2016-09-16 16:35:48.438212

"""

# revision identifiers, used by Alembic.
revision = 'f5c963d13750'
down_revision = '73759fbaa1f4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'chapters', 'books', ['book_slug'], ['book_slug'])
    op.create_foreign_key(None, 'kathismas', 'books', ['book_slug'], ['book_slug'])
    op.create_foreign_key(None, 'pericopes', 'books', ['book_slug'], ['book_slug'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pericopes', type_='foreignkey')
    op.drop_constraint(None, 'kathismas', type_='foreignkey')
    op.drop_constraint(None, 'chapters', type_='foreignkey')
    ### end Alembic commands ###
