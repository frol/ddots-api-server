"""add_programming_languages_module

Revision ID: dc67ca82abd4
Revises: 4d936a11537a
Create Date: 2017-05-31 01:41:38.095864

"""

# revision identifiers, used by Alembic.
revision = 'dc67ca82abd4'
down_revision = '4d936a11537a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('programming_language',
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('compiler_docker_image_name', sa.String(length=255), nullable=False),
        sa.Column('executor_docker_image_name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('name')
    )


def downgrade():
    op.drop_table('programming_language')
