"""
Modèle RunningSession - Séances de course à pied
Suivi des sorties running avec distance, dénivelé, allure, FC
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class RunningSession(Base):
    """
    Séance de course à pied
    Données : distance, dénivelé, allure, fréquence cardiaque
    """
    __tablename__ = "running_sessions"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === DATE & DURÉE ===
    date = Column(Date, nullable=False, index=True)
    duration_min = Column(Integer)  # Durée en minutes
    
    # === PERFORMANCE ===
    distance_km = Column(Float)  # Distance en km
    elevation_gain_m = Column(Integer)  # Dénivelé positif en mètres
    average_pace_min_km = Column(Float)  # Allure moyenne en min/km
    
    # === FRÉQUENCE CARDIAQUE ===
    average_heart_rate = Column(Integer)  # FC moyenne en bpm
    max_heart_rate = Column(Integer)  # FC max en bpm
    
    # === TYPE & LIEU ===
    session_type = Column(String(50))  # footing, fractionné, sortie longue, etc.
    location = Column(String(200))  # Lieu de la sortie
    
    # === NOTES ===
    comments = Column(Text)
    
    # === RESSENTI ===
    rpe = Column(Integer)  # Rate of Perceived Exertion (1-10)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="running_sessions")
    
    def __repr__(self):
        return f"<RunningSession(id={self.id}, date={self.date}, distance={self.distance_km}km)>"
    
    @property
    def average_speed_kmh(self) -> float:
        """Calcule la vitesse moyenne en km/h"""
        if self.average_pace_min_km and self.average_pace_min_km > 0:
            return 60 / self.average_pace_min_km
        return 0