"""
Modèle Route - Grandes voies
Pour le suivi des objectifs DE (Diplôme d'État)
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class RouteType(str, enum.Enum):
    """Types de voies"""
    SPORT = "sport"  # Équipé
    TRAD = "trad"    # Terrain d'aventure
    MIXED = "mixed"  # Mixte


class Route(Base):
    """
    Grande voie d'escalade
    Avec photos, commentaires, et lien aux objectifs DE
    """
    __tablename__ = "routes"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_category_id = Column(Integer, ForeignKey("goal_categories.id", ondelete="SET NULL"))
    
    # === INFORMATIONS ===
    name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    
    # === CARACTÉRISTIQUES ===
    grade = Column(String(10), nullable=False)  # Ex: "7a", "ED-"
    type = Column(Enum(RouteType), nullable=False)
    length_m = Column(Integer)  # Longueur en mètres
    pitch_count = Column(Integer)  # Nombre de longueurs
    
    # === RÉALISATION ===
    date_completed = Column(Date, index=True)
    style = Column(String(50))  # onsight, flash, redpoint, etc.
    
    # === MÉDIA ===
    photo_url = Column(String(500))  # Chemin vers la photo
    
    # === NOTES ===
    comments = Column(Text)
    rating = Column(Integer)  # Note personnelle (1-5 étoiles)
    
    # === VALIDATION DE ===
    validated_for_de = Column(Integer, default=False)  # Validée pour le DE
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATIONS ===
    user = relationship("User", back_populates="routes")
    goal_category = relationship("GoalCategory", back_populates="routes")
    
    def __repr__(self):
        return f"<Route(id={self.id}, name='{self.name}', grade='{self.grade}', length={self.length_m}m)>"