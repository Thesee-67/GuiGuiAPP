"""
Application FastAPI principale
Training Escalade - Suivi d'entraînement escalade
"""

from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
import logging

from backend.config import settings
from backend.database import engine, get_db
from backend.middleware import setup_middlewares
from backend.api import api_router
from backend.schemas import HealthCheckResponse

# Configuration du logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Training Escalade API",
    description="API de suivi d'entraînement pour l'escalade et la course",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # Swagger UI uniquement en dev
    redoc_url="/redoc" if settings.DEBUG else None,  # ReDoc uniquement en dev
)

# Configuration des middlewares
setup_middlewares(app)

# Inclusion du router principal de l'API
app.include_router(api_router, prefix="/api")


# === ROUTES PRINCIPALES ===

@app.get("/")
def root():
    """
    Page d'accueil de l'API
    """
    return {
        "name": "Training Escalade API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.DEBUG else None
    }


@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    """
    Vérification de l'état de l'API et de la base de données
    """
    # Tester la connexion à la base de données
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow()
    }


# === ÉVÉNEMENTS DE DÉMARRAGE/ARRÊT ===

@app.on_event("startup")
async def startup_event():
    """
    Actions au démarrage de l'application
    """
    logger.info("=" * 60)
    logger.info("🚀 Training Escalade API - Démarrage")
    logger.info("=" * 60)
    logger.info(f"Environnement : {settings.ENVIRONMENT}")
    logger.info(f"Debug : {settings.DEBUG}")
    logger.info(f"Database : {settings.DATABASE_TYPE}")
    logger.info(f"Host : {settings.APP_HOST}:{settings.APP_PORT}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions à l'arrêt de l'application
    """
    logger.info("=" * 60)
    logger.info("🛑 Training Escalade API - Arrêt")
    logger.info("=" * 60)


# === GESTIONNAIRE D'ERREURS GLOBAL ===

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Gestionnaire pour les 404"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Resource not found",
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )