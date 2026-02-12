# 📘 Guide d'Installation - Training Escalade

Guide complet pour installer l'application en local et sur PlanetHoster.

## 📋 Prérequis

### Système
- **Python 3.11+** (vérifier avec `python --version`)
- **Git** (optionnel mais recommandé)
- Accès SSH à ton serveur PlanetHoster

### Comptes nécessaires
- ✅ Compte PlanetHoster actif
- ✅ Accès cPanel
- ✅ Email SMTP configuré (pour envoi emails)

---

## 🚀 Installation Locale (Développement)

### Étape 1 : Cloner/Télécharger le projet

```bash
# Option A : Via Git
git clone https://github.com/ton-user/training-escalade.git
cd training-escalade

# Option B : Sans Git
# Télécharge et décompresse le ZIP
cd training-escalade
```

### Étape 2 : Créer l'arborescence

```bash
# Créer automatiquement tous les fichiers et dossiers
python3 setup_project.py
```

Résultat :
```
✅ Arborescence complète créée avec succès !
📊 Statistiques :
   📁 Dossiers créés: 45
   📄 Fichiers créés: 140
```

### Étape 3 : Créer l'environnement virtuel

```bash
# Créer le venv
python3 -m venv venv

# Activer (Linux/Mac)
source venv/bin/activate

# Activer (Windows)
venv\Scripts\activate
```

Tu devrais voir `(venv)` devant ton prompt.

### Étape 4 : Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Attendre l'installation (2-3 minutes).

### Étape 5 : Configuration

```bash
# Copier l'exemple de configuration
cp .env.example .env

# Éditer avec ton éditeur
nano .env  # ou code .env, vim .env, etc.
```

**Configuration minimale pour le développement local** :

```env
# Sécurité
SECRET_KEY=genere-une-cle-secrete-longue-ici

# Base de données (SQLite pour dev local)
DATABASE_TYPE=sqlite

# Email (désactiver pour dev local)
SMTP_ENABLED=False
EMAIL_VERIFICATION_REQUIRED=False

# Admin par défaut
FIRST_ADMIN_EMAIL=toi@example.com
FIRST_ADMIN_USERNAME=admin
FIRST_ADMIN_PASSWORD=MotDePasseTemporaire123!
```

**Générer une SECRET_KEY** :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Étape 6 : Initialiser la base de données

```bash
python database/init_db.py
```

Résultat :
```
✅ Base de données initialisée
✅ Tables créées
✅ Utilisateur admin créé
```

### Étape 7 : Lancer l'application

```bash
./run_dev.sh
```

Ou manuellement :
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'application est accessible sur :
- 🌐 **Interface** : http://localhost:8000
- 📡 **API Docs** : http://localhost:8000/docs
- 📚 **ReDoc** : http://localhost:8000/redoc

### Étape 8 : Premier test

1. Ouvre http://localhost:8000
2. Clique "S'inscrire"
3. Crée ton compte
4. Explore l'application ! 🎉

---

## 🌐 Installation Production (PlanetHoster)

### Prérequis PlanetHoster

#### 1. Créer la base de données MySQL

Dans **cPanel → MySQL Databases** :

1. **Créer une base** :
   - Nom : `training_escalade`
   - Créer

2. **Créer un utilisateur** :
   - Username : `training_user`
   - Password : [générer un mot de passe fort]
   - Créer

3. **Lier utilisateur à la base** :
   - Sélectionner utilisateur + base
   - Cocher "ALL PRIVILEGES"
   - Make Changes

4. **Noter les infos** :
   ```
   DB_HOST=localhost
   DB_NAME=training_escalade
   DB_USER=training_user
   DB_PASSWORD=[ton-mot-de-passe]
   ```

#### 2. Créer l'email SMTP

Dans **cPanel → Email Accounts** :

1. Créer un compte :
   - Email : `noreply@climbingthenet.fr`
   - Password : [mot de passe fort]
   - Quota : 250 MB suffit

2. **Noter les infos SMTP** :
   ```
   SMTP_HOST=mail.climbingthenet.fr
   SMTP_PORT=465
   SMTP_USERNAME=noreply@climbingthenet.fr
   SMTP_PASSWORD=[ton-mot-de-passe]
   ```

### Upload des fichiers

#### Option A : Via Git (Recommandé)

```bash
# Sur ton ordinateur
git init
git add .
git commit -m "Initial commit"
git remote add origin [url-git]
git push -u origin main

# Sur le serveur PlanetHoster (SSH)
ssh ton-user@ton-serveur.planethoster.world
cd ~
git clone [url-git] training-escalade
```

#### Option B : Via SFTP

1. Utilise FileZilla ou WinSCP
2. Connecte-toi en SFTP
3. Upload TOUT le dossier `training-escalade` vers `~/training-escalade`
4. **Ne PAS uploader** : `venv/`, `__pycache__/`, `.env`

### Configuration Serveur

