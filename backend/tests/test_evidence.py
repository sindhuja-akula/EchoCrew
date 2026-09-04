import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestEvidenceAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_submit_and_get_evidence(self):
        # 1. Setup report & work order
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Evidence submission test",
            "latitude": 12.9840,
            "longitude": 77.6040,
            "category": "dry",
            "volume_tier": "minor"
        })
        report_id = rep_res.json()["id"]
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        unique_phone = f"+9193{int(time.time() * 1000) % 100000000:08d}"
        w_res = self.client.post("/api/v1/workers", json={"phone": unique_phone})
        worker_id = w_res.json()["id"]

        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        assignment_id = assign_res.json()["id"]

        # 2. Submit Evidence
        ev_res = self.client.post("/api/v1/evidence", json={
            "work_unit_id": work_unit_id,
            "work_assignment_id": assignment_id,
            "evidence_type": "after",
            "image_url": "storage/uploads/test_after.jpg",
            "latitude": 12.9840,
            "longitude": 77.6040
        })
        self.assertEqual(ev_res.status_code, 201)
        ev_data = ev_res.json()
        self.assertIn("id", ev_data)
        self.assertEqual(ev_data["evidence_type"], "after")
        evidence_id = ev_data["id"]

        # 3. Retrieve Evidence
        get_res = self.client.get(f"/api/v1/evidence/{evidence_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], evidence_id)

    def test_submit_evidence_invalid_work_unit(self):
        ev_res = self.client.post("/api/v1/evidence", json={
            "work_unit_id": 999999,
            "evidence_type": "after",
            "image_url": "storage/uploads/test.jpg"
        })
        self.assertEqual(ev_res.status_code, 400)

if __name__ == "__main__":
    unittest.main()
