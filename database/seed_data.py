#!/usr/bin/env python3
"""
Script d'ajout de données d'exemple
Pour tester l'application avec des données fictives
⚠️ À utiliser uniquement en développement !
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
import random

from backend.database import SessionLocal
from backend.models.user import User
from backend.models.user_config import UserConfig
from backend.models.exercise import Exercise
from backend.models.session_template import SessionTemplate
from backend.models.route import Route
from backend.models.goal_category import GoalCategory
from backend.models.running_session import RunningSession
from backend.config import settings, get_upload_path

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_demo_users(db: Session):
    """Crée des utilisateurs de démonstration"""
    print("\n👥 Création utilisateurs démo...")
    
    users_data = [
        {
            "email": "demo@training-escalade.fr",
            "username": "demo",
            "password": "Demo2024!",
            "first_name": "Demo",
            "last_name": "User",
            "role": "user",
        },
        {
            "email": "coach@training-escalade.fr",
            "username": "coach",
            "password": "Coach2024!",
            "first_name": "Coach",
            "last_name": "Expert",
            "role": "coach",
        },
    ]
    
    created_users = []
    
    for user_data in users_data:
        # Vérifier si existe déjà
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"   ℹ️  {user_data['email']} existe déjà")
            created_users.append(existing)
            continue
        
        # Créer l'utilisateur
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            password_hash=pwd_context.hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Créer config par défaut
        config = UserConfig(
            user_id=user.id,
            sae_per_week=4,
            outdoor_per_week_min=1,
            outdoor_per_week_max=2,
            rest_days=3,
            rest_frequency_weeks=3,
            morning_run_enabled=True,
        )
        db.add(config)
        
        # Créer dossiers uploads
        get_upload_path(user.id, "routes")
        get_upload_path(user.id, "avatars")
        
        created_users.append(user)
        print(f"   ✅ {user.email} - Mot de passe : {user_data['password']}")
    
    db.commit()
    return created_users


def create_demo_exercises(db: Session, user: User):
    """Crée des exercices d'exemple"""
    print(f"\n💪 Création exercices pour {user.username}...")
    
    exercises_data = [
        # SAE
        {"name": "Échauffement SAE", "type": "sae", "duration_min": 20, "description": "Traversées faciles + mobilité"},
        {"name": "Bloc Force Max", "type": "sae", "duration_min": 60, "description": "Blocs difficiles, repos complets"},
        {"name": "Résistance 4x4", "type": "sae", "duration_min": 90, "description": "4 voies en 4 minutes, 3 séries"},
        {"name": "Continuité Voies", "type": "sae", "duration_min": 120, "description": "Enchaînement voies sans repos"},
        {"name": "À vue", "type": "sae", "duration_min": 90, "description": "Grimper à vue, lecture de voie"},
        
        # Course
        {"name": "Footing Easy", "type": "running", "duration_min": 45, "description": "Course facile, allure conversation"},
        {"name": "Sortie Longue", "type": "running", "duration_min": 90, "description": "Endurance fondamentale"},
        {"name": "Fractionné Court", "type": "running", "duration_min": 60, "description": "8x400m récup 1min"},
        
        # Routines
        {"name": "Gainage Matin", "type": "routine_morning", "duration_min": 10, "description": "Planche, gainage latéral"},
        {"name": "Mobilité Épaules", "type": "routine_morning", "duration_min": 15, "description": "Étirements dynamiques"},
        {"name": "Étirements Soir", "type": "routine_evening", "duration_min": 15, "description": "Stretching complet"},
        
        # Outdoor
        {"name": "Sortie Falaise", "type": "outdoor", "duration_min": 240, "description": "Journée falaise, voies longues"},
        {"name": "Grande Voie", "type": "outdoor", "duration_min": 360, "description": "Engagement, plusieurs longueurs"},
    ]
    
    for ex_data in exercises_data:
        exercise = Exercise(
            user_id=user.id,
            name=ex_data["name"],
            type=ex_data["type"],
            duration_min=ex_data["duration_min"],
            description=ex_data["description"],
            intensity=3,
            focus="force,technique",
            created_at=datetime.utcnow()
        )
        db.add(exercise)
    
    db.commit()
    print(f"   ✅ {len(exercises_data)} exercices créés")


def create_demo_session_templates(db: Session, user: User):
    """Crée des templates de séances"""
    print(f"\n📝 Création templates séances pour {user.username}...")
    
    # Récupérer quelques exercices
    exercises = db.query(Exercise).filter(Exercise.user_id == user.id).limit(5).all()
    if not exercises:
        print("   ⚠️  Aucun exercice trouvé, skip templates")
        return
    
    templates_data = [
        {
            "name": "Force Max",
            "type": "force",
            "duration_min": 120,
            "description": "Séance force maximale sur bloc",
        },
        {
            "name": "Résistance",
            "type": "resistance",
            "duration_min": 150,
            "description": "Travail résistance 4x4",
        },
        {
            "name": "Continuité",
            "type": "continuity",
            "duration_min": 120,
            "description": "Volume de grimpe, voies enchaînées",
        },
    ]
    
    for tpl_data in templates_data:
        template = SessionTemplate(
            user_id=user.id,
            name=tpl_data["name"],
            type=tpl_data["type"],
            duration_min=tpl_data["duration_min"],
            description=tpl_data["description"],
            created_at=datetime.utcnow()
        )
        # Utiliser le setter pour convertir la liste en JSON
        template.exercise_ids = [ex.id for ex in exercises[:3]]
        db.add(template)
    
    db.commit()
    print(f"   ✅ {len(templates_data)} templates créés")


