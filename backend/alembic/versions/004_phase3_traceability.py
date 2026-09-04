"""004_phase3_traceability - Add Transfer Weighments and Disposal Records

Revision ID: 004_phase3_traceability
Revises: 003_audit_log
Create Date: 2026-09-05

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '004_phase3_traceability'
down_revision = '003_audit_log'
branch_labels = None
depends_on = None

facility_type_enum = postgresql.ENUM(
    'recycling_plant', 'composting_facility', 'waste_to_energy', 'sanitary_landfill',
    name='facility_type'
)


def upgrade() -> None:
    # 1. Create facility_type enum
    facility_type_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add new values to audit_action enum if in PostgreSQL
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        for val in ['intelligent_verification_evaluated', 'weighment_recorded', 'waste_segregated', 'disposal_recorded']:
            op.execute(f"ALTER TYPE audit_action ADD VALUE IF NOT EXISTS '{val}'")

    # 3. Create transfer_weighments table
    op.create_table(
        'transfer_weighments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('batch_id', sa.Integer(), sa.ForeignKey('collection_batches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('weighbridge_code', sa.String(50), nullable=False),
        sa.Column('gross_weight_kg', sa.Float(), nullable=False),
        sa.Column('tare_weight_kg', sa.Float(), nullable=False),
        sa.Column('net_weight_kg', sa.Float(), nullable=False),
        sa.Column('weighment_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('operator_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_transfer_weighments_batch_id', 'transfer_weighments', ['batch_id'])

    # 4. Create disposal_records table
    op.create_table(
        'disposal_records',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('weighment_id', sa.Integer(), sa.ForeignKey('transfer_weighments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('facility_name', sa.String(100), nullable=False),
        sa.Column('facility_type', postgresql.ENUM('recycling_plant', 'composting_facility', 'waste_to_energy', 'sanitary_landfill', name='facility_type', create_type=False), nullable=False),
        sa.Column('recycled_weight_kg', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('composted_weight_kg', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('landfill_weight_kg', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('diversion_rate_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_disposal_records_weighment_id', 'disposal_records', ['weighment_id'])
    op.create_index('idx_disposal_records_facility_type', 'disposal_records', ['facility_type'])


def downgrade() -> None:
    op.drop_index('idx_disposal_records_facility_type', table_name='disposal_records')
    op.drop_index('idx_disposal_records_weighment_id', table_name='disposal_records')
    op.drop_table('disposal_records')
    op.drop_index('idx_transfer_weighments_batch_id', table_name='transfer_weighments')
    op.drop_table('transfer_weighments')
    facility_type_enum.drop(op.get_bind(), checkfirst=True)
