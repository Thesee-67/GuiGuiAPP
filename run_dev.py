"""
Script de lancement en mode développement
Lance le serveur FastAPI avec auto-reload
"""

import uvicorn
from backend.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Training Escalade API - Mode Développement")
    print("=" * 60)
    print(f"🌐 URL : http://{settings.APP_HOST}:{settings.APP_PORT}")
    print(f"📚 Docs : http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    print(f"🔧 ReDoc : http://{settings.APP_HOST}:{settings.APP_PORT}/redoc")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "backend.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        log_level="info"
    )