"""add_company_fields_to_user

Revision ID: a93120ee251b
Revises: 2fedec953e13
Create Date: 2025-05-05 23:44:36.529066

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'a93120ee251b'
down_revision = '2fedec953e13'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('company_name', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('company_size', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('industry_type', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(length=20), nullable=True))

def downgrade():
    op.drop_column('user', 'company_name')
    op.drop_column('user', 'company_size')
    op.drop_column('user', 'industry_type')
    op.drop_column('user', 'phone')