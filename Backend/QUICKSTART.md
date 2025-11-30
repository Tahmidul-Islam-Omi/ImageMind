# Quick Start Guide

## Setup in 5 Steps

### 1. Start Qdrant
```bash
cd Backend
docker-compose up -d
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
**Note:** First run will download ~500MB SigLIP model

### 4. Start Backend
```bash
python run.py
```

**Expected startup output:**
```
============================================================
Initializing Image Upload API
============================================================
Step 1/3: Loading SigLIP embedding model...
✓ Embedding model loaded successfully
Step 2/3: Connecting to Qdrant...
✓ Connected to Qdrant successfully
Step 3/3: Setting up Qdrant collection...
✓ Qdrant collection ready
============================================================
✓ All services initialized successfully
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "qdrant": "connected",
  "embedding_model": "loaded"
}
```

## What Happens on Image Upload?

```
User uploads image
  ↓
1. Validate image (type, size, duplicate)
  ↓
2. Save to Images/ folder
  ↓
3. Generate SigLIP embedding (512D vector)
  ↓
4. Store embedding + metadata in Qdrant
  ↓
5. Return success to user
```

## Troubleshooting

### Qdrant not running
```bash
docker ps | grep qdrant
# If not running:
docker-compose up -d
```

### Backend won't start
Check the error message:
- **"Failed to load embedding model"** → Check internet connection
- **"Failed to connect to Qdrant"** → Start Qdrant with docker-compose
- **"Port already in use"** → Kill process or change port

### Model download slow
First run downloads ~500MB model. Subsequent runs use cached model from `~/.cache/huggingface/`

## Configuration

Edit `.env` file (copy from `.env.example`):

```env
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=image_embeddings

# Model
EMBEDDING_MODEL=google/siglip-base-patch16-224
```

## Next Steps

- Start frontend: `cd Frontend && npm run dev`
- Upload images and see embeddings stored automatically
- Check Qdrant dashboard: http://localhost:6333/dashboard
- View API docs: http://localhost:8000/docs
