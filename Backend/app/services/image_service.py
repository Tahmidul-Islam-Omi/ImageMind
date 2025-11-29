from pathlib import Path
from typing import List
import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from app.config.settings import settings
from app.models.image import ImageResponse


class ImageService:
    """Service for handling image operations"""
    
    @staticmethod
    def validate_image(file: UploadFile) -> None:
        """Validate uploaded image file"""
        # Check file extension
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_extensions_list)}"
            )
    
    @staticmethod
    def validate_image_content(content: bytes) -> None:
        """Validate image content using PIL"""
        try:
            image = Image.open(io.BytesIO(content))
            image.verify()
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid image file or corrupted image"
            )
    
    @staticmethod
    async def save_image(file: UploadFile) -> ImageResponse:
        """Save uploaded image to file system"""
        # Validate file
        ImageService.validate_image(file)
        
        # Check file size
        content = await file.read()
        if len(content) > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {settings.max_file_size / 1024 / 1024}MB"
            )
        
        # Validate image content
        ImageService.validate_image_content(content)
        
        # Check if file already exists
        file_path = settings.upload_path / file.filename
        if file_path.exists():
            raise HTTPException(
                status_code=409,
                detail=f"File '{file.filename}' already exists"
            )
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Create response
        return ImageResponse(
            id=file.filename,
            name=file.filename,
            url=f"/api/v1/images/{file.filename}",
            size=len(content),
            type=file.content_type or "image/jpeg",
            uploaded_at=datetime.now().isoformat()
        )
    
    @staticmethod
    def get_all_images() -> List[ImageResponse]:
        """Get list of all uploaded images"""
        images = []
        upload_path = settings.upload_path
        
        if not upload_path.exists():
            return images
        
        for file_path in upload_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower().lstrip('.') in settings.allowed_extensions_list:
                stat = file_path.stat()
                images.append(ImageResponse(
                    id=file_path.name,
                    name=file_path.name,
                    url=f"/api/v1/images/{file_path.name}",
                    size=stat.st_size,
                    type=f"image/{file_path.suffix.lstrip('.')}",
                    uploaded_at=datetime.fromtimestamp(stat.st_mtime).isoformat()
                ))
        
        # Sort by upload time (newest first)
        images.sort(key=lambda x: x.uploaded_at, reverse=True)
        return images
    
    @staticmethod
    def delete_image(filename: str) -> bool:
        """Delete an image from file system"""
        file_path = settings.upload_path / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Image '{filename}' not found"
            )
        
        try:
            file_path.unlink()
            return True
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete image: {str(e)}"
            )
