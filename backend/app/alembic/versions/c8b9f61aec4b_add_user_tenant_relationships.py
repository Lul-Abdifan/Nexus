# """add_user_tenant_relationships

# Revision ID: c8b9f61aec4b
# Revises: c982c1889793
# Create Date: 2025-05-07 00:38:46.131167

# """
# from alembic import op
# import sqlalchemy as sa
# import sqlmodel.sql.sqltypes


# # revision identifiers, used by Alembic.
# revision = 'c8b9f61aec4b'
# down_revision = 'c982c1889793'
# branch_labels = None
# depends_on = None


# def upgrade():
#     pass


# def downgrade():
#     pass
"""add_user_tenant_relationships

Revision ID: c8b9f61aec4b
Revises: c982c1889793
Create Date: 2025-05-07 00:38:46.131167

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c8b9f61aec4b'
down_revision = 'c982c1889793'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Add tenant_id column (nullable) if it doesn't exist
    conn = op.get_bind()
    
    # Check if column exists
    column_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='user' AND column_name='tenant_id'
        )
        """)
    ).scalar()
    
    if not column_exists:
        op.add_column(
            'user',
            sa.Column('tenant_id', postgresql.UUID(), nullable=True)
        )

    # 2. Add foreign key constraint if it doesn't exist
    fk_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.table_constraints
            WHERE table_name='user' AND constraint_name='fk_user_tenant_id'
        )
        """)
    ).scalar()
    
    if not fk_exists:
        op.create_foreign_key(
            'fk_user_tenant_id',
            'user', 'tenant',
            ['tenant_id'], ['id'],
            ondelete='SET NULL'  # Changed to SET NULL since column is nullable
        )

    # 3. Create tenantmodule table if it doesn't exist
    table_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name='tenantmodule'
        )
        """)
    ).scalar()
    
    if not table_exists:
        op.create_table(
            'tenantmodule',
            sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), primary_key=True),
            sa.Column('tenant_id', postgresql.UUID(), nullable=False),
            sa.Column('module_id', postgresql.UUID(), nullable=False),
            sa.Column('user_id', postgresql.UUID(), nullable=False),
            sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
            sa.Column('enabled_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['module_id'], ['erpsystemmodule.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('tenant_id', 'module_id', name='uq_tenant_module')
        )
        
        # Create indexes for the new table
        op.create_index('ix_tenantmodule_tenant_id', 'tenantmodule', ['tenant_id'])
        op.create_index('ix_tenantmodule_module_id', 'tenantmodule', ['module_id'])
        op.create_index('ix_tenantmodule_user_id', 'tenantmodule', ['user_id'])

    # 4. Create index on user.tenant_id if it doesn't exist
    index_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM pg_indexes
            WHERE tablename='user' AND indexname='ix_user_tenant_id'
        )
        """)
    ).scalar()
    
    if not index_exists:
        op.create_index('ix_user_tenant_id', 'user', ['tenant_id'])

def downgrade():
    # 1. Drop indexes first (check if they exist)
    conn = op.get_bind()
    
    indexes = ['ix_tenantmodule_user_id', 'ix_tenantmodule_module_id', 'ix_tenantmodule_tenant_id', 'ix_user_tenant_id']
    
    for index in indexes:
        exists = conn.execute(
            sa.text(f"""
            SELECT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE indexname='{index}'
            )
            """)
        ).scalar()
        
        if exists:
            op.drop_index(index, table_name='user' if index == 'ix_user_tenant_id' else 'tenantmodule')

    # 2. Drop tenantmodule table if it exists
    table_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name='tenantmodule'
        )
        """)
    ).scalar()
    
    if table_exists:
        op.drop_table('tenantmodule')

    # 3. Remove tenant_id from user table if it exists
    column_exists = conn.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='user' AND column_name='tenant_id'
        )
        """)
    ).scalar()
    
    if column_exists:
        # Drop foreign key first if it exists
        fk_exists = conn.execute(
            sa.text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.table_constraints
                WHERE table_name='user' AND constraint_name='fk_user_tenant_id'
            )
            """)
        ).scalar()
        
        if fk_exists:
            op.drop_constraint('fk_user_tenant_id', 'user', type_='foreignkey')
        
        op.drop_column('user', 'tenant_id')