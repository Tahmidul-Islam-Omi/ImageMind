from typing import List, Dict, Any, Optional
import uuid
import time
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config.settings import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for managing Qdrant vector database operations"""
    
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.qdrant_collection
    
    def connect(self, max_retries: int = 3, retry_delay: int = 5) -> None:
        """
        Connect to Qdrant with retry logic
        
        Args:
            max_retries: Maximum number of connection attempts
            retry_delay: Delay in seconds between retries
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Connecting to Qdrant at {settings.qdrant_host}:{settings.qdrant_port} (attempt {attempt + 1}/{max_retries})")
                
                self.client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    timeout=10
                )
                
                # Test connection
                self.client.get_collections()
                
                logger.info("Successfully connected to Qdrant")
                return
                
            except Exception as e:
                logger.warning(f"Failed to connect to Qdrant (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("Failed to connect to Qdrant after all retries")
                    raise RuntimeError(f"Failed to connect to Qdrant: {e}")
    
    def create_collection(self, vector_size: int = 512) -> None:
        """
        Create Qdrant collection if it doesn't exist
        
        Args:
            vector_size: Dimension of the embedding vectors
        """
        if self.client is None:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            # Create collection
            logger.info(f"Creating collection '{self.collection_name}' with vector size {vector_size}")
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            
            logger.info(f"Collection '{self.collection_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise RuntimeError(f"Failed to create collection: {e}")
    
    def store_embedding(
        self,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> str:
        """
        Store image embedding with metadata in Qdrant
        
        Args:
            embedding: Image embedding vector
            metadata: Image metadata (filename, path, size, etc.)
            
        Returns:
            UUID of the stored point
        """
        if self.client is None:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Generate unique ID
            point_id = str(uuid.uuid4())
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )
            
            # Store in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Stored embedding for {metadata.get('filename')} with ID {point_id}")
            return point_id
            
        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            raise RuntimeError(f"Failed to store embedding: {e}")
    
    def delete_embedding(self, filename: str) -> bool:
        """
        Delete embedding by filename
        
        Args:
            filename: Name of the image file
            
        Returns:
            True if deleted successfully
        """
        if self.client is None:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Search for points with matching filename
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter={
                    "must": [
                        {
                            "key": "filename",
                            "match": {"value": filename}
                        }
                    ]
                },
                limit=1
            )
            
            points = search_result[0]
            
            if not points:
                logger.warning(f"No embedding found for {filename}")
                return False
            
            # Delete the point
            point_id = points[0].id
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id]
            )
            
            logger.info(f"Deleted embedding for {filename} (ID: {point_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete embedding: {e}")
            raise RuntimeError(f"Failed to delete embedding: {e}")
    
    def health_check(self) -> bool:
        """Check if Qdrant is healthy"""
        if self.client is None:
            return False
        
        try:
            self.client.get_collections()
            return True
        except:
            return False


# Global instance
qdrant_service = QdrantService()
