import unittest
import io
import asyncio
from fastapi import UploadFile, HTTPException
from app.services.storage_service import storage_service

class TestStorageService(unittest.TestCase):
    def test_invalid_image_extension(self):
        file_obj = UploadFile(filename="malicious.exe", file=io.BytesIO(b"dummy text"))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            with self.assertRaises(HTTPException) as ctx:
                loop.run_until_complete(storage_service.save_upload_file(file_obj))
            self.assertEqual(ctx.exception.status_code, 400)
            self.assertIn("Unsupported file format", ctx.exception.detail)
        finally:
            loop.close()

    def test_valid_image_upload(self):
        fake_jpeg_content = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01"
        file_obj = UploadFile(filename="test_photo.jpg", file=io.BytesIO(fake_jpeg_content))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            url = loop.run_until_complete(storage_service.save_upload_file(file_obj))
            self.assertTrue(url.startswith("storage/uploads/"))
            self.assertTrue(url.endswith(".jpg"))
        finally:
            loop.close()

if __name__ == "__main__":
    unittest.main()
