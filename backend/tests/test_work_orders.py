import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestWorkOrdersAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_work_order_success(self):
        # 1. Create Report
        rep_res = self.client.post("/api/v1/reports", json={
            "description": "Work order test site",
            "latitude": 12.9810,
            "longitude": 77.6010,
            "category": "mixed",
            "volume_tier": "bulk"
        })
        self.assertEqual(rep_res.status_code, 201)
        report_id = rep_res.json()["id"]

        # 2. Create Work Order
        wo_res = self.client.post("/api/v1/work-orders", json={
            "report_id": report_id,
            "classification": "BULK_RECOVERY",
            "required_worker_count": 2
        })
        self.assertEqual(wo_res.status_code, 201)
        wo_data = wo_res.json()
        self.assertIn("id", wo_data)
        self.assertEqual(wo_data["report_id"], report_id)
        self.assertEqual(wo_data["status"], "open")
        self.assertGreater(len(wo_data["units"]), 0)
        self.assertEqual(wo_data["units"][0]["status"], "pending")

        # 3. Retrieve Work Order
        wo_id = wo_data["id"]
        get_res = self.client.get(f"/api/v1/work-orders/{wo_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], wo_id)

    def test_create_work_order_invalid_report(self):
        wo_res = self.client.post("/api/v1/work-orders", json={
            "report_id": 999999,
            "classification": "BULK_RECOVERY",
            "required_worker_count": 1
        })
        self.assertEqual(wo_res.status_code, 400)

    def test_list_work_orders(self):
        res = self.client.get("/api/v1/work-orders?limit=10")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()
