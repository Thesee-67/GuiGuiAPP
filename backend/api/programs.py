"""
Routes de gestion des programmes d'entraînement
CRUD sur les programmes
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.program import Program

router = APIRouter()


# === SCHEMAS ===

class ProgramResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    duration_weeks: int | None
    structure_json: str | None
    is_active: bool | None
    is_public: bool | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateProgramRequest(BaseModel):
    name: str
    description: str | None = None
    duration_weeks: int | None = None
    structure: dict = {}
    is_active: bool = False
    is_public: bool = False


class UpdateProgramRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_weeks: int | None = None
    structure: dict | None = None
    is_active: bool | None = None
    is_public: bool | None = None


# === ROUTES ===

@router.get("", response_model=list[ProgramResponse])
def list_programs(
    active_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Liste les programmes d'entraînement
    """
    query = db.query(Program).filter(Program.user_id == current_user.id)
    
    if active_only:
        query = query.filter(Program.is_active == True)
    
    programs = query.offset(skip).limit(limit).all()
    return programs


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère un programme par son ID
    """
    program = db.query(Program).filter(
        Program.id == program_id,
        Program.user_id == current_user.id
    ).first()
    
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    return program


@router.post("", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
def create_program(
    data: CreateProgramRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée un nouveau programme d'entraînement
    """
    program = Program(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        duration_weeks=data.duration_weeks,
        is_active=data.is_active,
        is_public=data.is_public,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Utiliser le setter pour convertir le dict en JSON
    program.structure = data.structure
    
    db.add(program)
    db.commit()
    db.refresh(program)
    
    return program


@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    data: UpdateProgramRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour un programme d'entraînement
    """
    program = db.query(Program).filter(
        Program.id == program_id,
        Program.user_id == current_user.id
    ).first()
    
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    # Mettre à jour les champs fournis
    if data.name is not None:
        program.name = data.name
    
    if data.description is not None:
        program.description = data.description
    
    if data.duration_weeks is not None:
        program.duration_weeks = data.duration_weeks
    
    if data.structure is not None:
        program.structure = data.structure
    
    if data.is_active is not None:
        program.is_active = data.is_active
    
    if data.is_public is not None:
        program.is_public = data.is_public
    
    program.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(program)
    
    return program


@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un programme d'entraînement
    """
    program = db.query(Program).filter(
        Program.id == program_id,
        Program.user_id == current_user.id
    ).first()
    
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    db.delete(program)
    db.commit()
    
    return {"message": "Program deleted successfully"}


@router.post("/{program_id}/activate")
def activate_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Active un programme (désactive tous les autres)
    """
    # Désactiver tous les programmes de l'utilisateur
    db.query(Program).filter(Program.user_id == current_user.id).update({"is_active": False})
    
    # Activer le programme sélectionné
    program = db.query(Program).filter(
        Program.id == program_id,
        Program.user_id == current_user.id
    ).first()
    
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    program.is_active = True
    program.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Program activated successfully"}