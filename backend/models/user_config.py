"""
Modèle UserConfig - Configuration personnalisée de chaque utilisateur
Règles de planning, objectifs, préférences
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class UserConfig(Base):
    """
    Configuration personnalisée de l'utilisateur
    Règles pour la génération automatique du planning
    """
    __tablename__ = "user_configs"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # === PLANNING AUTOMATIQUE ===
    # Séances SAE
    sae_per_week = Column(Integer, default=4, nullable=False)
    
    # Sorties outdoor
    outdoor_per_week_min = Column(Integer, default=1, nullable=False)
    outdoor_per_week_max = Column(Integer, default=2, nullable=False)
    
    # Repos
    rest_days = Column(Integer, default=3, nullable=False)  # Nombre de jours de repos
    rest_frequency_weeks = Column(Integer, default=3, nullable=False)  # Tous les X semaines
    
    # Course à pied
    morning_run_enabled = Column(Boolean, default=True, nullable=False)
    
    # === OBJECTIFS ===
    target_date = Column(Date)  # Date objectif (ex: examen DE)
    target_level = Column(String(10))  # Niveau cible (ex: "7a", "8a")
    
    # === PRÉFÉRENCES CRÉNEAUX ===
    # JSON : {"monday": {"afternoon": true, "evening": false}, ...}
    available_slots_json = Column(String(1000))
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="config")
    
    def __repr__(self):
        return f"<UserConfig(user_id={self.user_id}, sae={self.sae_per_week}/week)>"