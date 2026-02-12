"""
Modèle Planning - Planning d'entraînement
Séances planifiées (futures ou passées)
"""

from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class ActivityType(str, enum.Enum):
    """Types d'activités dans le planning"""
    SAE = "sae"
    OUTDOOR = "outdoor"
    RUNNING = "running"
    ROUTINE_MORNING = "routine_morning"
    ROUTINE_EVENING = "routine_evening"
    REST = "rest"
    OTHER = "other"


class TimeSlot(str, enum.Enum):
    """Créneaux horaires"""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"


class Planning(Base):
    """
    Activité planifiée dans le planning
    Générée automatiquement ou ajoutée manuellement
    """
    __tablename__ = "planning"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === DATE & HEURE ===
    date = Column(Date, nullable=False, index=True)
    time_slot = Column(Enum(TimeSlot), nullable=False)
    time_start = Column(Time)
    
    # === ACTIVITÉ ===
    activity_type = Column(Enum(ActivityType), nullable=False)
    activity_id = Column(Integer)  # ID de l'exercice ou du template
    title = Column(String(200))
    description = Column(Text)
    
    # === STATUT ===
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime)
    
    # === NOTES ===
    notes = Column(Text)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="planning")
    
    def __repr__(self):
        return f"<Planning(id={self.id}, date={self.date}, activity='{self.activity_type}')>"
    
    def mark_as_completed(self):
        """Marque l'activité comme complétée"""
        self.completed = True
        self.completed_at = datetime.utcnow()