"""
Modèle SessionTemplate - Templates de séances réutilisables
Ex: "Force Max", "Résistance 4x4", "Continuité"
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import json

from backend.database import Base


class SessionType(str, enum.Enum):
    """Types de séances"""
    FORCE = "force"
    RESISTANCE = "resistance"
    CONTINUITY = "continuity"
    ONSIGHT = "onsight"
    PROJECT = "project"
    MIXED = "mixed"


class SessionTemplate(Base):
    """
    Template de séance réutilisable
    Contient une liste d'exercices et leur ordre
    """
    __tablename__ = "session_templates"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === INFORMATIONS ===
    name = Column(String(200), nullable=False)
    type = Column(Enum(SessionType), nullable=False)
    duration_min = Column(Integer)
    description = Column(Text)
    
    # === EXERCICES ===
    # Liste des IDs d'exercices au format JSON
    # Ex: [1, 5, 12, 3] pour l'ordre des exercices
    exercises_json = Column(String(1000))
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="session_templates")
    
    def __repr__(self):
        return f"<SessionTemplate(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    @property
    def exercise_ids(self) -> list:
        """Retourne la liste des IDs d'exercices"""
        if self.exercises_json:
            try:
                return json.loads(self.exercises_json)
            except:
                return []
        return []
    
    @exercise_ids.setter
    def exercise_ids(self, ids: list):
        """Définit la liste des IDs d'exercices"""
        self.exercises_json = json.dumps(ids)