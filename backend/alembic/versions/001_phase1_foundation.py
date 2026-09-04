"""create_phase1_tables

Revision ID: 001_phase1_foundation
Revises: 
Create Date: 2026-09-04 22:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

revision: str = '001_phase1_foundation'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Ensure PostGIS extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('commander', 'dispatcher', 'crew_lead', 'responder', 'citizen', name='user_role'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create garbage_reports table
    op.create_table(
        'garbage_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('reporter_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', spatial_index=False), nullable=False),
        sa.Column('category', sa.Enum('wet', 'dry', 'electronic', 'clothing', 'hazardous', 'mixed', 'other', name='waste_category'), nullable=False),
        sa.Column('volume_tier', sa.Enum('minor', 'moderate', 'bulk', name='volume_tier'), nullable=False),
        sa.Column('status', sa.Enum('reported', 'under_review', 'approved', 'assigned', 'in_progress', 'cleaned', 'verified', name='report_status'), nullable=False),
        sa.Column('image_url', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_garbage_reports_id'), 'garbage_reports', ['id'], unique=False)
    op.create_index(op.f('ix_garbage_reports_reporter_id'), 'garbage_reports', ['reporter_id'], unique=False)
    op.create_index('idx_garbage_reports_created_at', 'garbage_reports', ['created_at'], unique=False)
    op.create_index('idx_garbage_reports_status', 'garbage_reports', ['status'], unique=False)
    op.create_index('idx_garbage_reports_location', 'garbage_reports', ['location'], unique=False, postgresql_using='gist')

def downgrade() -> None:
    op.drop_index('idx_garbage_reports_location', table_name='garbage_reports', postgresql_using='gist')
    op.drop_index('idx_garbage_reports_status', table_name='garbage_reports')
    op.drop_index('idx_garbage_reports_created_at', table_name='garbage_reports')
    op.drop_index(op.f('ix_garbage_reports_reporter_id'), table_name='garbage_reports')
    op.drop_index(op.f('ix_garbage_reports_id'), table_name='garbage_reports')
    op.drop_table('garbage_reports')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS report_status;")
    op.execute("DROP TYPE IF EXISTS volume_tier;")
    op.execute("DROP TYPE IF EXISTS waste_category;")
    op.execute("DROP TYPE IF EXISTS user_role;")
