import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestVerificationAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_approve_verification_flow(self):
        # 1. Setup report, work order, worker, assignment, evidence
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Verification approval test",
            "latitude": 12.9850,
            "longitude": 77.6050,
            "category": "dry",
            "volume_tier": "minor"
        })
        report_id = rep_res.json()["id"]
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        unique_phone = f"+9194{int(time.time() * 1000) % 100000000:08d}"
        w_res = self.client.post("/api/v1/workers", json={"phone": unique_phone})
        worker_id = w_res.json()["id"]

        assign_res = self.client.post("/api/v1/assignments", json={
            "worker_id": worker_id,
            "work_unit_id": work_unit_id
        })
        assignment_id = assign_res.json()["id"]

        ev_res = self.client.post("/api/v1/evidence", json={
            "work_unit_id": work_unit_id,
            "work_assignment_id": assignment_id,
            "evidence_type": "after",
            "image_url": "storage/uploads/verify_test.jpg"
        })
        evidence_id = ev_res.json()["id"]

        # 2. Submit Verification (Approved)
        ver_res = self.client.post("/api/v1/verifications", json={
            "work_unit_id": work_unit_id,
            "evidence_id": evidence_id,
            "status": "approved",
            "method": "supervisor",
            "notes": "Quality verified by field supervisor"
        })
        self.assertEqual(ver_res.status_code, 201)
        ver_data = ver_res.json()
        self.assertEqual(ver_data["status"], "approved")
        self.assertEqual(ver_data["method"], "supervisor")
        ver_id = ver_data["id"]

        # 3. Retrieve Verification
        get_res = self.client.get(f"/api/v1/verifications/{ver_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], ver_id)

    def test_reject_verification_flow(self):
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Verification reject test",
            "latitude": 12.9860,
            "longitude": 77.6060,
            "category": "dry",
            "volume_tier": "minor"
        })
        report_id = rep_res.json()["id"]
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        ver_res = self.client.post("/api/v1/verifications", json={
            "work_unit_id": work_unit_id,
            "status": "rejected",
            "method": "manual",
            "notes": "Incomplete cleanup area"
        })
        self.assertEqual(ver_res.status_code, 201)
        self.assertEqual(ver_res.json()["status"], "rejected")

if __name__ == "__main__":
    unittest.main()
