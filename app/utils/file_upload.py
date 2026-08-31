import uuid
from pathlib import Path
from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "static" / "profile_images"

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

async def save_profile_image(file: UploadFile | None) -> str | None:
    """
    Save a profile image locally.

    Returns:
        Unique filename if image is uploaded.
        None if no image is provided.
    """
    # 1. No file
    if not file or not file.filename:
        return None

    # 2. Validate content type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(
            "Only JPEG, PNG and WEBP images are allowed"
        )
    
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise ValueError(
            "Image size must be less than 5 MB"
        )

    # 5. Create upload directory
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # 6. Get extension
    file_extension = Path(
        file.filename
    ).suffix.lower()
    
    # 7. Generate unique filename
    saved_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    # 8. Complete path
    file_path = UPLOAD_DIR / saved_filename

    # 9. Save binary file
    with open(file_path, "wb") as f:
        f.write(content)

    # 10. Return filename
    return saved_filename