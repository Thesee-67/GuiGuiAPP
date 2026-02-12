"""
Modèle User - Utilisateurs de l'application
Table principale pour l'authentification et les données utilisateur
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class UserRole(str, enum.Enum):
    """Rôles utilisateurs"""
    USER = "user"
    COACH = "coach"
    ADMIN = "admin"


class User(Base):
    """
    Table des utilisateurs
    Chaque utilisateur a ses propres données isolées
    """
    __tablename__ = "users"
    
    # === IDENTITÉ ===
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # === INFORMATIONS PERSONNELLES ===
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    
    # === STATUT ===
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime)
    
    # === RELATIONS ===
    # Configuration
    config = relationship("UserConfig", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Entraînement
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")
    session_templates = relationship("SessionTemplate", back_populates="user", cascade="all, delete-orphan")
    planning = relationship("Planning", back_populates="user", cascade="all, delete-orphan")
    training_sessions = relationship("TrainingSession", back_populates="user", cascade="all, delete-orphan")
    
    # Grandes voies
    routes = relationship("Route", back_populates="user", cascade="all, delete-orphan")
    goal_categories = relationship("GoalCategory", back_populates="user", cascade="all, delete-orphan")
    
    # Course à pied
    running_sessions = relationship("RunningSession", back_populates="user", cascade="all, delete-orphan")
    
    # Programmes
    programs = relationship("Program", back_populates="user", cascade="all, delete-orphan")
    
    # Stats
    stats_cache = relationship("StatsCache", back_populates="user", cascade="all, delete-orphan")
    
    # Tokens
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    email_verification_tokens = relationship("EmailVerificationToken", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Retourne le nom complet"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur est admin"""
        return self.role == UserRole.ADMIN
    
    @property
    def is_coach(self) -> bool:
        """Vérifie si l'utilisateur est coach"""
        return self.role == UserRole.COACH