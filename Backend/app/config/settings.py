from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Image Upload API"
    api_version: str = "v1"
    
    # Upload Configuration
    upload_dir: str = "../Images"
    max_file_size: int = 10485760  # 10MB in bytes
    allowed_extensions: str = "jpg,jpeg,png,gif,webp"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def upload_path(self) -> Path:
        """Get absolute upload directory path"""
        path = Path(__file__).parent.parent.parent / self.upload_dir
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Get list of allowed file extensions"""
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get list of CORS origins"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
