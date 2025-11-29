# Image Upload Gallery

A full-stack image upload and management application with a beautiful Material-UI interface. Upload, view, download, and delete images with persistent storage.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-19.2.0-blue.svg)

## 🚀 Features

- ✨ **Drag & Drop Upload** - Intuitive file upload with drag-and-drop support
- 🖼️ **Image Gallery** - Responsive grid layout with beautiful hover effects
- 💾 **Persistent Storage** - Images saved to file system and persist across sessions
- 🗑️ **Delete Images** - Remove unwanted images with confirmation
- 💿 **Download Images** - Download images directly from the gallery
- 🎨 **Beautiful UI** - Modern gradient design with Material-UI components
- ✅ **File Validation** - Type checking, size limits, and duplicate detection
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🔒 **CORS Enabled** - Secure cross-origin resource sharing

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Tech Stack

### Frontend
- **React 19.2** - UI library
- **Vite** - Build tool and dev server
- **Material-UI (MUI)** - Component library
- **Emotion** - CSS-in-JS styling

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Pillow (PIL)** - Image processing and validation
- **Python 3.11+** - Programming language

## 📁 Project Structure

```
ImageMind/
├── Backend/                    # FastAPI backend
│   ├── app/
│   │   ├── config/            # Configuration and settings
│   │   │   └── settings.py    # Environment variables and app config
│   │   ├── models/            # Pydantic models
│   │   │   └── image.py       # Image response models
│   │   ├── routers/           # API route handlers
│   │   │   └── images.py      # Image upload/download/delete endpoints
│   │   ├── services/          # Business logic layer
│   │   │   └── image_service.py  # Image processing and validation
│   │   └── main.py            # FastAPI application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Development server runner
│   └── .env.example           # Environment variables template
│
├── Frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ImageUpload/   # Image upload components
│   │   │       ├── ImageUploadContainer.jsx  # Main container
│   │   │       ├── ImageUploadZone.jsx       # Drag & drop zone
│   │   │       ├── ImageGallery.jsx          # Gallery grid
│   │   │       ├── ImageCard.jsx             # Individual image card
│   │   │       └── index.js                  # Component exports
│   │   ├── services/
│   │   │   └── imageService.js  # API communication layer
│   │   ├── App.jsx            # Root component
│   │   └── main.jsx           # Application entry point
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
│
├── Images/                     # Image storage directory
└── README.md                   # This file
```

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+ and npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ImageMind
```

### 2. Backend Setup

```bash
# Navigate to Backend directory
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for custom configuration
copy .env.example .env
```

### 3. Frontend Setup

```bash
# Navigate to Frontend directory (open new terminal)
cd Frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd Backend

# Activate virtual environment if not already activated
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Run the server
python run.py

# Or use uvicorn directly
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Start Frontend Server

```bash
cd Frontend

# Run development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### Access the Application

Open your browser and navigate to **http://localhost:5173**

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Upload Single Image
```http
POST /images/upload
Content-Type: multipart/form-data

Body: file (image file)

Response: 201 Created
{
  "id": "image1.jpg",
  "name": "image1.jpg",
  "url": "/api/v1/images/image1.jpg",
  "size": 123456,
  "type": "image/jpeg",
  "uploaded_at": "2025-11-30T10:30:00"
}
```

#### Upload Multiple Images
```http
POST /images/upload-multiple
Content-Type: multipart/form-data

Body: files[] (multiple image files)

Response: 201 Created
[
  {
    "id": "image1.jpg",
    "name": "image1.jpg",
    "url": "/api/v1/images/image1.jpg",
    "size": 123456,
    "type": "image/jpeg",
    "uploaded_at": "2025-11-30T10:30:00"
  }
]
```

#### Get All Images
```http
GET /images

Response: 200 OK
{
  "images": [...],
  "total": 5
}
```

#### Get Specific Image
```http
GET /images/{filename}

Response: 200 OK (image file)
```

#### Delete Image
```http
DELETE /images/{filename}

Response: 204 No Content
```

### Error Responses

```json
{
  "detail": "Error message description"
}
```

Status Codes:
- `400` - Bad Request (invalid file, size exceeded)
- `404` - Not Found (image doesn't exist)
- `409` - Conflict (duplicate filename)
- `500` - Internal Server Error

## ⚙️ Configuration

### Backend Configuration

Edit `Backend/.env` or `Backend/app/config/settings.py`:

```python
# Upload directory (relative to Backend folder)
UPLOAD_DIR=../Images

# Maximum file size (10MB in bytes)
MAX_FILE_SIZE=10485760

# Allowed file extensions
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration

Edit `Frontend/src/services/imageService.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

## 🏗️ Architecture

### Clean Architecture Principles

The application follows clean architecture with clear separation of concerns:

**Backend Layers:**
1. **Routers** - Handle HTTP requests/responses
2. **Services** - Business logic and validation
3. **Models** - Data structures and validation schemas
4. **Config** - Application configuration

**Frontend Layers:**
1. **Components** - UI presentation
2. **Services** - API communication
3. **State Management** - React hooks (useState, useEffect)

### Data Flow

```
User Action
  ↓
Frontend Component
  ↓
Service Layer (API calls)
  ↓
Backend Router
  ↓
Service Layer (validation & business logic)
  ↓
File System (Images folder)
  ↓
Response back through layers
  ↓
UI Update
```

### Key Design Patterns

- **Repository Pattern** - Service layer abstracts data access
- **Dependency Injection** - Settings injected via Pydantic
- **Component Composition** - React components are modular and reusable
- **Callback Props** - Parent-child communication in React
- **Error Boundaries** - Graceful error handling with try-catch

## 🔒 Security Features

- File type validation (only images allowed)
- File size limits (10MB default)
- Image content verification using PIL
- Duplicate filename detection
- CORS configuration for allowed origins
- Input sanitization via Pydantic models

## 🧪 Testing

### Backend Tests
```bash
cd Backend
pytest
```

### Frontend Tests
```bash
cd Frontend
npm test
```

## 🐛 Troubleshooting

### Backend Issues

**Module not found error:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Change port in run.py or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Dependencies not installed:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Check backend CORS_ORIGINS setting includes frontend URL
- Verify backend server is running

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using React and FastAPI**
