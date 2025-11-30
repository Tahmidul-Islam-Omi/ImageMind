from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from app.config.settings import settings
from app.routers import images
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_services():
    """Initialize all required services on startup"""
    try:
        logger.info("=" * 60)
        logger.info("Initializing Image Upload API")
        logger.info("=" * 60)
        
        # 1. Load embedding model
        logger.info("Step 1/3: Loading SigLIP embedding model...")
        embedding_service.load_model()
        logger.info("✓ Embedding model loaded successfully")
        
        # 2. Connect to Qdrant
        logger.info("Step 2/3: Connecting to Qdrant...")
        qdrant_service.connect(max_retries=3, retry_delay=5)
        logger.info("✓ Connected to Qdrant successfully")
        
        # 3. Create collection
        logger.info("Step 3/3: Setting up Qdrant collection...")
        qdrant_service.create_collection(
            vector_size=embedding_service.get_embedding_dimension()
        )
        logger.info("✓ Qdrant collection ready")
        
        logger.info("=" * 60)
        logger.info("✓ All services initialized successfully")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"✗ Failed to initialize services: {e}")
        logger.error("=" * 60)
        logger.error("Backend startup aborted. Please check the error above.")
        sys.exit(1)


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="API for uploading and managing images with vector embeddings"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services on startup
@app.on_event("startup")
async def startup_event():
    """Run initialization on startup"""
    initialize_services()

# Include routers
app.include_router(images.router, prefix=f"/api/{settings.api_version}")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.api_version,
        "docs": "/docs",
        "embedding_model": settings.embedding_model,
        "qdrant_collection": settings.qdrant_collection
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    qdrant_healthy = qdrant_service.health_check()
    model_loaded = embedding_service.model is not None
    
    return {
        "status": "healthy" if (qdrant_healthy and model_loaded) else "degraded",
        "qdrant": "connected" if qdrant_healthy else "disconnected",
        "embedding_model": "loaded" if model_loaded else "not loaded"
    }
