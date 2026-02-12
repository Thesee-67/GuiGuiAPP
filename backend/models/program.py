"""
Modèle Program - Programmes d'entraînement
Bibliothèque de programmes pré-définis ou créés par l'utilisateur
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import json

from backend.database import Base


class Program(Base):
    """
    Programme d'entraînement
    Ex: "Progression force 8 semaines", "Préparation DE"
    """
    __tablename__ = "programs"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === INFORMATIONS ===
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # === DURÉE ===
    duration_weeks = Column(Integer)  # Durée en semaines
    
    # === PROGRAMME ===
    # Structure du programme au format JSON
    # Ex: {"week1": [{"day": "monday", "session_template_id": 5}, ...], "week2": [...]}
    structure_json = Column(Text)
    
    # === STATUT ===
    is_active = Column(Boolean, default=False)  # Programme actuellement suivi
    is_public = Column(Boolean, default=False)  # Partageable avec d'autres utilisateurs
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="programs")
    
    def __repr__(self):
        return f"<Program(id={self.id}, name='{self.name}', weeks={self.duration_weeks})>"
    
    @property
    def structure(self) -> dict:
        """Retourne la structure du programme"""
        if self.structure_json:
            try:
                return json.loads(self.structure_json)
            except:
                return {}
        return {}
    
    @structure.setter
    def structure(self, data: dict):
        """Définit la structure du programme"""
        self.structure_json = json.dumps(data)