import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestCompensationAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_compensation_eligibility_and_status_transition(self):
        # 1. Setup full workflow leading to approved verification
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Compensation flow report",
            "latitude": 12.9870,
            "longitude": 77.6070,
            "category": "dry",
            "volume_tier": "moderate"
        })
        report_id = rep_res.json()["id"]
        wo_res = self.client.post("/api/v1/work-orders", json={"report_id": report_id})
        work_unit_id = wo_res.json()["units"][0]["id"]

        unique_phone = f"+9195{int(time.time() * 1000) % 100000000:08d}"
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
            "image_url": "storage/uploads/comp_test.jpg"
        })
        evidence_id = ev_res.json()["id"]

        # Approve verification -> triggers auto-compensation eligibility
        ver_res = self.client.post("/api/v1/verifications", json={
            "work_unit_id": work_unit_id,
            "evidence_id": evidence_id,
            "status": "approved",
            "method": "manual"
        })
        self.assertEqual(ver_res.status_code, 201)

        # 2. Check Compensation Record
        comp_res = self.client.get(f"/api/v1/compensations?worker_id={worker_id}")
        self.assertEqual(comp_res.status_code, 200)
        comps = comp_res.json()
        self.assertGreater(len(comps), 0)
        comp = comps[0]
        self.assertEqual(comp["status"], "eligible")
        self.assertEqual(comp["amount"], 250.0)
        self.assertEqual(comp["currency"], "INR")
        comp_id = comp["id"]

        # 3. Retrieve single compensation
        get_res = self.client.get(f"/api/v1/compensations/{comp_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], comp_id)

        # 4. Transition Status: eligible -> processing
        patch_res = self.client.patch(
            f"/api/v1/compensations/{comp_id}/status", json={"status": "processing"}
        )
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.json()["status"], "processing")

if __name__ == "__main__":
    unittest.main()
