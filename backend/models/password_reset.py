"""
Modèle PasswordResetToken - Tokens de réinitialisation de mot de passe
Gestion sécurisée des demandes de reset password
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets

from backend.database import Base


class PasswordResetToken(Base):
    """
    Token de réinitialisation de mot de passe
    Expire après X heures pour la sécurité
    """
    __tablename__ = "password_reset_tokens"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === TOKEN ===
    token = Column(String(255), unique=True, nullable=False, index=True)
    
    # === STATUT ===
    used = Column(Boolean, default=False, nullable=False)
    used_at = Column(DateTime)
    
    # === EXPIRATION ===
    expires_at = Column(DateTime, nullable=False)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="password_reset_tokens")
    
    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, user_id={self.user_id}, used={self.used})>"
    
    @staticmethod
    def generate_token() -> str:
        """Génère un token sécurisé"""
        return secrets.token_urlsafe(32)
    
    def is_expired(self) -> bool:
        """Vérifie si le token est expiré"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Vérifie si le token est valide (non utilisé et non expiré)"""
        return not self.used and not self.is_expired()
    
    def mark_as_used(self):
        """Marque le token comme utilisé"""
        self.used = True
        self.used_at = datetime.utcnow()