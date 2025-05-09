"""Create Address, Customer, Modules, Order tables

Revision ID: 52bbc9a8469b
Revises: 6044cdd58f01
Create Date: 2025-05-08 21:05:05.578964

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '52bbc9a8469b'
down_revision = '6044cdd58f01'
branch_labels = None
depends_on = None

def upgrade():
    # Create Address table
    op.create_table(
        'address',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('address_line1', sa.String(), nullable=False),
        sa.Column('address_line2', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Customer table
    op.create_table(
        'customer',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('industry', sa.Text(), nullable=False),
        sa.Column('address', sa.UUID(), nullable=False),
        sa.Column('phone_no', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['address'], ['address.id'], name='customer_address_fkey'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Modules table
    op.create_table(
        'modules',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.Enum('module1', 'module2', name='modulenameenum'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

# Create CustomerModule table
    op.create_table(
        'customer_module',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('customer_id', sa.UUID(), nullable=False),
        sa.Column('module_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='customer_module_customer_id_fkey'),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], name='customer_module_module_id_fkey'),
        sa.PrimaryKeyConstraint('id')
    )
    # Create Order table
    op.create_table(
        'order',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('customer_id', sa.UUID(), nullable=False),
        sa.Column('order_status', sa.Enum('pending', 'completed', 'cancelled', name='orderstatusenum'), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('erp_username', sa.String(), nullable=False),
        sa.Column('erp_password', sa.String(), nullable=False),
        sa.Column('erp_link', sa.String(), nullable=False),
        sa.Column('company_description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='order_customer_id_fkey'),
        sa.PrimaryKeyConstraint('id')
    )
def downgrade():
    # Drop tables in reverse order (child first, then parent)
    op.drop_table('order')
    op.drop_table('modules')
    op.drop_table('customer')
    op.drop_table('customer_module')
    op.drop_table('address')