```bash
# Connexion SSH
ssh ton-user@ton-serveur.planethoster.world

# Aller dans le dossier
cd ~/training-escalade

# Créer le fichier .env
nano .env
```

**Configuration Production** :

```env
# Application
DEBUG=False
ENVIRONMENT=production
APP_URL=https://training.climbingthenet.fr

# Sécurité (IMPORTANT : nouvelle clé différente du dev !)
SECRET_KEY=[ta-vraie-cle-secrete-ultra-longue]

# Base de données MySQL
DATABASE_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=training_escalade
DB_USER=training_user
DB_PASSWORD=[mot-de-passe-mysql]

# Email SMTP
SMTP_ENABLED=True
SMTP_HOST=mail.climbingthenet.fr
SMTP_PORT=465
SMTP_USE_TLS=True
SMTP_USERNAME=noreply@climbingthenet.fr
SMTP_PASSWORD=[mot-de-passe-email]
SMTP_FROM_EMAIL=noreply@climbingthenet.fr

# Vérification email
EMAIL_VERIFICATION_REQUIRED=True

# Premier admin
FIRST_ADMIN_EMAIL=olivier@climbingthenet.fr
FIRST_ADMIN_USERNAME=olivier
FIRST_ADMIN_PASSWORD=[mot-de-passe-temporaire]
```

### Déploiement Automatique

```bash
# Rendre le script exécutable
chmod +x deployment/deploy-planethoster.sh

# Lancer le déploiement
./deployment/deploy-planethoster.sh
```

Le script va :
1. ✅ Créer le backup de la DB
2. ✅ Créer l'environnement virtuel
3. ✅ Installer les dépendances
4. ✅ Initialiser la base de données
5. ✅ Créer les dossiers nécessaires
6. ✅ Redémarrer l'application

### Configuration .htaccess

Édite `public_html/.htaccess` et remplace `TON_USER` :

```bash
nano public_html/.htaccess
```

Remplace :
```apache
PassengerAppRoot /home/TON_USER/training-escalade
PassengerPython /home/TON_USER/training-escalade/venv/bin/python
```

Par (exemple si ton user est `olivier123`) :
```apache
PassengerAppRoot /home/olivier123/training-escalade
PassengerPython /home/olivier123/training-escalade/venv/bin/python
```

### Configuration Passenger

Édite `public_html/passenger_wsgi.py` :

```bash
nano public_html/passenger_wsgi.py
```

Idem, remplace les chemins.

### Redémarrage Final

```bash
# Créer le fichier restart.txt
mkdir -p tmp
touch tmp/restart.txt
```

Passenger va redémarrer automatiquement.

### Vérification

1. Va sur https://training.climbingthenet.fr
2. Tu devrais voir la page de connexion ✅

Si erreur 500 :
```bash
# Voir les logs
tail -f logs/app.log

# Ou logs Apache
tail -f ~/logs/error_log
```

---

## 🔧 Configuration Sous-Domaine

Dans **cPanel → Domains → Subdomains** :

1. Créer sous-domaine : `training`
2. Document Root : `/home/ton-user/training-escalade/public_html`
3. Créer

Attendre propagation DNS (5-30 minutes).

SSL automatique Let's Encrypt se configure tout seul ! ✅

---

## ✅ Checklist Post-Installation

- [ ] Application accessible sur l'URL
- [ ] Page de connexion s'affiche
- [ ] Création de compte fonctionne
- [ ] Email de vérification reçu
- [ ] Connexion fonctionne
- [ ] Dashboard s'affiche
- [ ] Upload de photo fonctionne
- [ ] Création d'exercice fonctionne

---

## 🐛 Dépannage

### Erreur : "Module not found"
```bash
# Réinstaller les dépendances
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
touch tmp/restart.txt
```

### Erreur : "Can't connect to database"
- Vérifier .env (DB_HOST, DB_USER, DB_PASSWORD)
- Vérifier que la base existe dans cPanel
- Tester connexion : `mysql -h localhost -u training_user -p`

### Erreur : "500 Internal Server Error"
```bash
# Voir les logs détaillés
tail -f logs/app.log
tail -f ~/logs/error_log

# Vérifier les permissions
chmod 755 public_html
chmod 755 public_html/uploads
```

### Application ne redémarre pas
```bash
# Forcer le redémarrage
pkill -f passenger
touch tmp/restart.txt
```

### Emails ne partent pas
- Vérifier SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD dans .env
- Tester l'email dans cPanel → Email Accounts → Check Email
- Vérifier les logs : `grep "SMTP" logs/app.log`

---

## 📚 Prochaines Étapes

Consulte les autres docs :
- [DEPLOYMENT.md](DEPLOYMENT.md) - Gestion déploiement
- [API.md](API.md) - Documentation API
- [USER_GUIDE.md](USER_GUIDE.md) - Guide utilisateur
- [SECURITY.md](SECURITY.md) - Bonnes pratiques sécurité

---

**Besoin d'aide ? olivier@climbingthenet.fr** 📧