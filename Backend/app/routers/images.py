from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List

from app.services.image_service import ImageService
from app.models.image import ImageResponse, ImageListResponse, ErrorResponse
from app.config.settings import settings


router = APIRouter(prefix="/images", tags=["images"])


@router.post(
    "/upload",
    response_model=ImageResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        409: {"model": ErrorResponse, "description": "File already exists"},
    }
)
async def upload_image(file: UploadFile = File(...)):
    """Upload a single image"""
    return await ImageService.save_image(file)


@router.post(
    "/upload-multiple",
    response_model=List[ImageResponse],
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        409: {"model": ErrorResponse, "description": "File already exists"},
    }
)
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """Upload multiple images"""
    uploaded_images = []
    errors = []
    
    for file in files:
        try:
            image = await ImageService.save_image(file)
            uploaded_images.append(image)
        except HTTPException as e:
            errors.append({"filename": file.filename, "error": e.detail})
    
    if errors and not uploaded_images:
        raise HTTPException(status_code=400, detail=errors)
    
    return uploaded_images


@router.get(
    "",
    response_model=ImageListResponse,
    responses={
        200: {"description": "List of all images"}
    }
)
def get_images():
    """Get list of all uploaded images"""
    images = ImageService.get_all_images()
    return ImageListResponse(images=images, total=len(images))


@router.get(
    "/{filename}",
    response_class=FileResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Image not found"}
    }
)
def get_image(filename: str):
    """Get a specific image file"""
    file_path = settings.upload_path / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Image '{filename}' not found")
    
    # Determine media type from file extension
    import mimetypes
    media_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    
    return FileResponse(
        file_path,
        media_type=media_type,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600"
        }
    )


@router.delete(
    "/{filename}",
    status_code=204,
    responses={
        404: {"model": ErrorResponse, "description": "Image not found"}
    }
)
def delete_image(filename: str):
    """Delete an image"""
    ImageService.delete_image(filename)
    return None
