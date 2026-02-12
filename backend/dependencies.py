"""
Dépendances FastAPI
Utilisées pour l'injection de dépendances dans les routes
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.auth import decode_access_token
from backend.models.user import User, UserRole

# Schema OAuth2 pour récupérer le token dans le header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Récupère l'utilisateur actuellement connecté à partir du token JWT
    
    Args:
        token: Token JWT d'accès
        db: Session de base de données
    
    Returns:
        Utilisateur connecté
    
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Décoder le token
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception
    
    # Récupérer l'utilisateur
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    # Vérifier que le compte est actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Récupère l'utilisateur actif actuellement connecté
    Alias de get_current_user pour plus de clarté
    
    Args:
        current_user: Utilisateur connecté
    
    Returns:
        Utilisateur actif
    """
    return current_user


def get_current_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Récupère l'utilisateur vérifié actuellement connecté
    
    Args:
        current_user: Utilisateur connecté
    
    Returns:
        Utilisateur vérifié
    
    Raises:
        HTTPException: Si l'utilisateur n'est pas vérifié
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    return current_user


def require_role(required_role: UserRole):
    """
    Factory pour créer une dépendance qui vérifie le rôle de l'utilisateur
    
    Args:
        required_role: Rôle requis
    
    Returns:
        Fonction de dépendance
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        """
        Vérifie que l'utilisateur a le rôle requis
        
        Args:
            current_user: Utilisateur connecté
        
        Returns:
            Utilisateur si le rôle correspond
        
        Raises:
            HTTPException: Si le rôle ne correspond pas
        """
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role.value} required"
            )
        return current_user
    
    return role_checker


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur est administrateur
    
    Args:
        current_user: Utilisateur connecté
    
    Returns:
        Utilisateur si admin
    
    Raises:
        HTTPException: Si l'utilisateur n'est pas admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def require_coach(current_user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur est coach ou admin
    
    Args:
        current_user: Utilisateur connecté
    
    Returns:
        Utilisateur si coach ou admin
    
    Raises:
        HTTPException: Si l'utilisateur n'est ni coach ni admin
    """
    if not (current_user.is_coach or current_user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach privileges required"
        )
    return current_user


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Récupère l'utilisateur connecté si un token est fourni
    Ne lève pas d'exception si le token est absent ou invalide
    
    Args:
        token: Token JWT d'accès (optionnel)
        db: Session de base de données
    
    Returns:
        Utilisateur connecté ou None
    """
    if not token:
        return None
    
    try:
        email = decode_access_token(token)
        if email is None:
            return None
        
        user = db.query(User).filter(User.email == email).first()
        return user if user and user.is_active else None
    except:
        return None