"""add user email migration

Revision ID: 8e8d72e56aa
Revises: None
Create Date: 2015-11-30 16:58:59.339460

"""

# revision identifiers, used by Alembic.
revision = '8e8d72e56aa'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    ### end Alembic commands ###
