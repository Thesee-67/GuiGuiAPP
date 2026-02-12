"""
Gestion de la base de données
Connexion SQLAlchemy + Session management
"""

import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from backend.config import settings

logger = logging.getLogger(__name__)

# === CONFIGURATION ENGINE ===

if settings.DATABASE_TYPE == "mysql":
    # Configuration MySQL
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Vérifie la connexion avant utilisation
        pool_recycle=3600,   # Recycle les connexions après 1h
        echo=settings.DEBUG,  # Log les requêtes SQL en mode debug
    )
    logger.info(f"✅ Connexion MySQL configurée : {settings.DB_NAME}")
    
else:
    # Configuration SQLite
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # Nécessaire pour SQLite
        poolclass=StaticPool,  # Pool statique pour SQLite
        echo=settings.DEBUG,
    )
    logger.info(f"✅ Connexion SQLite configurée : {settings.SQLITE_PATH}")


# === SESSION FACTORY ===
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# === BASE MODEL ===
Base = declarative_base()


# === DEPENDENCY INJECTION ===
def get_db() -> Generator[Session, None, None]:
    """
    Dépendance FastAPI pour obtenir une session de base de données
    
    Usage dans les routes :
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: Session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === FONCTIONS UTILITAIRES ===

def init_db():
    """
    Initialise la base de données en créant toutes les tables
    À appeler au premier démarrage de l'application
    """
    try:
        # Import tous les modèles pour que Base les connaisse
        from backend.models import (
            user, user_config, exercise, session_template,
            planning, training_session, route, goal_category,
            running_session, program, stats_cache,
            password_reset, email_verification
        )
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables créées avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur création tables : {e}")
        raise


def drop_all_tables():
    """
    ⚠️ DANGER : Supprime TOUTES les tables
    À utiliser uniquement en développement !
    """
    if settings.ENVIRONMENT == "production":
        raise Exception("❌ INTERDIT en production !")
    
    Base.metadata.drop_all(bind=engine)
    logger.warning("⚠️ Toutes les tables ont été supprimées")


def reset_database():
    """
    ⚠️ DANGER : Reset complet de la base
    Supprime et recrée toutes les tables
    À utiliser uniquement en développement !
    """
    if settings.ENVIRONMENT == "production":
        raise Exception("❌ INTERDIT en production !")
    
    drop_all_tables()
    init_db()
    logger.warning("⚠️ Base de données réinitialisée")


def check_db_connection() -> bool:
    """
    Vérifie que la connexion à la base fonctionne
    
    Returns:
        bool: True si connexion OK, False sinon
    """
    try:
        db = SessionLocal()
        # Test simple de connexion (avec text() pour SQLAlchemy 2.0)
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Connexion base de données OK")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur connexion base de données : {e}")
        return False


def get_table_counts() -> dict:
    """
    Compte le nombre d'enregistrements dans chaque table
    Utile pour le debug et les stats
    
    Returns:
        dict: Dictionnaire {nom_table: count}
    """
    db = SessionLocal()
    counts = {}
    
    try:
        # Import des modèles
        from backend.models.user import User
        from backend.models.exercise import Exercise
        from backend.models.session_template import SessionTemplate
        from backend.models.planning import Planning
        from backend.models.training_session import TrainingSession
        from backend.models.route import Route
        from backend.models.goal_category import GoalCategory
        from backend.models.running_session import RunningSession
        from backend.models.program import Program
        
        # Compter les enregistrements
        counts = {
            "users": db.query(User).count(),
            "exercises": db.query(Exercise).count(),
            "session_templates": db.query(SessionTemplate).count(),
            "planning": db.query(Planning).count(),
            "training_sessions": db.query(TrainingSession).count(),
            "routes": db.query(Route).count(),
            "goal_categories": db.query(GoalCategory).count(),
            "running_sessions": db.query(RunningSession).count(),
            "programs": db.query(Program).count(),
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du comptage : {e}")
    finally:
        db.close()
    
    return counts


# === CONTEXT MANAGER (optionnel) ===

class DatabaseSession:
    """
    Context manager pour gérer les sessions de base de données
    
    Usage :
        with DatabaseSession() as db:
            user = db.query(User).first()
            print(user.email)
    """
    
    def __enter__(self):
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        self.db.close()


# === LOGGING CONFIGURATION ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# === TEST AU DÉMARRAGE ===
if __name__ == "__main__":
    print("🧪 Test de connexion à la base de données...")
    
    if check_db_connection():
        print("✅ Connexion réussie !")
        print(f"📊 Type de base : {settings.DATABASE_TYPE}")
        
        if settings.DATABASE_TYPE == "mysql":
            print(f"📍 Serveur : {settings.DB_HOST}:{settings.DB_PORT}")
            print(f"📦 Base : {settings.DB_NAME}")
        else:
            print(f"📄 Fichier : {settings.SQLITE_PATH}")
    else:
        print("❌ Échec de la connexion")