"""create_erp_and_tenant_tables

Revision ID: c982c1889793
Revises: fa553e526fba
Create Date: 2025-05-07 00:23:01.268499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c982c1889793'
down_revision = 'fa553e526fba'
branch_labels = None
depends_on = None


def upgrade():
    # Create ERPSystemModule table
    op.create_table(
        'erpsystemmodule',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('display_name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('required_modules', postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'::text[]"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )
    
    # Create Tenant table
    op.create_table(
        'tenant',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('max_users', sa.Integer(), server_default=sa.text('10'), nullable=False),
        sa.Column('plan', sa.String(), server_default=sa.text("'basic'"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )
    
    # Create TenantModule association table
    op.create_table(
        'tenantmodule',
        sa.Column('tenant_id', postgresql.UUID(), nullable=False),
        sa.Column('module_id', postgresql.UUID(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('activated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('config', postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['module_id'], ['erpsystemmodule.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('tenant_id', 'module_id')
    )
    
   

def downgrade():
    # Drop tables in reverse order
    op.drop_table('tenantmodule')
    op.drop_table('tenant')
    op.drop_table('erpsystemmodule')