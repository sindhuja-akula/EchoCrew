import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestWorkersAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_worker_registration_and_status_flow(self):
        unique_phone = f"+9198{int(time.time()) % 100000000:08d}"
        payload = {
            "phone": unique_phone,
            "identity_ref": "REF-ID-9999"
        }
        res = self.client.post("/api/v1/workers", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["phone"], unique_phone)
        self.assertEqual(data["status"], "available")
        worker_id = data["id"]

        # Get worker details
        get_res = self.client.get(f"/api/v1/workers/{worker_id}")
        self.assertEqual(get_res.status_code, 200)

        # Update worker status
        patch_res = self.client.patch(f"/api/v1/workers/{worker_id}/status", json={"status": "off_duty"})
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.json()["status"], "off_duty")

    def test_list_workers_api(self):
        res = self.client.get("/api/v1/workers")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()
