import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestVerificationAndCollectionsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_full_evidence_verification_compensation_and_collection_flow(self):
        # 1. Create Report
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Full lifecycle report",
            "latitude": 12.9900,
            "longitude": 77.6100,
            "category": "dry",
            "volume_tier": "moderate"
        })
        report_id = rep_res.json()["id"]

        # 2. Work Order & Unit
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        # 3. Worker & Assignment
        w_res = self.client.post("/api/v1/workers", json={"phone": f"+9196{int(time.time()) % 100000000:08d}"})
        worker_id = w_res.json()["id"]
        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        assignment_id = assign_res.json()["id"]

        # 4. Submit Evidence Photo
        ev_res = self.client.post("/api/v1/evidence", json={
            "work_unit_id": work_unit_id,
            "work_assignment_id": assignment_id,
            "evidence_type": "after",
            "image_url": "storage/uploads/after_clean_01.jpg",
            "latitude": 12.9900,
            "longitude": 77.6100
        })
        self.assertEqual(ev_res.status_code, 201)
        evidence_id = ev_res.json()["id"]

        # 5. Submit Verification Decision (Approved)
        ver_res = self.client.post("/api/v1/verifications", json={
            "work_unit_id": work_unit_id,
            "evidence_id": evidence_id,
            "status": "approved",
            "method": "manual",
            "notes": "Verified cleanup site"
        })
        self.assertEqual(ver_res.status_code, 201)
        self.assertEqual(ver_res.json()["status"], "approved")

        # 6. Check Compensation Eligibility Record
        comp_res = self.client.get(f"/api/v1/compensations?worker_id={worker_id}")
        self.assertEqual(comp_res.status_code, 200)
        comps = comp_res.json()
        self.assertGreater(len(comps), 0)
        self.assertEqual(comps[0]["amount"], 250.0)
        self.assertEqual(comps[0]["status"], "eligible")

        # 7. Create Collection Batch
        batch_res = self.client.post("/api/v1/collections", json={
            "total_volume_m3": 4.5
        })
        self.assertEqual(batch_res.status_code, 201)
        batch_data = batch_res.json()
        self.assertEqual(batch_data["total_volume_m3"], 4.5)
        self.assertEqual(batch_data["status"], "collecting")

if __name__ == "__main__":
    unittest.main()
