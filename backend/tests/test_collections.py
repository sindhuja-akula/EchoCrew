import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestCollectionsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_collection_batch_lifecycle(self):
        # 1. Create Collection Batch
        create_res = self.client.post("/api/v1/collections", json={
            "total_volume_m3": 8.5
        })
        self.assertEqual(create_res.status_code, 201)
        batch = create_res.json()
        self.assertIn("id", batch)
        self.assertEqual(batch["status"], "collecting")
        self.assertEqual(batch["total_volume_m3"], 8.5)
        batch_id = batch["id"]

        # 2. Retrieve Batch
        get_res = self.client.get(f"/api/v1/collections/{batch_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], batch_id)

        # 3. Update Status: collecting -> sealed
        patch_res = self.client.patch(
            f"/api/v1/collections/{batch_id}/status", json={"status": "sealed"}
        )
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.json()["status"], "sealed")

        # 4. List Batches
        list_res = self.client.get("/api/v1/collections")
        self.assertEqual(list_res.status_code, 200)
        self.assertIsInstance(list_res.json(), list)

if __name__ == "__main__":
    unittest.main()
