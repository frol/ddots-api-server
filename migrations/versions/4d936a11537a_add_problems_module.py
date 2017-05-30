"""add_problems_module

Revision ID: 4d936a11537a
Revises: 2f07434defaf
Create Date: 2017-05-31 01:41:02.218809

"""

# revision identifiers, used by Alembic.
revision = '4d936a11537a'
down_revision = '2f07434defaf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('problem',
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('tests_seaweed_id', sa.String(length=255), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('problem')