def create_demo_routes(db: Session, user: User):
    """Crée des grandes voies d'exemple"""
    print(f"\n🧗 Création grandes voies pour {user.username}...")
    
    routes_data = [
        # ED- Équipé
        {"name": "Pilier Rouge", "location": "Buoux", "grade": "7b+", "length": 250, "type": "sport"},
        {"name": "La Demande", "location": "Céüse", "grade": "7c", "length": 280, "type": "sport"},
        {"name": "Biographie", "location": "Céüse", "grade": "7b", "length": 220, "type": "sport"},
        
        # TD+ Trad
        {"name": "Voie des Dalles", "location": "Calanques", "grade": "6c", "length": 200, "type": "trad"},
        {"name": "Arête de la Barre", "location": "Vercors", "grade": "6b+", "length": 230, "type": "trad"},
    ]
    
    for route_data in routes_data:
        route = Route(
            user_id=user.id,
            name=route_data["name"],
            location=route_data["location"],
            grade=route_data["grade"],
            length_m=route_data["length"],
            type=route_data["type"],
            pitch_count=random.randint(4, 8),
            date_completed=datetime.utcnow() - timedelta(days=random.randint(10, 100)),
            comments=f"Super voie, ambiance grandiose !",
            rating=random.randint(3, 5),
            created_at=datetime.utcnow()
        )
        db.add(route)
    
    db.commit()
    print(f"   ✅ {len(routes_data)} grandes voies créées")


def create_demo_goal_categories(db: Session, user: User):
    """Crée les catégories d'objectifs DE"""
    print(f"\n🎯 Création objectifs DE pour {user.username}...")
    
    categories_data = [
        {
            "name": "ED- Équipé 200m",
            "description": "8 grandes voies ED- minimum 200m en terrain équipé",
            "required_count": 8,
            "criteria": {
                "min_grade": "7a",
                "min_length": 200,
                "route_type": "sport"
            }
        },
        {
            "name": "TD+ Trad 200m",
            "description": "8 grandes voies TD+ minimum 200m en terrain d'aventure",
            "required_count": 8,
            "criteria": {
                "min_grade": "6b",
                "min_length": 200,
                "route_type": "trad"
            }
        },
        {
            "name": "TD Équipé 400m",
            "description": "1 grande voie TD minimum 400m en terrain équipé",
            "required_count": 1,
            "criteria": {
                "min_grade": "6a",
                "min_length": 400,
                "route_type": "sport"
            }
        },
    ]
    
    for cat_data in categories_data:
        category = GoalCategory(
            user_id=user.id,
            name=cat_data["name"],
            description=cat_data["description"],
            required_count=cat_data["required_count"],
            order=1,
            created_at=datetime.utcnow()
        )
        # Utiliser le setter pour convertir le dict en JSON
        category.criteria = cat_data["criteria"]
        db.add(category)
    
    db.commit()
    print(f"   ✅ {len(categories_data)} catégories objectifs créées")


def create_demo_running_sessions(db: Session, user: User):
    """Crée des séances de course"""
    print(f"\n🏃 Création séances course pour {user.username}...")
    
    for i in range(10):
        days_ago = random.randint(1, 30)
        session = RunningSession(
            user_id=user.id,
            date=datetime.utcnow() - timedelta(days=days_ago),
            duration_min=random.randint(30, 90),
            distance_km=round(random.uniform(5, 15), 2),
            elevation_gain_m=random.randint(50, 500),
            average_pace_min_km=round(random.uniform(5, 7), 2),
            average_heart_rate=random.randint(130, 170),
            comments="Belle sortie",
            created_at=datetime.utcnow()
        )
        db.add(session)
    
    db.commit()
    print(f"   ✅ 10 séances course créées")


def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("🌱 SEED DATA - Données d'exemple")
    print("=" * 60)
    
    if settings.ENVIRONMENT == "production":
        print("\n⚠️  ATTENTION : Vous êtes en PRODUCTION")
        confirm = input("Voulez-vous vraiment ajouter des données de test ? (yes/no) : ")
        if confirm.lower() != "yes":
            print("❌ Annulé")
            return
    
    db = SessionLocal()
    
    try:
        # Créer les utilisateurs démo
        users = create_demo_users(db)
        
        # Pour chaque utilisateur, créer des données
        for user in users:
            create_demo_exercises(db, user)
            create_demo_session_templates(db, user)
            create_demo_routes(db, user)
            create_demo_goal_categories(db, user)
            create_demo_running_sessions(db, user)
        
        print("\n" + "=" * 60)
        print("✅ DONNÉES D'EXEMPLE CRÉÉES !")
        print("=" * 60)
        print("\n🔑 Comptes de test créés :")
        print("   • demo@training-escalade.fr - Mot de passe : Demo2024!")
        print("   • coach@training-escalade.fr - Mot de passe : Coach2024!")
        print("\n💡 Connectez-vous avec ces comptes pour tester l'application")
        print("")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
        sys.exit(0)