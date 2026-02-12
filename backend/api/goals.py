"""
Routes de gestion des objectifs DE
Catégories d'objectifs et progression
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.goal_category import GoalCategory

router = APIRouter()


# === SCHEMAS ===

class GoalCategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    required_count: int
    criteria_json: str | None
    order: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GoalCategoryWithProgressResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    required_count: int
    criteria_json: str | None
    order: int | None
    created_at: datetime
    progress: dict
    
    class Config:
        from_attributes = True


class CreateGoalCategoryRequest(BaseModel):
    name: str
    description: str | None = None
    required_count: int
    criteria: dict = {}
    order: int | None = None


class UpdateGoalCategoryRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    required_count: int | None = None
    criteria: dict | None = None
    order: int | None = None


# === ROUTES ===

@router.get("", response_model=list[GoalCategoryWithProgressResponse])
def list_goal_categories(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Liste les catégories d'objectifs avec progression
    """
    categories = db.query(GoalCategory).filter(
        GoalCategory.user_id == current_user.id
    ).order_by(GoalCategory.order).offset(skip).limit(limit).all()
    
    # Ajouter la progression pour chaque catégorie
    result = []
    for category in categories:
        cat_dict = {
            "id": category.id,
            "user_id": category.user_id,
            "name": category.name,
            "description": category.description,
            "required_count": category.required_count,
            "criteria_json": category.criteria_json,
            "order": category.order,
            "created_at": category.created_at,
            "progress": category.progress
        }
        result.append(cat_dict)
    
    return result


@router.get("/{category_id}", response_model=GoalCategoryWithProgressResponse)
def get_goal_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère une catégorie d'objectif par son ID
    """
    category = db.query(GoalCategory).filter(
        GoalCategory.id == category_id,
        GoalCategory.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal category not found"
        )
    
    return {
        "id": category.id,
        "user_id": category.user_id,
        "name": category.name,
        "description": category.description,
        "required_count": category.required_count,
        "criteria_json": category.criteria_json,
        "order": category.order,
        "created_at": category.created_at,
        "progress": category.progress
    }


@router.post("", response_model=GoalCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_goal_category(
    data: CreateGoalCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle catégorie d'objectif
    """
    category = GoalCategory(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        required_count=data.required_count,
        order=data.order or 1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Utiliser le setter pour convertir le dict en JSON
    category.criteria = data.criteria
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category


@router.put("/{category_id}", response_model=GoalCategoryResponse)
def update_goal_category(
    category_id: int,
    data: UpdateGoalCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour une catégorie d'objectif
    """
    category = db.query(GoalCategory).filter(
        GoalCategory.id == category_id,
        GoalCategory.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal category not found"
        )
    
    # Mettre à jour les champs fournis
    if data.name is not None:
        category.name = data.name
    
    if data.description is not None:
        category.description = data.description
    
    if data.required_count is not None:
        category.required_count = data.required_count
    
    if data.criteria is not None:
        category.criteria = data.criteria
    
    if data.order is not None:
        category.order = data.order
    
    category.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}")
def delete_goal_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime une catégorie d'objectif
    """
    category = db.query(GoalCategory).filter(
        GoalCategory.id == category_id,
        GoalCategory.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Goal category deleted successfully"}