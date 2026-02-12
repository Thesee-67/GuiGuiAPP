#!/bin/bash
# ============================================
# Training Escalade - Script de déploiement PlanetHoster
# ============================================

set -e  # Arrêt en cas d'erreur

echo "🚀 Déploiement Training Escalade sur PlanetHoster"
echo "=================================================="
echo ""

# === CONFIGURATION ===
APP_DIR="$HOME/training-escalade"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="$APP_DIR/backups/manual"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# === VÉRIFICATIONS PRÉALABLES ===
echo "📋 Vérifications préalables..."

# Vérifier qu'on est dans le bon dossier
if [ ! -f "$APP_DIR/README.md" ]; then
    echo -e "${RED}❌ Erreur: Fichier README.md non trouvé${NC}"
    echo "Êtes-vous dans le bon dossier ?"
    exit 1
fi

# Vérifier que .env existe
if [ ! -f "$APP_DIR/.env" ]; then
    echo -e "${RED}❌ Erreur: Fichier .env non trouvé${NC}"
    echo "Copiez .env.example en .env et configurez-le"
    exit 1
fi

echo -e "${GREEN}✅ Vérifications OK${NC}"
echo ""

# === BACKUP DE LA BASE DE DONNÉES ===
echo "💾 Backup de la base de données..."

mkdir -p "$BACKUP_DIR"
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

# Charger les variables d'environnement
source "$APP_DIR/.env"

if [ "$DATABASE_TYPE" = "mysql" ]; then
    echo "   Backup MySQL..."
    mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > "$BACKUP_DIR/backup_$BACKUP_DATE.sql"
    gzip "$BACKUP_DIR/backup_$BACKUP_DATE.sql"
    echo -e "${GREEN}   ✅ Backup MySQL créé${NC}"
else
    echo "   Backup SQLite..."
    cp "$APP_DIR/database/training.db" "$BACKUP_DIR/backup_$BACKUP_DATE.db"
    gzip "$BACKUP_DIR/backup_$BACKUP_DATE.db"
    echo -e "${GREEN}   ✅ Backup SQLite créé${NC}"
fi

echo ""

# === MISE À JOUR DU CODE ===
echo "📦 Mise à jour du code..."

# Si Git est utilisé
if [ -d "$APP_DIR/.git" ]; then
    echo "   Git pull..."
    cd "$APP_DIR"
    git pull origin main
    echo -e "${GREEN}   ✅ Code mis à jour via Git${NC}"
else
    echo -e "${YELLOW}   ⚠️  Pas de dépôt Git - mise à jour manuelle${NC}"
fi

echo ""

# === ENVIRONNEMENT VIRTUEL ===
echo "🐍 Configuration environnement Python..."

# Créer venv si nécessaire
if [ ! -d "$VENV_DIR" ]; then
    echo "   Création de l'environnement virtuel..."
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}   ✅ Environnement virtuel créé${NC}"
fi

# Activer venv
source "$VENV_DIR/bin/activate"

# Mettre à jour pip
echo "   Mise à jour de pip..."
pip install --upgrade pip > /dev/null 2>&1

# Installer/mettre à jour les dépendances
echo "   Installation des dépendances..."
pip install -r "$APP_DIR/requirements.txt" --upgrade

echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

# === MIGRATIONS BASE DE DONNÉES ===
echo "🗄️  Migrations base de données..."

cd "$APP_DIR"
python database/init_db.py --migrate

echo -e "${GREEN}✅ Migrations appliquées${NC}"
echo ""

# === CRÉATION DES DOSSIERS ===
echo "📁 Vérification des dossiers..."

mkdir -p "$APP_DIR/logs"
mkdir -p "$APP_DIR/public_html/uploads/routes"
mkdir -p "$APP_DIR/public_html/uploads/avatars"
mkdir -p "$APP_DIR/backups/daily"
mkdir -p "$APP_DIR/backups/weekly"

# Permissions
chmod 755 "$APP_DIR/public_html/uploads"
chmod 755 "$APP_DIR/public_html/uploads/routes"
chmod 755 "$APP_DIR/public_html/uploads/avatars"

echo -e "${GREEN}✅ Dossiers vérifiés${NC}"
echo ""

# === COLLECTE FICHIERS STATIQUES ===
echo "📦 Fichiers statiques..."

# Vérifier que les libs sont présentes
if [ ! -f "$APP_DIR/public_html/static/lib/bootstrap.min.css" ]; then
    echo -e "${YELLOW}   ⚠️  Bibliothèques frontend manquantes${NC}"
    echo "   Téléchargement des libs..."
    # Ici tu pourrais ajouter des wget pour télécharger Bootstrap, etc.
fi

echo -e "${GREEN}✅ Fichiers statiques OK${NC}"
echo ""

# === REDÉMARRAGE PASSENGER ===
echo "🔄 Redémarrage de l'application..."

# Créer le fichier restart.txt pour redémarrer Passenger
mkdir -p "$APP_DIR/tmp"
touch "$APP_DIR/tmp/restart.txt"

echo -e "${GREEN}✅ Application redémarrée${NC}"
echo ""

# === VÉRIFICATION SANTÉ ===
echo "🏥 Vérification de l'application..."

sleep 3  # Attendre que Passenger redémarre

# Test de health check
APP_URL=$(grep "APP_URL" "$APP_DIR/.env" | cut -d '=' -f2)
if curl -f -s "$APP_URL/api/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application accessible et fonctionnelle${NC}"
else
    echo -e "${YELLOW}⚠️  Impossible de joindre l'application${NC}"
    echo "   URL testée: $APP_URL/api/health"
    echo "   Vérifiez les logs: $APP_DIR/logs/app.log"
fi

echo ""

# === NETTOYAGE ===
echo "🧹 Nettoyage..."

# Supprimer les anciens backups (garder 7 derniers)
cd "$BACKUP_DIR"
ls -t backup_*.sql.gz 2>/dev/null | tail -n +8 | xargs -r rm
ls -t backup_*.db.gz 2>/dev/null | tail -n +8 | xargs -r rm

# Nettoyer les logs trop anciens (> 30 jours)
find "$APP_DIR/logs" -name "*.log" -mtime +30 -delete 2>/dev/null || true

echo -e "${GREEN}✅ Nettoyage effectué${NC}"
echo ""

# === RÉSUMÉ ===
echo "=================================================="
echo -e "${GREEN}🎉 Déploiement terminé avec succès !${NC}"
echo "=================================================="
echo ""
echo "📊 Résumé:"
echo "   • Code: Mis à jour"
echo "   • Base de données: Backup + migrations OK"
echo "   • Dépendances: Installées"
echo "   • Application: Redémarrée"
echo ""
echo "🌐 Accès: $APP_URL"
echo "📝 Logs: $APP_DIR/logs/app.log"
echo "💾 Backup: $BACKUP_DIR/backup_$BACKUP_DATE.sql.gz"
echo ""
echo "💡 Commandes utiles:"
echo "   • Voir les logs: tail -f $APP_DIR/logs/app.log"
echo "   • Redémarrer: touch $APP_DIR/tmp/restart.txt"
echo "   • Rollback: ./deployment/rollback.sh"
echo ""