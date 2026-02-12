"""
Training Escalade - Point d'entrée Passenger WSGI
Ce fichier est appelé par Apache + Passenger pour lancer l'application FastAPI
"""

import sys
import os
from pathlib import Path

# === CONFIGURATION CHEMIN ===
# Remplace TON_USER par ton vrai nom d'utilisateur PlanetHoster
INTERP = os.path.expanduser("~/training-escalade/venv/bin/python")
BASE_DIR = os.path.expanduser("~/training-escalade")

# Force l'utilisation du Python de l'environnement virtuel
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajoute les chemins au PYTHONPATH
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

# Change le répertoire de travail
os.chdir(BASE_DIR)

# === CHARGEMENT .ENV ===
from dotenv import load_dotenv
env_path = Path(BASE_DIR) / ".env"
load_dotenv(dotenv_path=env_path)

# === IMPORT APPLICATION FASTAPI ===
try:
    from backend.main import app as application
    
    # Log de démarrage
    print(f"✅ Training Escalade démarré depuis {BASE_DIR}")
    print(f"✅ Python: {sys.version}")
    print(f"✅ Environment: {os.getenv('ENVIRONMENT', 'production')}")
    
except Exception as e:
    # En cas d'erreur, on affiche des détails pour debug
    print(f"❌ ERREUR AU DÉMARRAGE: {e}")
    print(f"Python Path: {sys.path}")
    print(f"Base Dir: {BASE_DIR}")
    
    # Créer une application WSGI d'erreur temporaire
    def application(environ, start_response):
        status = '500 Internal Server Error'
        output = f"""
        <html>
        <head><title>Erreur - Training Escalade</title></head>
        <body>
            <h1>Erreur de démarrage de l'application</h1>
            <p><strong>Erreur:</strong> {e}</p>
            <p><strong>Python:</strong> {sys.version}</p>
            <p><strong>Base Dir:</strong> {BASE_DIR}</p>
            <hr>
            <p>Vérifiez les logs pour plus de détails.</p>
        </body>
        </html>
        """.encode('utf-8')
        
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]

# Export de l'application pour Passenger
# Passenger cherche une variable appelée "application"