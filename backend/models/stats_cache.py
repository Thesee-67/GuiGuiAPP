"""
Modèle StatsCache - Cache des statistiques
Évite de recalculer les stats à chaque fois
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class StatsCache(Base):
    """
    Cache des statistiques calculées
    Pour améliorer les performances
    """
    __tablename__ = "stats_cache"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === TYPE DE STAT ===
    stat_type = Column(String(50), nullable=False, index=True)
    # Ex: "monthly_volume", "progression_chart", "best_performances"
    
    # === PÉRIODE ===
    period_start = Column(Date)
    period_end = Column(Date)
    
    # === DONNÉES ===
    # Statistiques au format JSON
    data_json = Column(Text, nullable=False)
    
    # === CACHE ===
    expires_at = Column(DateTime)  # Date d'expiration du cache
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="stats_cache")
    
    def __repr__(self):
        return f"<StatsCache(id={self.id}, type='{self.stat_type}', user_id={self.user_id})>"
    
    def is_expired(self) -> bool:
        """Vérifie si le cache est expiré"""
        if not self.expires_at:
            return True
        return datetime.utcnow() > self.expires_at