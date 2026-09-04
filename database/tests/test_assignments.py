"""
Tests for WorkOrder, WorkUnit, and WorkAssignment models and status flows.
"""

import unittest
from database.models import (
    WorkOrder,
    WorkUnit,
    WorkAssignment,
    WorkOrderStatus,
    WorkUnitStatus,
    AssignmentStatus
)

class TestAssignments(unittest.TestCase):

    def test_assignment_enums(self):
        self.assertEqual(WorkOrderStatus.OPEN.value, "open")
        self.assertEqual(WorkOrderStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(WorkUnitStatus.PENDING.value, "pending")
        self.assertEqual(AssignmentStatus.ASSIGNED.value, "assigned")
        self.assertEqual(AssignmentStatus.COMPLETED.value, "completed")

    def test_work_order_instance_creation(self):
        work_order = WorkOrder(
            report_id=1,
            work_code="WO-2026-0001",
            classification="GENERAL_CLEANUP",
            required_worker_count=2,
            status=WorkOrderStatus.OPEN
        )
        self.assertEqual(work_order.work_code, "WO-2026-0001")
        self.assertEqual(work_order.required_worker_count, 2)
        self.assertEqual(work_order.status, WorkOrderStatus.OPEN)

    def test_work_unit_instance_creation(self):
        unit = WorkUnit(
            work_order_id=1,
            unit_code="WU-2026-0001-A",
            sequence_number=1,
            status=WorkUnitStatus.PENDING,
            latitude=12.9716,
            longitude=77.5946
        )
        self.assertEqual(unit.unit_code, "WU-2026-0001-A")
        self.assertEqual(unit.sequence_number, 1)
        self.assertEqual(unit.status, WorkUnitStatus.PENDING)

    def test_work_assignment_instance_creation(self):
        assignment = WorkAssignment(
            worker_id=1,
            work_unit_id=1,
            work_order_id=1,
            assigned_by_id=1,
            status=AssignmentStatus.ASSIGNED
        )
        self.assertEqual(assignment.worker_id, 1)
        self.assertEqual(assignment.work_unit_id, 1)
        self.assertEqual(assignment.status, AssignmentStatus.ASSIGNED)

if __name__ == "__main__":
    unittest.main()
