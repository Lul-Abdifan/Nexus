"""Create modules table

Revision ID: create_module_table
Revises: 02e017ea88e8
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'create_module_table'
down_revision = '02e017ea88e8'
branch_labels = None
depends_on = None

def upgrade():
    # Create modules table
    op.create_table(
        'modules',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )

def downgrade():
    op.drop_table('modules') 