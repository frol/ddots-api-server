"""add_solutions_module

Revision ID: bc763380bd74
Revises: dc67ca82abd4
Create Date: 2017-05-31 01:42:10.677597

"""

# revision identifiers, used by Alembic.
revision = 'bc763380bd74'
down_revision = 'dc67ca82abd4'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    op.create_table('solution',
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('programming_language_name', sa.String(length=20), nullable=False),
        sa.Column('testing_mode', sa.Enum('one', 'first_fail', 'full', name='testingmodes'), nullable=False),
        sa.Column('state', sa.Enum('new', 'reserved', 'received', 'tested', 'rejected', name='states'), nullable=False),
        sa.Column('status', sqlalchemy_utils.types.scalar_list.ScalarListType(), nullable=False),
        sa.Column('scored_points', sa.Numeric(precision=3), nullable=False),
        sa.Column('source_code_seaweed_id', sa.String(length=255), nullable=False),
        sa.Column('testing_report_seaweed_id', sa.String(length=255), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['problem_id'], ['problem.id'], ),
        sa.ForeignKeyConstraint(['programming_language_name'], ['programming_language.name'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('solution')
