from typing import List
import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating image embeddings using SigLIP model"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
    
    def load_model(self) -> None:
        """Load SigLIP model and processor"""
        try:
            logger.info(f"Loading embedding model: {settings.embedding_model}")
            
            self.processor = AutoProcessor.from_pretrained(settings.embedding_model)
            self.model = AutoModel.from_pretrained(settings.embedding_model)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise RuntimeError(f"Failed to load embedding model: {e}")
    
    def generate_embedding(self, image: Image.Image) -> List[float]:
        """
        Generate embedding vector for an image
        
        Args:
            image: PIL Image object
            
        Returns:
            List of floats representing the embedding vector
        """
        if self.model is None or self.processor is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Preprocess image
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                outputs = self.model.get_image_features(**inputs)
                
            # Normalize embedding (important for cosine similarity)
            embedding = outputs[0].cpu().numpy()
            embedding = embedding / (embedding**2).sum()**0.5
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Failed to generate embedding: {e}")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors"""
        return 768  # SigLIP base model dimension


# Global instance
embedding_service = EmbeddingService()
