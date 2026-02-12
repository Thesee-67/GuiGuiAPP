"""
Routes de gestion des exercices
CRUD sur les exercices personnalisés
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.exercise import Exercise, ExerciseType

router = APIRouter()


# === SCHEMAS ===

class ExerciseResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    duration_min: int | None
    description: str | None
    intensity: int | None
    focus: str | None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreateExerciseRequest(BaseModel):
    name: str
    type: ExerciseType
    duration_min: int | None = None
    description: str | None = None
    intensity: int | None = None
    focus: str | None = None


class UpdateExerciseRequest(BaseModel):
    name: str | None = None
    type: ExerciseType | None = None
    duration_min: int | None = None
    description: str | None = None
    intensity: int | None = None
    focus: str | None = None


# === ROUTES ===

@router.get("", response_model=list[ExerciseResponse])
def list_exercises(
    exercise_type: ExerciseType | None = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Liste les exercices de l'utilisateur connecté
    """
    query = db.query(Exercise).filter(Exercise.user_id == current_user.id)
    
    if exercise_type:
        query = query.filter(Exercise.type == exercise_type)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère un exercice par son ID
    """
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    return exercise


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(
    data: CreateExerciseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel exercice
    """
    exercise = Exercise(
        user_id=current_user.id,
        name=data.name,
        type=data.type,
        duration_min=data.duration_min,
        description=data.description,
        intensity=data.intensity,
        focus=data.focus,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    data: UpdateExerciseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour un exercice
    """
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Mettre à jour les champs fournis
    if data.name is not None:
        exercise.name = data.name
    
    if data.type is not None:
        exercise.type = data.type
    
    if data.duration_min is not None:
        exercise.duration_min = data.duration_min
    
    if data.description is not None:
        exercise.description = data.description
    
    if data.intensity is not None:
        exercise.intensity = data.intensity
    
    if data.focus is not None:
        exercise.focus = data.focus
    
    exercise.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(exercise)
    
    return exercise


@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un exercice
    """
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    db.delete(exercise)
    db.commit()
    
    return {"message": "Exercise deleted successfully"}