"""
Routes de gestion des grandes voies
CRUD sur les voies d'escalade
"""

from datetime import datetime
from datetime import date as date_type
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.models.route import Route, RouteType

router = APIRouter()


# === SCHEMAS ===

class RouteResponse(BaseModel):
    id: int
    user_id: int
    goal_category_id: int | None
    name: str
    location: str
    grade: str
    type: str
    length_m: int | None
    pitch_count: int | None
    date_completed: date_type | None
    style: str | None
    photo_url: str | None
    comments: str | None
    rating: int | None
    validated_for_de: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateRouteRequest(BaseModel):
    goal_category_id: int | None = None
    name: str
    location: str
    grade: str
    type: RouteType
    length_m: int | None = None
    pitch_count: int | None = None
    date_completed: date_type | None = None
    style: str | None = None
    photo_url: str | None = None
    comments: str | None = None
    rating: int | None = None
    validated_for_de: bool = False


class UpdateRouteRequest(BaseModel):
    goal_category_id: int | None = None
    name: str | None = None
    location: str | None = None
    grade: str | None = None
    type: RouteType | None = None
    length_m: int | None = None
    pitch_count: int | None = None
    date_completed: date_type | None = None
    style: str | None = None
    photo_url: str | None = None
    comments: str | None = None
    rating: int | None = None
    validated_for_de: bool | None = None


# === ROUTES ===

@router.get("", response_model=list[RouteResponse])
def list_routes(
    route_type: RouteType | None = None,
    validated_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Liste les grandes voies de l'utilisateur
    """
    query = db.query(Route).filter(Route.user_id == current_user.id)
    
    if route_type:
        query = query.filter(Route.type == route_type)
    
    if validated_only:
        query = query.filter(Route.validated_for_de == True)
    
    routes = query.order_by(Route.date_completed.desc()).offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère une grande voie par son ID
    """
    route = db.query(Route).filter(
        Route.id == route_id,
        Route.user_id == current_user.id
    ).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    return route


@router.post("", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(
    data: CreateRouteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle grande voie
    """
    route = Route(
        user_id=current_user.id,
        goal_category_id=data.goal_category_id,
        name=data.name,
        location=data.location,
        grade=data.grade,
        type=data.type,
        length_m=data.length_m,
        pitch_count=data.pitch_count,
        date_completed=data.date_completed,
        style=data.style,
        photo_url=data.photo_url,
        comments=data.comments,
        rating=data.rating,
        validated_for_de=data.validated_for_de,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(route)
    db.commit()
    db.refresh(route)
    
    return route


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    data: UpdateRouteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour une grande voie
    """
    route = db.query(Route).filter(
        Route.id == route_id,
        Route.user_id == current_user.id
    ).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    # Mettre à jour les champs fournis
    if data.goal_category_id is not None:
        route.goal_category_id = data.goal_category_id
    if data.name is not None:
        route.name = data.name
    if data.location is not None:
        route.location = data.location
    if data.grade is not None:
        route.grade = data.grade
    if data.type is not None:
        route.type = data.type
    if data.length_m is not None:
        route.length_m = data.length_m
    if data.pitch_count is not None:
        route.pitch_count = data.pitch_count
    if data.date_completed is not None:
        route.date_completed = data.date_completed
    if data.style is not None:
        route.style = data.style
    if data.photo_url is not None:
        route.photo_url = data.photo_url
    if data.comments is not None:
        route.comments = data.comments
    if data.rating is not None:
        route.rating = data.rating
    if data.validated_for_de is not None:
        route.validated_for_de = data.validated_for_de
    
    route.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(route)
    
    return route


@router.delete("/{route_id}")
def delete_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime une grande voie
    """
    route = db.query(Route).filter(
        Route.id == route_id,
        Route.user_id == current_user.id
    ).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    db.delete(route)
    db.commit()
    
    return {"message": "Route deleted successfully"}