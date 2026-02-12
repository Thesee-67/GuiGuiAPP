"""
Middlewares FastAPI
CORS, gestion d'erreurs, rate limiting
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time

from backend.config import settings

logger = logging.getLogger(__name__)


def setup_cors(app: FastAPI):
    """
    Configure CORS pour l'application
    
    Args:
        app: Application FastAPI
    """
    origins = [
        "http://localhost:3000",  # React dev
        "http://localhost:8000",  # FastAPI dev
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Ajouter l'URL de production si définie
    if settings.APP_URL:
        origins.append(settings.APP_URL)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    logger.info(f"CORS configuré pour : {origins}")


def setup_exception_handlers(app: FastAPI):
    """
    Configure les gestionnaires d'exceptions
    
    Args:
        app: Application FastAPI
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Gestionnaire pour les exceptions HTTP"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Gestionnaire pour les erreurs de validation"""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.errors(),
                "body": exc.body,
                "status_code": 422
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Gestionnaire pour toutes les autres exceptions"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        # En production, ne pas exposer les détails de l'erreur
        if settings.ENVIRONMENT == "production":
            detail = "Internal server error"
        else:
            detail = str(exc)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": detail,
                "status_code": 500
            }
        )


def setup_logging_middleware(app: FastAPI):
    """
    Configure le middleware de logging des requêtes
    
    Args:
        app: Application FastAPI
    """
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log toutes les requêtes"""
        start_time = time.time()
        
        # Traiter la requête
        response = await call_next(request)
        
        # Calculer le temps de traitement
        process_time = time.time() - start_time
        
        # Logger
        logger.info(
            f"{request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Time: {process_time:.3f}s"
        )
        
        # Ajouter le temps de traitement dans les headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_security_headers(app: FastAPI):
    """
    Configure les headers de sécurité
    
    Args:
        app: Application FastAPI
    """
    
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """Ajoute les headers de sécurité"""
        response = await call_next(request)
        
        # Headers de sécurité
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


def setup_middlewares(app: FastAPI):
    """
    Configure tous les middlewares
    
    Args:
        app: Application FastAPI
    """
    setup_cors(app)
    setup_exception_handlers(app)
    setup_logging_middleware(app)
    
    # Headers de sécurité uniquement en production
    if settings.ENVIRONMENT == "production":
        setup_security_headers(app)
    
    logger.info("Middlewares configurés")