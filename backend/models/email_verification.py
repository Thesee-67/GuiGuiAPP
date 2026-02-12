"""
Modèle EmailVerificationToken - Tokens de vérification d'email
Gestion sécurisée de la vérification des comptes
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets

from backend.database import Base


class EmailVerificationToken(Base):
    """
    Token de vérification d'email
    Envoyé lors de l'inscription pour vérifier l'adresse email
    """
    __tablename__ = "email_verification_tokens"
    
    # === CLÉS ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # === TOKEN ===
    token = Column(String(255), unique=True, nullable=False, index=True)
    
    # === STATUT ===
    verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime)
    
    # === EXPIRATION ===
    expires_at = Column(DateTime, nullable=False)
    
    # === DATES ===
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # === RELATION ===
    user = relationship("User", back_populates="email_verification_tokens")
    
    def __repr__(self):
        return f"<EmailVerificationToken(id={self.id}, user_id={self.user_id}, verified={self.verified})>"
    
    @staticmethod
    def generate_token() -> str:
        """Génère un token sécurisé"""
        return secrets.token_urlsafe(32)
    
    def is_expired(self) -> bool:
        """Vérifie si le token est expiré"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Vérifie si le token est valide (non vérifié et non expiré)"""
        return not self.verified and not self.is_expired()
    
    def mark_as_verified(self):
        """Marque le token comme vérifié"""
        self.verified = True
        self.verified_at = datetime.utcnow()