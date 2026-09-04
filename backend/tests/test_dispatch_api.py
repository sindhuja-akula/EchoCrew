import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestDispatchAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_work_order_dispatch_and_assignment_flow(self):
        # 1. Create Garbage Report
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Dispatch test report",
            "latitude": 12.9800,
            "longitude": 77.6000,
            "category": "mixed",
            "volume_tier": "bulk"
        })
        self.assertEqual(rep_res.status_code, 201)
        report_id = rep_res.json()["id"]

        # 2. Dispatch Work Order
        wo_res = self.client.post("/api/v1/work-orders", json={
            "report_id": report_id,
            "classification": "BULK_CLEANUP",
            "required_worker_count": 2
        })
        self.assertEqual(wo_res.status_code, 201)
        wo_data = wo_res.json()
        self.assertIn("units", wo_data)
        self.assertGreater(len(wo_data["units"]), 0)
        work_unit_id = wo_data["units"][0]["id"]

        # 3. Create Worker
        w_res = self.client.post("/api/v1/workers", json={
            "phone": f"+9197{int(time.time()) % 100000000:08d}"
        })
        worker_id = w_res.json()["id"]

        # 4. Assign Worker to Work Unit
        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        self.assertEqual(assign_res.status_code, 201)
        assign_data = assign_res.json()
        self.assertEqual(assign_data["status"], "assigned")
        assignment_id = assign_data["id"]

        # 5. Update Assignment Status to IN_PROGRESS and then COMPLETED
        patch1 = self.client.patch(f"/api/v1/assignments/{assignment_id}/status", json={"status": "in_progress"})
        self.assertEqual(patch1.status_code, 200)
        self.assertEqual(patch1.json()["status"], "in_progress")

        patch2 = self.client.patch(f"/api/v1/assignments/{assignment_id}/status", json={"status": "completed"})
        self.assertEqual(patch2.status_code, 200)
        self.assertEqual(patch2.json()["status"], "completed")

if __name__ == "__main__":
    unittest.main()
