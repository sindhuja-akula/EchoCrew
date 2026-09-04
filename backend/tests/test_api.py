import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestScaffoldingAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

if __name__ == "__main__":
    unittest.main()
