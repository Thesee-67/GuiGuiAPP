"""
API Routes
Toutes les routes de l'API
"""

from fastapi import APIRouter

from backend.api import auth, users, exercises, sessions, routes, goals, running, programs, stats

# Router principal de l'API
api_router = APIRouter()

# Inclure tous les routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(routes.router, prefix="/routes", tags=["Routes"])
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])
api_router.include_router(running.router, prefix="/running", tags=["Running"])
api_router.include_router(programs.router, prefix="/programs", tags=["Programs"])
api_router.include_router(stats.router, prefix="/stats", tags=["Stats"])

__all__ = ["api_router"]