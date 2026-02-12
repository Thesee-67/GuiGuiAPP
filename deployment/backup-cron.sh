#!/bin/bash
# ============================================
# Training Escalade - Backup Automatique
# À lancer quotidiennement via cron
# ============================================

# Configuration
APP_DIR="$HOME/training-escalade"
BACKUP_DIR="$APP_DIR/backups/daily"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Charger les variables d'environnement
source "$APP_DIR/.env"

# Créer le dossier de backup
mkdir -p "$BACKUP_DIR"

echo "💾 Backup Training Escalade - $(date)"
echo "========================================"

# === BACKUP BASE DE DONNÉES ===
if [ "$DATABASE_TYPE" = "mysql" ]; then
    echo "📊 Backup MySQL..."
    mysqldump -h $DB_HOST \
              -u $DB_USER \
              -p$DB_PASSWORD \
              $DB_NAME \
              > "$BACKUP_DIR/db_$DATE.sql"
    
    # Compression
    gzip "$BACKUP_DIR/db_$DATE.sql"
    echo "✅ Backup MySQL créé: db_$DATE.sql.gz"
else
    echo "📊 Backup SQLite..."
    cp "$APP_DIR/database/training.db" "$BACKUP_DIR/db_$DATE.db"
    gzip "$BACKUP_DIR/db_$DATE.db"
    echo "✅ Backup SQLite créé: db_$DATE.db.gz"
fi

# === BACKUP UPLOADS (PHOTOS) ===
echo "📸 Backup uploads..."
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" \
    -C "$APP_DIR/public_html" \
    uploads/ \
    2>/dev/null || echo "⚠️  Aucun upload à sauvegarder"

if [ -f "$BACKUP_DIR/uploads_$DATE.tar.gz" ]; then
    echo "✅ Backup uploads créé: uploads_$DATE.tar.gz"
fi

# === BACKUP CONFIGURATION ===
echo "⚙️  Backup configuration..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    -C "$APP_DIR" \
    .env \
    public_html/.htaccess \
    2>/dev/null

echo "✅ Backup config créé: config_$DATE.tar.gz"

# === NETTOYAGE ANCIENS BACKUPS ===
echo "🧹 Nettoyage anciens backups (>${RETENTION_DAYS} jours)..."

find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "db_*.db.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "uploads_*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Compter les backups restants
BACKUPS_COUNT=$(ls -1 "$BACKUP_DIR"/db_*.gz 2>/dev/null | wc -l)
echo "✅ ${BACKUPS_COUNT} backups conservés"

# === TAILLE TOTALE ===
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "📦 Taille totale backups: $TOTAL_SIZE"

# === BACKUP HEBDOMADAIRE (dimanche) ===
if [ $(date +%u) -eq 7 ]; then
    echo "📅 Copie backup hebdomadaire..."
    WEEKLY_DIR="$APP_DIR/backups/weekly"
    mkdir -p "$WEEKLY_DIR"
    
    cp "$BACKUP_DIR/db_$DATE".* "$WEEKLY_DIR/" 2>/dev/null || true
    cp "$BACKUP_DIR/uploads_$DATE.tar.gz" "$WEEKLY_DIR/" 2>/dev/null || true
    
    # Nettoyer les backups hebdo > 90 jours
    find "$WEEKLY_DIR" -name "*.gz" -mtime +90 -delete
    
    echo "✅ Backup hebdomadaire créé"
fi

echo ""
echo "✅ Backup terminé avec succès !"
echo "========================================"

# === LOG ===
echo "[$DATE] Backup OK - Size: $TOTAL_SIZE" >> "$APP_DIR/logs/backup.log"