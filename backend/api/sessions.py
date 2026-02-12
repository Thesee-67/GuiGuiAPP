"""
Routes de gestion des séances
Templates, planning, training sessions
"""

from datetime import datetime
from datetime import date as date_type
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.session_template import SessionTemplate, SessionType
from backend.models.planning import Planning, ActivityType, TimeSlot
from backend.models.training_session import TrainingSession, ClimbingStyle

router = APIRouter()


# === SCHEMAS - SESSION TEMPLATES ===

class SessionTemplateResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    duration_min: int | None
    description: str | None
    exercises_json: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateSessionTemplateRequest(BaseModel):
    name: str
    type: SessionType
    duration_min: int | None = None
    description: str | None = None
    exercise_ids: list[int] = []


class UpdateSessionTemplateRequest(BaseModel):
    name: str | None = None
    type: SessionType | None = None
    duration_min: int | None = None
    description: str | None = None
    exercise_ids: list[int] | None = None


# === SCHEMAS - PLANNING ===

class PlanningResponse(BaseModel):
    id: int
    user_id: int
    date: date_type
    time_slot: str
    activity_type: str
    activity_id: int | None
    title: str | None
    description: str | None
    completed: bool
    completed_at: datetime | None
    notes: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreatePlanningRequest(BaseModel):
    date: date_type
    time_slot: TimeSlot
    activity_type: ActivityType
    activity_id: int | None = None
    title: str | None = None
    description: str | None = None


class UpdatePlanningRequest(BaseModel):
    date: date_type | None = None
    time_slot: TimeSlot | None = None
    activity_type: ActivityType | None = None
    activity_id: int | None = None
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    notes: str | None = None


# === SCHEMAS - TRAINING SESSIONS ===

class TrainingSessionResponse(BaseModel):
    id: int
    user_id: int
    planning_id: int | None
    date: date_type
    duration_min: int | None
    session_type: str | None
    location: str | None
    routes_json: str | None
    best_grade: str | None
    best_style: str | None
    rpe: int | None
    fatigue: int | None
    notes: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateTrainingSessionRequest(BaseModel):
    planning_id: int | None = None
    date: date_type
    duration_min: int | None = None
    session_type: str | None = None
    location: str | None = None
    routes_json: str | None = None
    best_grade: str | None = None
    best_style: ClimbingStyle | None = None
    rpe: int | None = None
    fatigue: int | None = None
    notes: str | None = None


# === ROUTES - SESSION TEMPLATES ===

@router.get("/templates", response_model=list[SessionTemplateResponse])
def list_session_templates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liste les templates de séances"""
    templates = db.query(SessionTemplate).filter(
        SessionTemplate.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return templates


@router.post("/templates", response_model=SessionTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_session_template(
    data: CreateSessionTemplateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crée un nouveau template de séance"""
    template = SessionTemplate(
        user_id=current_user.id,
        name=data.name,
        type=data.type,
        duration_min=data.duration_min,
        description=data.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Utiliser le setter pour convertir la liste en JSON
    template.exercise_ids = data.exercise_ids
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}")
def delete_session_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime un template de séance"""
    template = db.query(SessionTemplate).filter(
        SessionTemplate.id == template_id,
        SessionTemplate.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}


# === ROUTES - PLANNING ===

@router.get("/planning", response_model=list[PlanningResponse])
def list_planning(
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liste les activités planifiées"""
    query = db.query(Planning).filter(Planning.user_id == current_user.id)
    
    if date_from:
        query = query.filter(Planning.date >= date_from)
    
    if date_to:
        query = query.filter(Planning.date <= date_to)
    
    planning = query.order_by(Planning.date).offset(skip).limit(limit).all()
    return planning


@router.post("/planning", response_model=PlanningResponse, status_code=status.HTTP_201_CREATED)
def create_planning(
    data: CreatePlanningRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crée une nouvelle activité planifiée"""
    planning = Planning(
        user_id=current_user.id,
        date=data.date,
        time_slot=data.time_slot,
        activity_type=data.activity_type,
        activity_id=data.activity_id,
        title=data.title,
        description=data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(planning)
    db.commit()
    db.refresh(planning)
    
    return planning


@router.put("/planning/{planning_id}", response_model=PlanningResponse)
def update_planning(
    planning_id: int,
    data: UpdatePlanningRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Met à jour une activité planifiée"""
    planning = db.query(Planning).filter(
        Planning.id == planning_id,
        Planning.user_id == current_user.id
    ).first()
    
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planning not found"
        )
    
    # Mettre à jour les champs
    if data.date is not None:
        planning.date = data.date
    if data.time_slot is not None:
        planning.time_slot = data.time_slot
    if data.activity_type is not None:
        planning.activity_type = data.activity_type
    if data.activity_id is not None:
        planning.activity_id = data.activity_id
    if data.title is not None:
        planning.title = data.title
    if data.description is not None:
        planning.description = data.description
    if data.completed is not None:
        planning.completed = data.completed
        if data.completed and not planning.completed_at:
            planning.completed_at = datetime.utcnow()
    if data.notes is not None:
        planning.notes = data.notes
    
    planning.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(planning)
    
    return planning


@router.delete("/planning/{planning_id}")
def delete_planning(
    planning_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime une activité planifiée"""
    planning = db.query(Planning).filter(
        Planning.id == planning_id,
        Planning.user_id == current_user.id
    ).first()
    
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planning not found"
        )
    
    db.delete(planning)
    db.commit()
    
    return {"message": "Planning deleted successfully"}


# === ROUTES - TRAINING SESSIONS ===

@router.get("/training", response_model=list[TrainingSessionResponse])
def list_training_sessions(
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liste les séances d'entraînement réalisées"""
    query = db.query(TrainingSession).filter(TrainingSession.user_id == current_user.id)
    
    if date_from:
        query = query.filter(TrainingSession.date >= date_from)
    
    if date_to:
        query = query.filter(TrainingSession.date <= date_to)
    
    sessions = query.order_by(TrainingSession.date.desc()).offset(skip).limit(limit).all()
    return sessions


@router.post("/training", response_model=TrainingSessionResponse, status_code=status.HTTP_201_CREATED)
def create_training_session(
    data: CreateTrainingSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crée une nouvelle séance d'entraînement"""
    session = TrainingSession(
        user_id=current_user.id,
        planning_id=data.planning_id,
        date=data.date,
        duration_min=data.duration_min,
        session_type=data.session_type,
        location=data.location,
        routes_json=data.routes_json,
        best_grade=data.best_grade,
        best_style=data.best_style,
        rpe=data.rpe,
        fatigue=data.fatigue,
        notes=data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session


@router.delete("/training/{session_id}")
def delete_training_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime une séance d'entraînement"""
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training session not found"
        )
    
    db.delete(session)
    db.commit()
    
    return {"message": "Training session deleted successfully"}