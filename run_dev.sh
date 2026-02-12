#!/bin/bash
# ============================================
# Training Escalade - Script de lancement développement
# ============================================

echo "🚀 Démarrage Training Escalade (mode développement)"
echo ""

# Vérifier que venv existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé !"
    echo "Créez-le avec : python3 -m venv venv"
    exit 1
fi

# Activer l'environnement virtuel
echo "📦 Activation environnement virtuel..."
source venv/bin/activate

# Vérifier que .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé !"
    echo "Copie .env.example en .env et configure-le."
    read -p "Voulez-vous le créer maintenant ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✅ Fichier .env créé. Édite-le avant de relancer."
        exit 0
    else
        exit 1
    fi
fi

# Vérifier que la base de données est initialisée
if [ ! -f "database/training.db" ] && [ "$DATABASE_TYPE" != "mysql" ]; then
    echo "⚠️  Base de données non initialisée !"
    read -p "Voulez-vous l'initialiser maintenant ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python database/init_db.py
    fi
fi

# Créer les dossiers nécessaires
echo "📁 Vérification des dossiers..."
mkdir -p logs
mkdir -p public_html/uploads/routes
mkdir -p public_html/uploads/avatars
mkdir -p backups/daily
mkdir -p backups/weekly
mkdir -p backups/manual

echo ""
echo "✅ Prêt à démarrer !"
echo ""
echo "🌐 L'application sera accessible sur : http://localhost:8000"
echo "📡 Documentation API : http://localhost:8000/docs"
echo ""
echo "Pour arrêter : Ctrl+C"
echo ""
echo "─────────────────────────────────────────────────────────"
echo ""

# Lancer l'application avec uvicorn (reload automatique en dev)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000