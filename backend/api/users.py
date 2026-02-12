"""
Routes de gestion des utilisateurs
Profil, configuration, mise à jour
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from backend.database import get_db
from backend.dependencies import get_current_user, require_admin
from backend.auth import get_password_hash, verify_password, validate_password_strength
from backend.models.user import User
from backend.models.user_config import UserConfig

router = APIRouter()


# === SCHEMAS ===

class UserProfileResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    avatar_url: str | None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: datetime | None
    
    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserConfigResponse(BaseModel):
    id: int
    user_id: int
    sae_per_week: int
    outdoor_per_week_min: int
    outdoor_per_week_max: int
    rest_days: int
    rest_frequency_weeks: int
    morning_run_enabled: bool
    target_level: str | None
    target_date: str | None
    
    class Config:
        from_attributes = True


class UpdateConfigRequest(BaseModel):
    sae_per_week: int | None = None
    outdoor_per_week_min: int | None = None
    outdoor_per_week_max: int | None = None
    rest_days: int | None = None
    rest_frequency_weeks: int | None = None
    morning_run_enabled: bool | None = None
    target_level: str | None = None
    target_date: str | None = None


# === ROUTES ===

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Récupère le profil de l'utilisateur connecté
    """
    return current_user


@router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour le profil de l'utilisateur
    """
    if data.first_name is not None:
        current_user.first_name = data.first_name
    
    if data.last_name is not None:
        current_user.last_name = data.last_name
    
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url
    
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change le mot de passe de l'utilisateur
    """
    # Vérifier le mot de passe actuel
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Valider le nouveau mot de passe
    is_valid, error_msg = validate_password_strength(data.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Mettre à jour le mot de passe
    current_user.password_hash = get_password_hash(data.new_password)
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Password updated successfully"}


@router.get("/config", response_model=UserConfigResponse)
def get_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la configuration de l'utilisateur
    """
    config = db.query(UserConfig).filter(UserConfig.user_id == current_user.id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return config


@router.put("/config", response_model=UserConfigResponse)
def update_config(
    data: UpdateConfigRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour la configuration de l'utilisateur
    """
    config = db.query(UserConfig).filter(UserConfig.user_id == current_user.id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    # Mettre à jour les champs fournis
    if data.sae_per_week is not None:
        config.sae_per_week = data.sae_per_week
    
    if data.outdoor_per_week_min is not None:
        config.outdoor_per_week_min = data.outdoor_per_week_min
    
    if data.outdoor_per_week_max is not None:
        config.outdoor_per_week_max = data.outdoor_per_week_max
    
    if data.rest_days is not None:
        config.rest_days = data.rest_days
    
    if data.rest_frequency_weeks is not None:
        config.rest_frequency_weeks = data.rest_frequency_weeks
    
    if data.morning_run_enabled is not None:
        config.morning_run_enabled = data.morning_run_enabled
    
    if data.target_level is not None:
        config.target_level = data.target_level
    
    if data.target_date is not None:
        config.target_date = data.target_date
    
    config.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(config)
    
    return config


@router.delete("/account")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime le compte de l'utilisateur
    """
    db.delete(current_user)
    db.commit()
    
    return {"message": "Account deleted successfully"}


# === ADMIN ROUTES ===

@router.get("/list", dependencies=[Depends(require_admin)])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Liste tous les utilisateurs (admin uniquement)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un utilisateur (admin uniquement)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}