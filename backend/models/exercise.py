"""
Modèle Exercise - Bibliothèque d'exercices personnalisés
Chaque utilisateur peut créer ses propres exercices
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class ExerciseType(str, enum.Enum):
    """Types d'exercices"""
    SAE = "sae"
    OUTDOOR = "outdoor"
    RUNNING = "running"
    ROUTINE_MORNING = "routine_morning"
    ROUTINE_EVENING = "routine_evening"
    OTHER = "other"


class Exercise(Base):
    """
    Exercice personnalisé créé par l'utilisateur
    Ex: "Bloc Force Max", "Footing Easy", "Gainage Matin"
    """
    __tablename__ = "exercises"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === INFORMATIONS ===
    name = Column(String(200), nullable=False)
    type = Column(Enum(ExerciseType), nullable=False)
    duration_min = Column(Integer)  # Durée estimée en minutes
    description = Column(Text)
    
    # === CARACTÉRISTIQUES ===
    intensity = Column(Integer)  # 1-5 (1=facile, 5=très intense)
    focus = Column(String(200))  # "force,resistance,technique" (CSV)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="exercises")
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    @property
    def focus_list(self) -> list:
        """Retourne la liste des focus"""
        if self.focus:
            return [f.strip() for f in self.focus.split(",")]
        return []