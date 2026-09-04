import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestReportEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_invalid_latitude(self):
        payload = {
            "description": "Invalid latitude report",
            "latitude": 120.0,  # Out of bounds
            "longitude": 77.5946,
            "category": "dry",
            "volume_tier": "minor"
        }
        response = self.client.post("/api/v1/reports", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_and_get_report_flow(self):
        payload = {
            "description": "Sidewalk electronic waste dump site",
            "latitude": 13.0100,
            "longitude": 77.6200,
            "category": "electronic",
            "volume_tier": "minor",
            "image_url": "storage/uploads/demo_ewaste_01.jpg"
        }
        create_res = self.client.post("/api/v1/reports", json=payload)
        self.assertEqual(create_res.status_code, 201)
        data = create_res.json()
        self.assertIn("id", data)
        self.assertEqual(data["category"], "electronic")
        self.assertEqual(data["status"], "reported")
        report_id = data["id"]

        # Fetch created report by ID
        get_res = self.client.get(f"/api/v1/reports/{report_id}")
        self.assertEqual(get_res.status_code, 200)
        report_detail = get_res.json()
        self.assertEqual(report_detail["id"], report_id)
        self.assertEqual(report_detail["latitude"], 13.0100)

    def test_spatial_deduplication_20m_radius(self):
        import time
        offset = (time.time() % 50) / 100.0
        base_lat = 12.500000 + offset
        base_lon = 77.500000 + offset

        # Report 1
        r1_payload = {
            "description": "Original report near square",
            "latitude": base_lat,
            "longitude": base_lon,
            "category": "dry",
            "volume_tier": "moderate"
        }
        res1 = self.client.post("/api/v1/reports", json=r1_payload)
        self.assertEqual(res1.status_code, 201)
        rep1_id = res1.json()["id"]

        # Report 2 (~ 11 meters away from Report 1)
        r2_payload = {
            "description": "Near duplicate report ~ 11m away",
            "latitude": base_lat + 0.000010,
            "longitude": base_lon + 0.000010,
            "category": "dry",
            "volume_tier": "minor"
        }
        res2 = self.client.post("/api/v1/reports", json=r2_payload)
        self.assertEqual(res2.status_code, 201)
        rep2_data = res2.json()
        
        # Spatial deduplication metadata check
        self.assertTrue(rep2_data["is_spatial_duplicate"])
        self.assertEqual(rep2_data["duplicate_of_report_id"], rep1_id)

    def test_list_reports_endpoint(self):
        response = self.client.get("/api/v1/reports?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("reports", data)
        self.assertIsInstance(data["reports"], list)

if __name__ == "__main__":
    unittest.main()
