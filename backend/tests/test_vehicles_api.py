import unittest
import time
from fastapi.testclient import TestClient
from app.main import app

class TestVehiclesAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_vehicle_registration(self):
        unique_plate = f"KA-01-EQ-{int(time.time()) % 10000:04d}"
        payload = {
            "callsign": "CleanLoop-Echo-1",
            "license_plate": unique_plate,
            "vehicle_type": "UTILITY_TRUCK",
            "capacity_m3": 7.5
        }
        res = self.client.post("/api/v1/vehicles", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["license_plate"], unique_plate)
        self.assertEqual(data["capacity_m3"], 7.5)
        self.assertEqual(data["status"], "available")

    def test_list_vehicles(self):
        res = self.client.get("/api/v1/vehicles")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()
