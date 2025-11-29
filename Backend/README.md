# Image Upload Backend API

FastAPI backend for image upload and management.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (optional):
```bash
copy .env.example .env
```

5. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

- `POST /api/v1/images/upload` - Upload single image
- `POST /api/v1/images/upload-multiple` - Upload multiple images
- `GET /api/v1/images` - Get list of all images
- `GET /api/v1/images/{filename}` - Get specific image
- `DELETE /api/v1/images/{filename}` - Delete image

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

```
Backend/
├── app/
│   ├── config/          # Configuration and settings
│   ├── models/          # Pydantic models
│   ├── routers/         # API routes
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── requirements.txt
└── .env.example
```
