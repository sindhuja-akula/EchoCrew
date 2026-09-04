"""003_audit_log - Create audit_logs table for operational event trail

Revision ID: 003_audit_log
Revises: 002_phase2_extensions
Create Date: 2026-09-05

"""
from alembic import op
import sqlalchemy as sa

revision = '003_audit_log'
down_revision = '002_phase2_extensions'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('action', sa.Enum(
            'report_created', 'worker_created', 'work_order_created',
            'worker_assigned', 'assignment_accepted', 'work_started',
            'evidence_submitted', 'work_completed', 'verification_approved',
            'verification_rejected', 'compensation_eligible',
            'collection_batch_created', 'vehicle_created', 'assignment_cancelled',
            name='audit_action'
        ), nullable=False),
        sa.Column('entity_type', sa.String(64), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('actor_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_entity', 'audit_logs', ['entity_type', 'entity_id'])
    op.create_index('idx_audit_logs_actor', 'audit_logs', ['actor_id'])


def downgrade() -> None:
    op.drop_index('idx_audit_logs_actor', table_name='audit_logs')
    op.drop_index('idx_audit_logs_entity', table_name='audit_logs')
    op.drop_index('idx_audit_logs_action', table_name='audit_logs')
    op.drop_table('audit_logs')
    op.execute("DROP TYPE IF EXISTS audit_action")
