"""phase2_operational_extension

Revision ID: 002_phase2_extensions
Revises: 001_phase1_foundation
Create Date: 2026-09-04 23:00:00.000000

Phase 2 adds the full operational layer on top of Phase 1:
  - workers          : registered crew members
  - vehicles         : fleet transport
  - work_orders      : dispatched cleanup jobs per report
  - work_units       : sub-tasks within a work order
  - work_assignments : worker <-> work_unit linking table
  - cleaning_evidence: BEFORE/PROGRESS/AFTER photos
  - verifications    : evidence approval audit trail
  - compensations    : eligibility records (no payment gateway)
  - collection_batches: waste batch transport records
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

revision: str = '002_phase2_extensions'
down_revision: Union[str, None] = '001_phase1_foundation'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ------------------------------------------------------------------ #
    # workers                                                              #
    # ------------------------------------------------------------------ #
    op.create_table(
        'workers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('worker_code', sa.String(length=30), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('status', sa.Enum(
            'available', 'assigned', 'off_duty', 'suspended',
            name='worker_status'
        ), nullable=False, server_default='available'),
        sa.Column('verification_state', sa.Enum(
            'unverified', 'pending_verification', 'verified', 'rejected',
            name='worker_verification_state'
        ), nullable=False, server_default='unverified'),
        sa.Column('identity_ref', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        sa.UniqueConstraint('worker_code'),
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)
    op.create_index(op.f('ix_workers_user_id'), 'workers', ['user_id'], unique=False)
    op.create_index(op.f('ix_workers_worker_code'), 'workers', ['worker_code'], unique=False)

    # ------------------------------------------------------------------ #
    # vehicles                                                             #
    # ------------------------------------------------------------------ #
    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('vehicle_code', sa.String(length=30), nullable=False),
        sa.Column('callsign', sa.String(length=50), nullable=False),
        sa.Column('license_plate', sa.String(length=30), nullable=False),
        sa.Column('vehicle_type', sa.String(length=50), nullable=False, server_default='UTILITY_TRUCK'),
        sa.Column('capacity_m3', sa.Float(), nullable=False, server_default='5.0'),
        sa.Column('status', sa.Enum(
            'available', 'deployed', 'maintenance', 'offline',
            name='vehicle_status'
        ), nullable=False, server_default='available'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('vehicle_code'),
        sa.UniqueConstraint('license_plate'),
    )
    op.create_index(op.f('ix_vehicles_id'), 'vehicles', ['id'], unique=False)
    op.create_index(op.f('ix_vehicles_vehicle_code'), 'vehicles', ['vehicle_code'], unique=False)
    op.create_index('idx_vehicles_status', 'vehicles', ['status'], unique=False)

    # ------------------------------------------------------------------ #
    # work_orders                                                          #
    # ------------------------------------------------------------------ #
    op.create_table(
        'work_orders',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('report_id', sa.Integer(), nullable=False),
        sa.Column('work_code', sa.String(length=30), nullable=False),
        sa.Column('classification', sa.String(length=50), nullable=False, server_default='GENERAL_CLEANUP'),
        sa.Column('required_worker_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.Enum(
            'open', 'assigned', 'in_progress', 'completed', 'cancelled',
            name='work_order_status'
        ), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['report_id'], ['garbage_reports.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('work_code'),
    )
    op.create_index(op.f('ix_work_orders_id'), 'work_orders', ['id'], unique=False)
    op.create_index(op.f('ix_work_orders_report_id'), 'work_orders', ['report_id'], unique=False)
    op.create_index(op.f('ix_work_orders_work_code'), 'work_orders', ['work_code'], unique=False)
    op.create_index('idx_work_orders_status', 'work_orders', ['status'], unique=False)

    # ------------------------------------------------------------------ #
    # work_units                                                           #
    # ------------------------------------------------------------------ #
    op.create_table(
        'work_units',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('work_order_id', sa.Integer(), nullable=False),
        sa.Column('unit_code', sa.String(length=30), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.Enum(
            'pending', 'assigned', 'in_progress', 'completed', 'cancelled',
            name='work_unit_status'
        ), nullable=False, server_default='pending'),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326,
                                       from_text='ST_GeomFromEWKT', name='geometry', spatial_index=False), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['work_order_id'], ['work_orders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unit_code'),
    )
    op.create_index(op.f('ix_work_units_id'), 'work_units', ['id'], unique=False)
    op.create_index(op.f('ix_work_units_work_order_id'), 'work_units', ['work_order_id'], unique=False)
    op.create_index(op.f('ix_work_units_unit_code'), 'work_units', ['unit_code'], unique=False)
    op.create_index('idx_work_units_status', 'work_units', ['status'], unique=False)
    op.create_index('idx_work_units_location', 'work_units', ['location'], unique=False, postgresql_using='gist')

    # ------------------------------------------------------------------ #
    # work_assignments                                                     #
    # ------------------------------------------------------------------ #
    op.create_table(
        'work_assignments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('worker_id', sa.Integer(), nullable=False),
        sa.Column('work_unit_id', sa.Integer(), nullable=False),
        sa.Column('work_order_id', sa.Integer(), nullable=False),
        sa.Column('assigned_by_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum(
            'pending', 'assigned', 'accepted', 'in_progress', 'completed', 'cancelled',
            name='assignment_status'
        ), nullable=False, server_default='assigned'),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['assigned_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['work_order_id'], ['work_orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['work_unit_id'], ['work_units.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_work_assignments_id'), 'work_assignments', ['id'], unique=False)
    op.create_index(op.f('ix_work_assignments_worker_id'), 'work_assignments', ['worker_id'], unique=False)
    op.create_index(op.f('ix_work_assignments_work_unit_id'), 'work_assignments', ['work_unit_id'], unique=False)
    op.create_index(op.f('ix_work_assignments_work_order_id'), 'work_assignments', ['work_order_id'], unique=False)
    op.create_index(op.f('ix_work_assignments_assigned_by_id'), 'work_assignments', ['assigned_by_id'], unique=False)
    op.create_index('idx_work_assignments_status', 'work_assignments', ['status'], unique=False)

    # ------------------------------------------------------------------ #
    # cleaning_evidence                                                    #
    # ------------------------------------------------------------------ #
    op.create_table(
        'cleaning_evidence',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('work_unit_id', sa.Integer(), nullable=False),
        sa.Column('work_assignment_id', sa.Integer(), nullable=True),
        sa.Column('submitted_by_id', sa.Integer(), nullable=True),
        sa.Column('evidence_type', sa.Enum(
            'before', 'progress', 'after',
            name='evidence_type'
        ), nullable=False, server_default='after'),
        sa.Column('image_url', sa.String(length=512), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326,
                                       from_text='ST_GeomFromEWKT', name='geometry', spatial_index=False), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['submitted_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['work_assignment_id'], ['work_assignments.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['work_unit_id'], ['work_units.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_cleaning_evidence_id'), 'cleaning_evidence', ['id'], unique=False)
    op.create_index(op.f('ix_cleaning_evidence_work_unit_id'), 'cleaning_evidence', ['work_unit_id'], unique=False)
    op.create_index(op.f('ix_cleaning_evidence_work_assignment_id'), 'cleaning_evidence', ['work_assignment_id'], unique=False)
    op.create_index(op.f('ix_cleaning_evidence_submitted_by_id'), 'cleaning_evidence', ['submitted_by_id'], unique=False)
    op.create_index('idx_cleaning_evidence_type', 'cleaning_evidence', ['evidence_type'], unique=False)
    op.create_index('idx_cleaning_evidence_location', 'cleaning_evidence', ['location'], unique=False, postgresql_using='gist')

    # ------------------------------------------------------------------ #
    # verifications                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        'verifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('evidence_id', sa.Integer(), nullable=True),
        sa.Column('work_unit_id', sa.Integer(), nullable=False),
        sa.Column('verifier_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum(
            'pending', 'approved', 'rejected', 'requires_review',
            name='verification_status'
        ), nullable=False, server_default='pending'),
        sa.Column('method', sa.Enum(
            'manual', 'ai_assisted', 'supervisor',
            name='verification_method'
        ), nullable=False, server_default='manual'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['evidence_id'], ['cleaning_evidence.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['verifier_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['work_unit_id'], ['work_units.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_verifications_id'), 'verifications', ['id'], unique=False)
    op.create_index(op.f('ix_verifications_evidence_id'), 'verifications', ['evidence_id'], unique=False)
    op.create_index(op.f('ix_verifications_work_unit_id'), 'verifications', ['work_unit_id'], unique=False)
    op.create_index(op.f('ix_verifications_verifier_id'), 'verifications', ['verifier_id'], unique=False)
    op.create_index('idx_verifications_status', 'verifications', ['status'], unique=False)

    # ------------------------------------------------------------------ #
    # compensations                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        'compensations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('worker_id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=False),
        sa.Column('verification_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='INR'),
        sa.Column('status', sa.Enum(
            'pending', 'eligible', 'processing', 'paid', 'rejected',
            name='compensation_status'
        ), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['assignment_id'], ['work_assignments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['verification_id'], ['verifications.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_compensations_id'), 'compensations', ['id'], unique=False)
    op.create_index(op.f('ix_compensations_worker_id'), 'compensations', ['worker_id'], unique=False)
    op.create_index(op.f('ix_compensations_assignment_id'), 'compensations', ['assignment_id'], unique=False)
    op.create_index(op.f('ix_compensations_verification_id'), 'compensations', ['verification_id'], unique=False)
    op.create_index('idx_compensations_status', 'compensations', ['status'], unique=False)

    # ------------------------------------------------------------------ #
    # collection_batches                                                   #
    # ------------------------------------------------------------------ #
    op.create_table(
        'collection_batches',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('batch_code', sa.String(length=30), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum(
            'collecting', 'sealed', 'in_transit', 'delivered',
            name='collection_batch_status'
        ), nullable=False, server_default='collecting'),
        sa.Column('total_volume_m3', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('collected_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('batch_code'),
    )
    op.create_index(op.f('ix_collection_batches_id'), 'collection_batches', ['id'], unique=False)
    op.create_index(op.f('ix_collection_batches_batch_code'), 'collection_batches', ['batch_code'], unique=False)
    op.create_index(op.f('ix_collection_batches_vehicle_id'), 'collection_batches', ['vehicle_id'], unique=False)
    op.create_index('idx_collection_batches_status', 'collection_batches', ['status'], unique=False)


def downgrade() -> None:
    # Drop in reverse order of foreign key dependencies
    op.drop_index('idx_collection_batches_status', table_name='collection_batches')
    op.drop_index(op.f('ix_collection_batches_vehicle_id'), table_name='collection_batches')
    op.drop_index(op.f('ix_collection_batches_batch_code'), table_name='collection_batches')
    op.drop_index(op.f('ix_collection_batches_id'), table_name='collection_batches')
    op.drop_table('collection_batches')

    op.drop_index('idx_compensations_status', table_name='compensations')
    op.drop_index(op.f('ix_compensations_verification_id'), table_name='compensations')
    op.drop_index(op.f('ix_compensations_assignment_id'), table_name='compensations')
    op.drop_index(op.f('ix_compensations_worker_id'), table_name='compensations')
    op.drop_index(op.f('ix_compensations_id'), table_name='compensations')
    op.drop_table('compensations')

    op.drop_index('idx_verifications_status', table_name='verifications')
    op.drop_index(op.f('ix_verifications_verifier_id'), table_name='verifications')
    op.drop_index(op.f('ix_verifications_work_unit_id'), table_name='verifications')
    op.drop_index(op.f('ix_verifications_evidence_id'), table_name='verifications')
    op.drop_index(op.f('ix_verifications_id'), table_name='verifications')
    op.drop_table('verifications')

    op.drop_index('idx_cleaning_evidence_location', table_name='cleaning_evidence', postgresql_using='gist')
    op.drop_index('idx_cleaning_evidence_type', table_name='cleaning_evidence')
    op.drop_index(op.f('ix_cleaning_evidence_submitted_by_id'), table_name='cleaning_evidence')
    op.drop_index(op.f('ix_cleaning_evidence_work_assignment_id'), table_name='cleaning_evidence')
    op.drop_index(op.f('ix_cleaning_evidence_work_unit_id'), table_name='cleaning_evidence')
    op.drop_index(op.f('ix_cleaning_evidence_id'), table_name='cleaning_evidence')
    op.drop_table('cleaning_evidence')

    op.drop_index('idx_work_assignments_status', table_name='work_assignments')
    op.drop_index(op.f('ix_work_assignments_assigned_by_id'), table_name='work_assignments')
    op.drop_index(op.f('ix_work_assignments_work_order_id'), table_name='work_assignments')
    op.drop_index(op.f('ix_work_assignments_work_unit_id'), table_name='work_assignments')
    op.drop_index(op.f('ix_work_assignments_worker_id'), table_name='work_assignments')
    op.drop_index(op.f('ix_work_assignments_id'), table_name='work_assignments')
    op.drop_table('work_assignments')

    op.drop_index('idx_work_units_location', table_name='work_units', postgresql_using='gist')
    op.drop_index('idx_work_units_status', table_name='work_units')
    op.drop_index(op.f('ix_work_units_unit_code'), table_name='work_units')
    op.drop_index(op.f('ix_work_units_work_order_id'), table_name='work_units')
    op.drop_index(op.f('ix_work_units_id'), table_name='work_units')
    op.drop_table('work_units')

    op.drop_index('idx_work_orders_status', table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_work_code'), table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_report_id'), table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_id'), table_name='work_orders')
    op.drop_table('work_orders')

    op.drop_index('idx_vehicles_status', table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_vehicle_code'), table_name='vehicles')
    op.drop_index(op.f('ix_vehicles_id'), table_name='vehicles')
    op.drop_table('vehicles')

    op.drop_index(op.f('ix_workers_worker_code'), table_name='workers')
    op.drop_index(op.f('ix_workers_user_id'), table_name='workers')
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')

    # Drop Phase 2 enum types
    op.execute("DROP TYPE IF EXISTS collection_batch_status;")
    op.execute("DROP TYPE IF EXISTS compensation_status;")
    op.execute("DROP TYPE IF EXISTS verification_method;")
    op.execute("DROP TYPE IF EXISTS verification_status;")
    op.execute("DROP TYPE IF EXISTS evidence_type;")
    op.execute("DROP TYPE IF EXISTS assignment_status;")
    op.execute("DROP TYPE IF EXISTS work_unit_status;")
    op.execute("DROP TYPE IF EXISTS work_order_status;")
    op.execute("DROP TYPE IF EXISTS worker_verification_state;")
    op.execute("DROP TYPE IF EXISTS worker_status;")
    op.execute("DROP TYPE IF EXISTS vehicle_status;")
