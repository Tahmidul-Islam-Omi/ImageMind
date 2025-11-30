"""
Setup Verification Script
Run this to verify all components are working correctly
"""
import sys
import requests
from qdrant_client import QdrantClient


def check_qdrant():
    """Check if Qdrant is running"""
    print("Checking Qdrant...")
    try:
        client = QdrantClient(host="localhost", port=6333, timeout=5)
        client.get_collections()
        print("✓ Qdrant is running and accessible")
        return True
    except Exception as e:
        print(f"✗ Qdrant check failed: {e}")
        print("  → Start Qdrant: docker-compose up -d")
        return False


def check_backend():
    """Check if backend is running"""
    print("\nChecking Backend...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        data = response.json()
        
        if data.get("status") == "healthy":
            print("✓ Backend is running and healthy")
            print(f"  - Qdrant: {data.get('qdrant')}")
            print(f"  - Embedding model: {data.get('embedding_model')}")
            return True
        else:
            print(f"✗ Backend is degraded: {data}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running")
        print("  → Start backend: python run.py")
        return False
    except Exception as e:
        print(f"✗ Backend check failed: {e}")
        return False


def check_frontend():
    """Check if frontend is running"""
    print("\nChecking Frontend...")
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✓ Frontend is running")
            return True
        else:
            print(f"✗ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Frontend is not running")
        print("  → Start frontend: cd Frontend && npm run dev")
        return False
    except Exception as e:
        print(f"✗ Frontend check failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Image Upload API - Setup Verification")
    print("=" * 60)
    
    qdrant_ok = check_qdrant()
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Qdrant:   {'✓ OK' if qdrant_ok else '✗ FAILED'}")
    print(f"Backend:  {'✓ OK' if backend_ok else '✗ FAILED'}")
    print(f"Frontend: {'✓ OK' if frontend_ok else '✗ FAILED'}")
    print("=" * 60)
    
    if qdrant_ok and backend_ok and frontend_ok:
        print("\n✓ All systems operational!")
        print("  → Open http://localhost:5173 to use the app")
        sys.exit(0)
    else:
        print("\n✗ Some components are not running")
        print("  → Check the messages above for instructions")
        sys.exit(1)


if __name__ == "__main__":
    main()
