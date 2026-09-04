"""
Tests for Worker and Vehicle models, verification states, and vehicle statuses.
"""

import unittest
from database.models import (
    Worker,
    Vehicle,
    WorkerStatus,
    WorkerVerificationState,
    VehicleStatus
)

class TestWorkersAndVehicles(unittest.TestCase):

    def test_worker_enums(self):
        self.assertEqual(WorkerStatus.AVAILABLE.value, "available")
        self.assertEqual(WorkerStatus.ASSIGNED.value, "assigned")
        self.assertEqual(WorkerVerificationState.VERIFIED.value, "verified")
        self.assertEqual(WorkerVerificationState.UNVERIFIED.value, "unverified")

    def test_vehicle_enums(self):
        self.assertEqual(VehicleStatus.AVAILABLE.value, "available")
        self.assertEqual(VehicleStatus.DEPLOYED.value, "deployed")
        self.assertEqual(VehicleStatus.MAINTENANCE.value, "maintenance")

    def test_worker_instance_creation(self):
        worker = Worker(
            worker_code="WRK-001",
            phone="+919876543210",
            status=WorkerStatus.AVAILABLE,
            verification_state=WorkerVerificationState.VERIFIED,
            identity_ref="ID-1001"
        )
        self.assertEqual(worker.worker_code, "WRK-001")
        self.assertEqual(worker.phone, "+919876543210")
        self.assertEqual(worker.status, WorkerStatus.AVAILABLE)
        self.assertEqual(worker.verification_state, WorkerVerificationState.VERIFIED)

    def test_vehicle_instance_creation(self):
        vehicle = Vehicle(
            vehicle_code="TRK-01",
            callsign="CleanLoop-1",
            license_plate="KA-01-EA-1234",
            vehicle_type="UTILITY_TRUCK",
            capacity_m3=5.0,
            status=VehicleStatus.AVAILABLE
        )
        self.assertEqual(vehicle.vehicle_code, "TRK-01")
        self.assertEqual(vehicle.callsign, "CleanLoop-1")
        self.assertEqual(vehicle.capacity_m3, 5.0)
        self.assertEqual(vehicle.status, VehicleStatus.AVAILABLE)

if __name__ == "__main__":
    unittest.main()
