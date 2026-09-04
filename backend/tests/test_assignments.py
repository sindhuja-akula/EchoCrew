import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestAssignmentsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_assignment_lifecycle_flow(self):
        # 1. Create Report & Work Order
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Assignment lifecycle report",
            "latitude": 12.9820,
            "longitude": 77.6020,
            "category": "dry",
            "volume_tier": "moderate"
        })
        self.assertEqual(rep_res.status_code, 201)
        report_id = rep_res.json()["id"]

        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        self.assertEqual(wo_res.status_code, 201)
        work_unit_id = wo_res.json()["units"][0]["id"]

        # 2. Register Active Worker
        unique_phone = f"+9191{int(time.time() * 1000) % 100000000:08d}"
        w_res = self.client.post("/api/v1/workers", json={"phone": unique_phone})
        self.assertEqual(w_res.status_code, 201)
        worker_id = w_res.json()["id"]

        # 3. Assign Worker to Work Unit
        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        self.assertEqual(assign_res.status_code, 201)
        assign_data = assign_res.json()
        self.assertEqual(assign_data["status"], "assigned")
        assignment_id = assign_data["id"]

        # 4. Accept Assignment
        patch_accept = self.client.patch(
            f"/api/v1/assignments/{assignment_id}/status", json={"status": "accepted"}
        )
        self.assertEqual(patch_accept.status_code, 200)
        self.assertEqual(patch_accept.json()["status"], "accepted")

        # 5. Start Work (in_progress)
        patch_start = self.client.patch(
            f"/api/v1/assignments/{assignment_id}/status", json={"status": "in_progress"}
        )
        self.assertEqual(patch_start.status_code, 200)
        self.assertEqual(patch_start.json()["status"], "in_progress")

        # 6. Complete Work
        patch_complete = self.client.patch(
            f"/api/v1/assignments/{assignment_id}/status", json={"status": "completed"}
        )
        self.assertEqual(patch_complete.status_code, 200)
        self.assertEqual(patch_complete.json()["status"], "completed")

    def test_invalid_lifecycle_transition(self):
        # Setup assignment
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Invalid transition test report",
            "latitude": 12.9830,
            "longitude": 77.6030,
            "category": "wet",
            "volume_tier": "minor"
        })
        report_id = rep_res.json()["id"]
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        unique_phone = f"+9192{int(time.time() * 1000) % 100000000:08d}"
        w_res = self.client.post("/api/v1/workers", json={"phone": unique_phone})
        worker_id = w_res.json()["id"]

        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        assignment_id = assign_res.json()["id"]

        # Jump straight from assigned to completed (invalid)
        bad_patch = self.client.patch(
            f"/api/v1/assignments/{assignment_id}/status", json={"status": "completed"}
        )
        self.assertEqual(bad_patch.status_code, 400)

if __name__ == "__main__":
    unittest.main()
