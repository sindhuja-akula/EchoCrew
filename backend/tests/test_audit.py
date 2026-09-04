import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAuditAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_audit_logs_recorded_and_retrievable(self):
        # 1. Trigger an operation that writes an audit log (e.g. creating a report)
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Audit trail verification report",
            "latitude": 12.9880,
            "longitude": 77.6080,
            "category": "dry",
            "volume_tier": "minor"
        })
        self.assertEqual(rep_res.status_code, 201)

        # 2. Query Audit Log API
        audit_res = self.client.get("/api/v1/audit?action=report_created")
        self.assertEqual(audit_res.status_code, 200)
        logs = audit_res.json()
        self.assertIsInstance(logs, list)
        self.assertGreater(len(logs), 0)

        # 3. Verify Log Content
        log_entry = logs[0]
        self.assertEqual(log_entry["action"], "report_created")
        self.assertEqual(log_entry["entity_type"], "GarbageReport")
        self.assertIn("created_at", log_entry)

        # 4. Retrieve Single Log
        single_res = self.client.get(f"/api/v1/audit/{log_entry['id']}")
        self.assertEqual(single_res.status_code, 200)
        self.assertEqual(single_res.json()["id"], log_entry["id"])

    def test_audit_log_not_found(self):
        res = self.client.get("/api/v1/audit/999999")
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
