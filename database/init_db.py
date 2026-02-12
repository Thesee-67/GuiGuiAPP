#!/usr/bin/env python3
"""
Script d'initialisation de la base de données
- Crée toutes les tables
- Crée le premier utilisateur admin (optionnel)
- Crée les dossiers nécessaires
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from datetime import datetime
import logging

from backend.database import engine, SessionLocal, Base, init_db, check_db_connection
from backend.config import settings, get_upload_path

# Import de tous les modèles pour que SQLAlchemy les connaisse
from backend.models.user import User
from backend.models.user_config import UserConfig
from backend.models.exercise import Exercise
from backend.models.session_template import SessionTemplate
from backend.models.planning import Planning
from backend.models.training_session import TrainingSession
from backend.models.route import Route
from backend.models.goal_category import GoalCategory
from backend.models.running_session import RunningSession
from backend.models.program import Program
from backend.models.stats_cache import StatsCache
from backend.models.password_reset import PasswordResetToken
from backend.models.email_verification import EmailVerificationToken

# Pour le hash du mot de passe
from passlib.context import CryptContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_upload_directories():
    """Crée les dossiers pour les uploads"""
    print("\n📁 Création des dossiers uploads...")
    
    directories = [
        "public_html/uploads/routes",
        "public_html/uploads/avatars",
        "logs",
        "backups/daily",
        "backups/weekly",
        "backups/manual",
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Créer .gitkeep pour Git
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        
        print(f"   ✅ {directory}")
    
    print("✅ Dossiers créés")


def create_first_admin_user(db: Session) -> bool:
    """
    Crée le premier utilisateur admin si configuré dans .env
    
    Returns:
        bool: True si créé, False sinon
    """
    # Vérifier si un admin existe déjà
    admin_exists = db.query(User).filter(User.role == "admin").first()
    
    if admin_exists:
        print("ℹ️  Un administrateur existe déjà")
        return False
    
    # Vérifier les variables d'environnement
    if not all([
        settings.FIRST_ADMIN_EMAIL,
        settings.FIRST_ADMIN_USERNAME,
        settings.FIRST_ADMIN_PASSWORD
    ]):
        print("ℹ️  Pas de premier admin configuré dans .env")
        return False
    
    print("\n👤 Création du premier utilisateur admin...")
    
    try:
        # Créer l'utilisateur admin
        admin = User(
            email=settings.FIRST_ADMIN_EMAIL,
            username=settings.FIRST_ADMIN_USERNAME,
            password_hash=pwd_context.hash(settings.FIRST_ADMIN_PASSWORD),
            first_name="Admin",
            last_name="Training",
            role="admin",
            is_active=True,
            is_verified=True,  # Admin vérifié automatiquement
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        # Créer la config par défaut pour cet utilisateur
        user_config = UserConfig(
            user_id=admin.id,
            sae_per_week=4,
            outdoor_per_week_min=1,
            outdoor_per_week_max=2,
            rest_days=3,
            rest_frequency_weeks=3,
            morning_run_enabled=True,
            target_level="7a",
        )
        
        db.add(user_config)
        db.commit()
        
        # Créer les dossiers d'upload pour cet utilisateur
        get_upload_path(admin.id, "routes")
        get_upload_path(admin.id, "avatars")
        
        print(f"✅ Administrateur créé : {admin.email}")
        print(f"   Username : {admin.username}")
        print(f"   ID : {admin.id}")
        print(f"   ⚠️  IMPORTANT : Change le mot de passe après la première connexion !")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur création admin : {e}")
        return False


def verify_tables():
    """Vérifie que toutes les tables ont été créées"""
    print("\n🔍 Vérification des tables...")
    
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        "users",
        "user_configs",
        "exercises",
        "session_templates",
        "planning",
        "training_sessions",
        "routes",
        "goal_categories",
        "running_sessions",
        "programs",
        "stats_cache",
        "password_reset_tokens",
        "email_verification_tokens",
    ]
    
    all_ok = True
    for table in expected_tables:
        if table in tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MANQUANTE")
            all_ok = False
    
    if all_ok:
        print("✅ Toutes les tables sont présentes")
    else:
        print("⚠️  Certaines tables sont manquantes")
    
    return all_ok


def show_database_info():
    """Affiche les informations de la base de données"""
    print("\n📊 Informations base de données")
    print("=" * 50)
    print(f"Type : {settings.DATABASE_TYPE}")
    
    if settings.DATABASE_TYPE == "mysql":
        print(f"Serveur : {settings.DB_HOST}:{settings.DB_PORT}")
        print(f"Base : {settings.DB_NAME}")
        print(f"Utilisateur : {settings.DB_USER}")
    else:
        print(f"Fichier : {settings.SQLITE_PATH}")
    
    print(f"Environnement : {settings.ENVIRONMENT}")
    print(f"Debug : {settings.DEBUG}")
    print("=" * 50)


def main():
    """Fonction principale d'initialisation"""
    print("\n" + "=" * 60)
    print("🚀 INITIALISATION BASE DE DONNÉES - Training Escalade")
    print("=" * 60)
    
    # Afficher les infos
    show_database_info()
    
    # Vérifier la connexion
    print("\n🔌 Test de connexion...")
    if not check_db_connection():
        print("❌ Impossible de se connecter à la base de données")
        print("\n💡 Vérifiez votre configuration dans .env :")
        if settings.DATABASE_TYPE == "mysql":
            print("   - DB_HOST, DB_PORT, DB_NAME")
            print("   - DB_USER, DB_PASSWORD")
            print("\n📝 Assurez-vous d'avoir créé la base MySQL dans cPanel")
        else:
            print("   - SQLITE_PATH")
            print("   - Vérifiez les permissions du dossier")
        sys.exit(1)
    
    print("✅ Connexion OK")
    
    # Créer les dossiers
    create_upload_directories()
    
    # Créer les tables
    print("\n📋 Création des tables...")
    try:
        init_db()
        print("✅ Tables créées")
    except Exception as e:
        print(f"❌ Erreur création tables : {e}")
        sys.exit(1)
    
    # Vérifier les tables
    if not verify_tables():
        print("\n⚠️  Certaines tables n'ont pas été créées correctement")
        sys.exit(1)
    
    # Créer le premier admin
    db = SessionLocal()
    try:
        create_first_admin_user(db)
    finally:
        db.close()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("\n🎯 Prochaines étapes :")
    print("   1. Copier .env.example en .env (si pas déjà fait)")
    print("   2. Configurer les variables dans .env")
    print("   3. Lancer l'application : ./run_dev.sh")
    print("\n📚 Documentation : docs/INSTALLATION.md")
    print("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)