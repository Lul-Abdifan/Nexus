"""Drop tenantmodule and erpmodule tables

Revision ID: 02e017ea88e8
Revises: b4d537f7445a
Create Date: 2025-05-07 18:52:49.212206

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '02e017ea88e8'
down_revision = 'b4d537f7445a'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Drop the foreign key constraint first (if it exists)
    op.drop_constraint(
        'tenantmodule_module_id_fkey',  # constraint name
        'tenantmodule',                 # table name
        type_='foreignkey'
    )
    # 2. Drop the child table first
    op.drop_table('tenantmodule')
    # 3. Then drop the parent table
    op.drop_table('erpmodule')

def downgrade():
    # (Optional) Recreate the tables and constraint if you want to support downgrade
    op.execute("DROP TABLE tenantmodule CASCADE")
    op.execute("DROP TABLE erpmodule CASCADE")