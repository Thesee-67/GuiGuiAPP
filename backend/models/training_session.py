"""
Modèle TrainingSession - Séances d'entraînement réalisées
Historique complet avec détails (cotations, essais, RPE, etc.)
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class ClimbingStyle(str, enum.Enum):
    """Styles de grimpe"""
    ONSIGHT = "onsight"
    FLASH = "flash"
    REDPOINT = "redpoint"
    PROJECT = "project"


class TrainingSession(Base):
    """
    Séance d'entraînement réalisée (SAE ou outdoor)
    Avec détails : cotations, essais, RPE, fatigue, etc.
    """
    __tablename__ = "training_sessions"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    planning_id = Column(Integer, ForeignKey("planning.id", ondelete="SET NULL"))
    
    # === DATE & DURÉE ===
    date = Column(Date, nullable=False, index=True)
    duration_min = Column(Integer)
    
    # === TYPE DE SÉANCE ===
    session_type = Column(String(50))  # force, resistance, continuity, etc.
    location = Column(String(200))  # Nom de la salle ou du site
    
    # === PERFORMANCE ===
    # Voies/blocs grimpés au format JSON
    # Ex: [{"grade": "7a", "style": "onsight", "tries": 1}, ...]
    routes_json = Column(Text)
    
    # Meilleure performance de la séance
    best_grade = Column(String(10))
    best_style = Column(Enum(ClimbingStyle))
    
    # === RESSENTI ===
    rpe = Column(Integer)  # Rate of Perceived Exertion (1-10)
    fatigue = Column(Integer)  # Niveau de fatigue (1-10)
    
    # === NOTES ===
    notes = Column(Text)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="training_sessions")
    
    def __repr__(self):
        return f"<TrainingSession(id={self.id}, date={self.date}, type='{self.session_type}')>"