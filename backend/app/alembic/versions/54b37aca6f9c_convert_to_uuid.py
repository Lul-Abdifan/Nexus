"""convert_to_uuid

Revision ID: 54b37aca6f9c
Revises: 02e017ea88e8
Create Date: 2025-05-07 19:21:41.778408

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision = '54b37aca6f9c'
down_revision = '02e017ea88e8'
branch_labels = None
depends_on = None



def upgrade():
    # 1. Drop foreign key constraints first
    op.drop_constraint('tenantmodule_module_id_fkey', 'tenantmodule', type_='foreignkey')
    
    # 2. Convert erpmodule.id to UUID
    op.execute('ALTER TABLE erpmodule ALTER COLUMN id TYPE UUID USING id::TEXT::UUID')
    
    # 3. Convert tenantmodule.module_id to UUID
    op.execute('ALTER TABLE tenantmodule ALTER COLUMN module_id TYPE UUID USING module_id::TEXT::UUID')
    
    # 4. Recreate foreign key
    op.create_foreign_key(
        'tenantmodule_module_id_fkey',
        'tenantmodule', 'erpmodule',
        ['module_id'], ['id']
    )

def downgrade():
    # Reverse the process
    op.drop_constraint('tenantmodule_module_id_fkey', 'tenantmodule', type_='foreignkey')
    op.execute('ALTER TABLE tenantmodule ALTER COLUMN module_id TYPE INTEGER USING module_id::TEXT::INTEGER')
    op.execute('ALTER TABLE erpmodule ALTER COLUMN id TYPE INTEGER USING id::TEXT::INTEGER')
    op.create_foreign_key(
        'tenantmodule_module_id_fkey',
        'tenantmodule', 'erpmodule',
        ['module_id'], ['id']
    )
    op.alter_column('tenantmodule', 'module_id',
               existing_type=postgresql.UUID(),
               type_=sa.INTEGER())
    
    op.alter_column('erpmodule', 'id',
               existing_type=postgresql.UUID(),
               type_=sa.INTEGER())