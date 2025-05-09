"""fix_erp_module_relationships

Revision ID: b4d537f7445a
Revises: c8b9f61aec4b
Create Date: 2025-05-07 00:53:53.605455

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b4d537f7445a'
down_revision = 'c8b9f61aec4b'
branch_labels = None
depends_on = None

def upgrade():
    # 1. First verify the tables exist
    conn = op.get_bind()
    
    # Check if erpsystemmodule table exists
    erp_table_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'erpsystemmodule'
        )
        """)
    ).scalar()
    
    # Check if tenantmodule table exists
    tenant_module_table_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'tenantmodule'
        )
        """)
    ).scalar()

    if not erp_table_exists or not tenant_module_table_exists:
        raise Exception("Required tables don't exist. Run previous migrations first.")

    # 2. Add missing foreign key constraint if it doesn't exist
    fk_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.table_constraints
            WHERE table_name = 'tenantmodule'
            AND constraint_name = 'tenantmodule_module_id_fkey'
        )
        """)
    ).scalar()

    if not fk_exists:
        op.create_foreign_key(
            'tenantmodule_module_id_fkey',
            'tenantmodule', 'erpsystemmodule',
            ['module_id'], ['id'],
            ondelete='CASCADE'
        )

    # 3. Add missing index on module_id if it doesn't exist
    index_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM pg_indexes
            WHERE tablename = 'tenantmodule'
            AND indexname = 'ix_tenantmodule_module_id'
        )
        """)
    ).scalar()

    if not index_exists:
        op.create_index(
            'ix_tenantmodule_module_id',
            'tenantmodule',
            ['module_id']
        )

def downgrade():
    # 1. Drop the foreign key constraint if it exists
    conn = op.get_bind()
    
    fk_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.table_constraints
            WHERE table_name = 'tenantmodule'
            AND constraint_name = 'tenantmodule_module_id_fkey'
        )
        """)
    ).scalar()

    if fk_exists:
        op.drop_constraint(
            'tenantmodule_module_id_fkey',
            'tenantmodule',
            type_='foreignkey'
        )

    # 2. Drop the index if it exists
    index_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT FROM pg_indexes
            WHERE tablename = 'tenantmodule'
            AND indexname = 'ix_tenantmodule_module_id'
        )
        """)
    ).scalar()

    if index_exists:
        op.drop_index(
            'ix_tenantmodule_module_id',
            table_name='tenantmodule'
        )