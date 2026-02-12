"""
Modèle GoalCategory - Catégories d'objectifs DE
Ex: "ED- Équipé 200m", "TD+ Trad 200m"
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import json

from backend.database import Base


class GoalCategory(Base):
    """
    Catégorie d'objectif pour le DE
    Ex: 8 voies ED- de 200m en équipé
    """
    __tablename__ = "goal_categories"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === INFORMATIONS ===
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # === OBJECTIF ===
    required_count = Column(Integer, nullable=False)  # Nombre de voies requises
    
    # === CRITÈRES ===
    # Critères au format JSON
    # Ex: {"min_grade": "7a", "min_length": 200, "route_type": "sport"}
    criteria_json = Column(String(1000))
    
    # === AFFICHAGE ===
    order = Column(Integer, default=1)  # Ordre d'affichage
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATIONS ===
    user = relationship("User", back_populates="goal_categories")
    routes = relationship("Route", back_populates="goal_category")
    
    def __repr__(self):
        return f"<GoalCategory(id={self.id}, name='{self.name}', required={self.required_count})>"
    
    @property
    def criteria(self) -> dict:
        """Retourne les critères en dict"""
        if self.criteria_json:
            try:
                return json.loads(self.criteria_json)
            except:
                return {}
        return {}
    
    @criteria.setter
    def criteria(self, data: dict):
        """Définit les critères"""
        self.criteria_json = json.dumps(data)
    
    @property
    def progress(self) -> dict:
        """Calcule la progression"""
        completed = len([r for r in self.routes if r.validated_for_de])
        return {
            "completed": completed,
            "required": self.required_count,
            "percentage": int((completed / self.required_count) * 100) if self.required_count > 0 else 0
        }