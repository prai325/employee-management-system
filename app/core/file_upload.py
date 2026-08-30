import os
import uuid
from pathlib import Path
from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "static" / "profile_images"

async def save_profile_image(file: UploadFile | None) -> str | None:
    """
    Takes an UploadFile, generates a unique name, saves it locally, 
    and returns the unique filename. Returns None if no file is uploaded.
    """

    if not file or not file.filename:
        return None

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1]

    saved_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return saved_filename

