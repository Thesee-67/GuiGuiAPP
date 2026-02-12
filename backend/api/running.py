"""
Routes de gestion des séances de course à pied
CRUD sur les running sessions
"""

from datetime import datetime
from datetime import date as date_type
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.running_session import RunningSession

router = APIRouter()


# === SCHEMAS ===

class RunningSessionResponse(BaseModel):
    id: int
    user_id: int
    date: date_type
    duration_min: int | None
    distance_km: float | None
    elevation_gain_m: int | None
    average_pace_min_km: float | None
    average_heart_rate: int | None
    max_heart_rate: int | None
    session_type: str | None
    location: str | None
    comments: str | None
    rpe: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateRunningSessionRequest(BaseModel):
    date: date_type
    duration_min: int | None = None
    distance_km: float | None = None
    elevation_gain_m: int | None = None
    average_pace_min_km: float | None = None
    average_heart_rate: int | None = None
    max_heart_rate: int | None = None
    session_type: str | None = None
    location: str | None = None
    comments: str | None = None
    rpe: int | None = None


class UpdateRunningSessionRequest(BaseModel):
    date: date_type | None = None
    duration_min: int | None = None
    distance_km: float | None = None
    elevation_gain_m: int | None = None
    average_pace_min_km: float | None = None
    average_heart_rate: int | None = None
    max_heart_rate: int | None = None
    session_type: str | None = None
    location: str | None = None
    comments: str | None = None
    rpe: int | None = None


# === ROUTES ===

@router.get("", response_model=list[RunningSessionResponse])
def list_running_sessions(
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Liste les séances de course
    """
    query = db.query(RunningSession).filter(RunningSession.user_id == current_user.id)
    
    if date_from:
        query = query.filter(RunningSession.date >= date_from)
    
    if date_to:
        query = query.filter(RunningSession.date <= date_to)
    
    sessions = query.order_by(RunningSession.date.desc()).offset(skip).limit(limit).all()
    return sessions


@router.get("/{session_id}", response_model=RunningSessionResponse)
def get_running_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère une séance de course par son ID
    """
    session = db.query(RunningSession).filter(
        RunningSession.id == session_id,
        RunningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Running session not found"
        )
    
    return session


@router.post("", response_model=RunningSessionResponse, status_code=status.HTTP_201_CREATED)
def create_running_session(
    data: CreateRunningSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle séance de course
    """
    session = RunningSession(
        user_id=current_user.id,
        date=data.date,
        duration_min=data.duration_min,
        distance_km=data.distance_km,
        elevation_gain_m=data.elevation_gain_m,
        average_pace_min_km=data.average_pace_min_km,
        average_heart_rate=data.average_heart_rate,
        max_heart_rate=data.max_heart_rate,
        session_type=data.session_type,
        location=data.location,
        comments=data.comments,
        rpe=data.rpe,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session


@router.put("/{session_id}", response_model=RunningSessionResponse)
def update_running_session(
    session_id: int,
    data: UpdateRunningSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour une séance de course
    """
    session = db.query(RunningSession).filter(
        RunningSession.id == session_id,
        RunningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Running session not found"
        )
    
    # Mettre à jour les champs fournis
    if data.date is not None:
        session.date = data.date
    if data.duration_min is not None:
        session.duration_min = data.duration_min
    if data.distance_km is not None:
        session.distance_km = data.distance_km
    if data.elevation_gain_m is not None:
        session.elevation_gain_m = data.elevation_gain_m
    if data.average_pace_min_km is not None:
        session.average_pace_min_km = data.average_pace_min_km
    if data.average_heart_rate is not None:
        session.average_heart_rate = data.average_heart_rate
    if data.max_heart_rate is not None:
        session.max_heart_rate = data.max_heart_rate
    if data.session_type is not None:
        session.session_type = data.session_type
    if data.location is not None:
        session.location = data.location
    if data.comments is not None:
        session.comments = data.comments
    if data.rpe is not None:
        session.rpe = data.rpe
    
    session.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(session)
    
    return session


@router.delete("/{session_id}")
def delete_running_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime une séance de course
    """
    session = db.query(RunningSession).filter(
        RunningSession.id == session_id,
        RunningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Running session not found"
        )
    
    db.delete(session)
    db.commit()
    
    return {"message": "Running session deleted successfully"}