"""
Configuration de l'application
Charge les variables d'environnement depuis .env
"""

import os
from pathlib import Path
from typing import Optional

# Support Pydantic v1 et v2
try:
    from pydantic_settings import BaseSettings  # Pydantic v2
except ImportError:
    from pydantic import BaseSettings  # Pydantic v1 (fallback)

from pydantic import EmailStr, validator


class Settings(BaseSettings):
    """Configuration globale de l'application"""
    
    # === APPLICATION ===
    APP_NAME: str = "Training Escalade"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    APP_URL: str = "https://training.climbingthenet.fr"
    
    # === SÉCURITÉ ===
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # === BASE DE DONNÉES ===
    DATABASE_TYPE: str = "mysql"  # mysql ou sqlite
    
    # MySQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "training_escalade"
    DB_USER: str = "training_user"
    DB_PASSWORD: str
    
    # SQLite (fallback)
    SQLITE_PATH: str = "database/training.db"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construit l'URL de connexion à la base"""
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        else:
            return f"sqlite:///{self.SQLITE_PATH}"
    
    # === EMAIL SERVICE ===
    SMTP_ENABLED: bool = True
    SMTP_HOST: str = "mail.climbingthenet.fr"
    SMTP_PORT: int = 465
    SMTP_USE_TLS: bool = True
    SMTP_USERNAME: str = "noreply@climbingthenet.fr"
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: EmailStr = "noreply@climbingthenet.fr"
    SMTP_FROM_NAME: str = "Training Escalade"
    
    # === VÉRIFICATION EMAIL ===
    EMAIL_VERIFICATION_REQUIRED: bool = True
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    
    # === RESET PASSWORD ===
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 2
    
    # === UPLOADS ===
    UPLOAD_DIR: str = "public_html/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_EXTENSIONS: str = "jpg,jpeg,png,webp"
    
    @property
    def MAX_UPLOAD_SIZE_BYTES(self) -> int:
        """Taille max upload en bytes"""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    @property
    def ALLOWED_EXTENSIONS_LIST(self) -> list:
        """Parse les extensions autorisées en liste"""
        return [ext.strip() for ext in self.ALLOWED_IMAGE_EXTENSIONS.split(",")]
    
    # === RATE LIMITING ===
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # === BACKUP ===
    BACKUP_ENABLED: bool = True
    BACKUP_RETENTION_DAYS: int = 30
    
    # === LOGS ===
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # === PREMIER ADMIN (optionnel) ===
    FIRST_ADMIN_EMAIL: Optional[EmailStr] = None
    FIRST_ADMIN_USERNAME: Optional[str] = None
    FIRST_ADMIN_PASSWORD: Optional[str] = None
    
    # === CORS (pour dev) ===
    CORS_ORIGINS: list = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins depuis string ou list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # === PAGINATION ===
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instance globale des settings
settings = Settings()


# === CHEMINS UTILES ===
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR_PATH = BASE_DIR / settings.UPLOAD_DIR
LOG_DIR_PATH = BASE_DIR / "logs"
BACKUP_DIR_PATH = BASE_DIR / "backups"


def get_upload_path(user_id: int, upload_type: str = "routes") -> Path:
    """
    Retourne le chemin d'upload pour un utilisateur
    
    Args:
        user_id: ID de l'utilisateur
        upload_type: Type d'upload (routes, avatars)
    
    Returns:
        Path vers le dossier d'upload
    """
    path = UPLOAD_DIR_PATH / upload_type / f"user_{user_id}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_allowed_image(filename: str) -> bool:
    """
    Vérifie si l'extension du fichier est autorisée
    
    Args:
        filename: Nom du fichier
    
    Returns:
        True si extension autorisée
    """
    if "." not in filename:
        return False
    
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in settings.ALLOWED_EXTENSIONS_LIST


# === CONFIGURATION EMAILS ===
EMAIL_TEMPLATES = {
    "verification": {
        "subject": "Vérifiez votre adresse email - Training Escalade",
        "template": "email_verification.html"
    },
    "password_reset": {
        "subject": "Réinitialisation de votre mot de passe - Training Escalade",
        "template": "password_reset.html"
    },
    "welcome": {
        "subject": "Bienvenue sur Training Escalade ! 🧗",
        "template": "welcome.html"
    }
}


# === CONSTANTES ===
class UserRole:
    """Rôles utilisateurs"""
    USER = "user"
    COACH = "coach"
    ADMIN = "admin"


class ExerciseType:
    """Types d'exercices"""
    SAE = "sae"
    OUTDOOR = "outdoor"
    RUNNING = "running"
    ROUTINE_MORNING = "routine_morning"
    ROUTINE_EVENING = "routine_evening"
    OTHER = "other"


class RouteType:
    """Types de voies"""
    SPORT = "sport"  # Équipé
    TRAD = "trad"    # Terrain d'aventure
    MIXED = "mixed"  # Mixte


class SessionType:
    """Types de séances"""
    FORCE = "force"
    RESISTANCE = "resistance"
    CONTINUITY = "continuity"
    ONSIGHT = "onsight"
    PROJECT = "project"
    MIXED = "mixed"