import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.utils.validation import validate_image_filename

class StorageService:
    def __init__(self, upload_dir: Optional[Path] = None):
        self.upload_dir = upload_dir or settings.UPLOADS_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload_file(self, file: UploadFile) -> str:
        """
        Saves uploaded photo to storage directory and returns accessible relative URL.
        """
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided for upload."
            )

        is_valid, msg = validate_image_filename(file.filename)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg
            )

        ext = Path(file.filename).suffix.lower()
        unique_filename = f"report_{uuid.uuid4().hex[:12]}{ext}"
        destination_path = self.upload_dir / unique_filename

        try:
            content = await file.read()
            if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
                )

            with open(destination_path, "wb") as f:
                f.write(content)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to store uploaded image: {str(e)}"
            )

        # Return web-accessible URL relative path
        return f"storage/uploads/{unique_filename}"

storage_service = StorageService()
