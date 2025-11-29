from pydantic import BaseModel
from datetime import datetime


class ImageResponse(BaseModel):
    """Response model for image data"""
    id: str
    name: str
    url: str
    size: int
    type: str
    uploaded_at: str


class ImageListResponse(BaseModel):
    """Response model for list of images"""
    images: list[ImageResponse]
    total: int


class ErrorResponse(BaseModel):
    """Response model for errors"""
    detail: str
