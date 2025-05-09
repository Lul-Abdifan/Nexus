"""remove_display_name_and_required_modules_columns

Revision ID: 6044cdd58f01
Revises: 54b37aca6f9c
Create Date: 2025-05-07 20:16:12.842762

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision = '6044cdd58f01'
down_revision = '54b37aca6f9c'
branch_labels = None
depends_on = None



def upgrade():
    # First check if table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if 'erpmodule' in tables:
        # Check if columns exist before dropping
        columns = [col['name'] for col in inspector.get_columns('erpmodule')]
        
        if 'display_name' in columns:
            op.drop_column('erpmodule', 'display_name')
            
        if 'required_modules' in columns:
            op.drop_column('erpmodule', 'required_modules')

def downgrade():
    # Only add columns if table exists
    conn = op.get_bind()
    if 'erpmodule' in sa.inspect(conn).get_table_names():
        op.add_column('erpmodule', 
            sa.Column('display_name', sa.String(length=100), nullable=True))
        op.add_column('erpmodule',
            sa.Column('required_modules', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('erpmodule',
        sa.Column('display_name', sa.String(length=100), nullable=True))
    op.add_column('erpmodule',
        sa.Column('required_modules', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('erp_system_modules',
        sa.Column('display_name', sa.String(length=100), nullable=True))
    op.add_column('erp_system_modules',
        sa.Column('required_modules', postgresql.JSON(astext_type=sa.Text()), nullable=True))