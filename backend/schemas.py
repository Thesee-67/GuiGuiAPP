"""
Schémas Pydantic communs
Utilisés dans plusieurs routes
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr


# === BASE SCHEMAS ===

class MessageResponse(BaseModel):
    """Réponse simple avec un message"""
    message: str


class ErrorResponse(BaseModel):
    """Réponse d'erreur"""
    detail: str
    status_code: int


class SuccessResponse(BaseModel):
    """Réponse de succès"""
    success: bool
    message: str | None = None


# === PAGINATION ===

class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseModel):
    """Réponse paginée générique"""
    items: list
    total: int
    skip: int
    limit: int
    has_more: bool


# === HEALTH CHECK ===

class HealthCheckResponse(BaseModel):
    """Réponse du health check"""
    status: str
    database: str
    timestamp: datetime