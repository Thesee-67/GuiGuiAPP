"""
Routes de statistiques
Dashboard, progression, analytics
"""

from datetime import datetime, timedelta
from datetime import date as date_type
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.training_session import TrainingSession
from backend.models.running_session import RunningSession
from backend.models.route import Route
from backend.models.goal_category import GoalCategory

router = APIRouter()


# === SCHEMAS ===

class DashboardStats(BaseModel):
    total_training_sessions: int
    total_running_sessions: int
    total_routes: int
    current_month_sessions: int
    current_week_sessions: int
    goal_progress: list[dict]


class MonthlyVolume(BaseModel):
    month: str
    training_sessions: int
    running_sessions: int
    total_distance_km: float
    total_elevation_m: int


# === ROUTES ===

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques du dashboard
    """
    # Total séances d'entraînement
    total_training = db.query(func.count(TrainingSession.id)).filter(
        TrainingSession.user_id == current_user.id
    ).scalar()
    
    # Total séances course
    total_running = db.query(func.count(RunningSession.id)).filter(
        RunningSession.user_id == current_user.id
    ).scalar()
    
    # Total grandes voies
    total_routes = db.query(func.count(Route.id)).filter(
        Route.user_id == current_user.id
    ).scalar()
    
    # Séances du mois en cours
    first_day_month = date_type.today().replace(day=1)
    current_month = db.query(func.count(TrainingSession.id)).filter(
        TrainingSession.user_id == current_user.id,
        TrainingSession.date >= first_day_month
    ).scalar()
    
    # Séances de la semaine en cours
    start_of_week = date_type.today() - timedelta(days=date_type.today().weekday())
    current_week = db.query(func.count(TrainingSession.id)).filter(
        TrainingSession.user_id == current_user.id,
        TrainingSession.date >= start_of_week
    ).scalar()
    
    # Progression objectifs
    goal_categories = db.query(GoalCategory).filter(
        GoalCategory.user_id == current_user.id
    ).all()
    
    goal_progress = []
    for category in goal_categories:
        goal_progress.append({
            "name": category.name,
            "progress": category.progress
        })
    
    return {
        "total_training_sessions": total_training or 0,
        "total_running_sessions": total_running or 0,
        "total_routes": total_routes or 0,
        "current_month_sessions": current_month or 0,
        "current_week_sessions": current_week or 0,
        "goal_progress": goal_progress
    }


@router.get("/monthly-volume", response_model=list[MonthlyVolume])
def get_monthly_volume(
    months: int = 12,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère le volume mensuel d'entraînement
    """
    # Calculer la date de début
    start_date = date_type.today() - timedelta(days=30 * months)
    
    # Récupérer toutes les séances depuis cette date
    training_sessions = db.query(TrainingSession).filter(
        TrainingSession.user_id == current_user.id,
        TrainingSession.date >= start_date
    ).all()
    
    running_sessions = db.query(RunningSession).filter(
        RunningSession.user_id == current_user.id,
        RunningSession.date >= start_date
    ).all()
    
    # Agréger par mois
    monthly_data = {}
    
    for session in training_sessions:
        month_key = session.date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "month": session.date.strftime("%B %Y"),
                "training_sessions": 0,
                "running_sessions": 0,
                "total_distance_km": 0.0,
                "total_elevation_m": 0
            }
        monthly_data[month_key]["training_sessions"] += 1
    
    for session in running_sessions:
        month_key = session.date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "month": session.date.strftime("%B %Y"),
                "training_sessions": 0,
                "running_sessions": 0,
                "total_distance_km": 0.0,
                "total_elevation_m": 0
            }
        monthly_data[month_key]["running_sessions"] += 1
        monthly_data[month_key]["total_distance_km"] += session.distance_km or 0
        monthly_data[month_key]["total_elevation_m"] += session.elevation_gain_m or 0
    
    # Convertir en liste triée
    result = sorted(monthly_data.values(), key=lambda x: x["month"])
    
    return result


@router.get("/progression/{grade}")
def get_grade_progression(
    grade: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la progression sur une cotation donnée
    """
    routes = db.query(Route).filter(
        Route.user_id == current_user.id,
        Route.grade == grade
    ).order_by(Route.date_completed).all()
    
    return {
        "grade": grade,
        "count": len(routes),
        "routes": [
            {
                "name": r.name,
                "location": r.location,
                "date": r.date_completed,
                "style": r.style
            }
            for r in routes
        ]
    }


@router.get("/best-performances")
def get_best_performances(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les meilleures performances
    """
    # Meilleures voies
    best_routes = db.query(Route).filter(
        Route.user_id == current_user.id
    ).order_by(Route.grade.desc()).limit(limit).all()
    
    # Meilleures courses
    best_runs = db.query(RunningSession).filter(
        RunningSession.user_id == current_user.id,
        RunningSession.distance_km != None
    ).order_by(RunningSession.distance_km.desc()).limit(limit).all()
    
    return {
        "best_routes": [
            {
                "name": r.name,
                "grade": r.grade,
                "location": r.location,
                "date": r.date_completed
            }
            for r in best_routes
        ],
        "best_runs": [
            {
                "distance_km": r.distance_km,
                "date": r.date,
                "location": r.location,
                "duration_min": r.duration_min
            }
            for r in best_runs
        ]
    }