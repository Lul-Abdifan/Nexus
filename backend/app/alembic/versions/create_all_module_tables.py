"""Create all module-related tables

Revision ID: create_all_module_tables
Revises: 02e017ea88e8
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'create_all_module_tables'
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

    # Create customer_module table
    op.create_table(
        'customer_module',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('customer_id', UUID(as_uuid=True), sa.ForeignKey('customer.id', ondelete='CASCADE')),
        sa.Column('module_id', UUID(as_uuid=True), sa.ForeignKey('modules.id', ondelete='CASCADE')),
    )

    # Create indexes
    op.create_index('ix_customer_module_customer_id', 'customer_module', ['customer_id'])
    op.create_index('ix_customer_module_module_id', 'customer_module', ['module_id'])

def downgrade():
    op.drop_table('customer_module')
    op.drop_table('modules') 