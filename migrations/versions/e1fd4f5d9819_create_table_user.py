"""create table user

Revision ID: e1fd4f5d9819
Revises: 
Create Date: 2017-04-17 15:12:40.342375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1fd4f5d9819'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')
