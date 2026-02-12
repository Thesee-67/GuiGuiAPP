# 🧗 Training Escalade - Application d'Entraînement

Application web multi-utilisateurs pour la gestion et le suivi de l'entraînement en escalade.

## 📋 Fonctionnalités

### 🔐 Authentification
- ✅ Inscription / Connexion sécurisée
- ✅ Vérification email obligatoire
- ✅ Récupération mot de passe par email
- ✅ Sessions JWT
- ✅ Isolation des données par utilisateur

### 📅 Planning
- ✅ Génération automatique du planning
- ✅ Planning visuel avec drag & drop
- ✅ Configuration personnalisée (séances/semaine, repos, etc.)
- ✅ Règles de récupération automatiques

### 🏋️ Entraînement
- ✅ Bibliothèque d'exercices personnalisables
- ✅ Templates de séances (CRUD complet)
- ✅ Saisie de séance avec timer intégré
- ✅ Historique complet

### 🧗 Grandes Voies
- ✅ Liste de toutes tes voies
- ✅ Upload photos
- ✅ Commentaires détaillés
- ✅ Tableau objectifs DE (ED-, TD+, etc.)
- ✅ Progression en temps réel

### 🏃 Course à Pied
- ✅ Suivi quotidien
- ✅ Distance, dénivelé, allure
- ✅ Historique et stats

### 📊 Statistiques
- ✅ Volume d'entraînement
- ✅ Progression cotations
- ✅ Records personnels
- ✅ Graphiques interactifs
- ✅ Export PDF/Excel

### 📋 Programmes
- ✅ Bibliothèque de programmes pré-définis
- ✅ Création de programmes personnalisés
- ✅ Planification par semaines

## 🛠️ Stack Technique

- **Backend** : FastAPI (Python 3.11+)
- **Frontend** : HTML5 + Bootstrap 5 + Alpine.js
- **Base de données** : MySQL
- **Authentification** : JWT
- **Email** : SMTP
- **Serveur** : Apache + Passenger (PlanetHoster)

## 📦 Installation

Voir [INSTALLATION.md](docs/INSTALLATION.md) pour le guide complet.

### Installation rapide

```bash
# 1. Cloner le projet
git clone [URL] training-escalade
cd training-escalade

# 2. Créer l'arborescence
python3 setup_project.py

# 3. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configuration
cp .env.example .env
# Éditer .env avec tes valeurs

# 6. Initialiser la base de données
python database/init_db.py

# 7. Lancer en dev
./run_dev.sh
```

## 🚀 Déploiement PlanetHoster

Voir [DEPLOYMENT.md](docs/DEPLOYMENT.md) pour le guide complet.

```bash
# Sur ton serveur PlanetHoster
cd ~/training-escalade
./deployment/deploy-planethoster.sh
```

## 📖 Documentation

- [📘 Installation](docs/INSTALLATION.md)
- [🚀 Déploiement](docs/DEPLOYMENT.md)
- [📡 API Documentation](docs/API.md)
- [👤 Guide Utilisateur](docs/USER_GUIDE.md)
- [🔒 Sécurité](docs/SECURITY.md)

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=backend tests/
```

## 🔐 Sécurité

- ✅ Mots de passe hashés (bcrypt)
- ✅ Tokens JWT signés
- ✅ Validation email obligatoire
- ✅ Rate limiting
- ✅ HTTPS obligatoire
- ✅ Isolation totale des données par utilisateur
- ✅ Protection CSRF
- ✅ Headers de sécurité

## 📝 License

Projet personnel - Olivier @ ClimbingTheNet

## 🤝 Contribution

Projet personnel, pas de contributions externes pour le moment.

## 📧 Contact

- Email : olivier@climbingthenet.fr
- Site : https://climbingthenet.fr

## 🎯 Roadmap

### Version 1.0 (Actuelle)
- [x] Authentification multi-utilisateurs
- [x] Planning automatique
- [x] Suivi entraînement
- [x] Objectifs DE
- [x] Statistiques

### Version 1.1 (À venir)
- [ ] Application mobile (PWA)
- [ ] Export automatique vers Strava
- [ ] Partage de séances entre utilisateurs
- [ ] Mode coach (suivi d'autres grimpeurs)
- [ ] API publique

### Version 2.0 (Futur)
- [ ] Communauté de grimpeurs
- [ ] Défis et compétitions
- [ ] IA : suggestions de séances
- [ ] Intégration capteurs (force doigts, cardio)

---

**Fait avec ❤️ pour la grimpe** 🧗‍♂️