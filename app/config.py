"""
Configuration centralisée de l'application Pronote Amélioré
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Créer les dossiers s'ils n'existent pas
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# Fichiers de données
CREDENTIALS_FILE = DATA_DIR / "credentials.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
CACHE_FILE = DATA_DIR / "cache.json"

# Configuration de l'application
APP_NAME = "Pronote Amélioré"
APP_VERSION = "1.0.0"
WINDOW_SIZE = (1200, 800)
MIN_WINDOW_SIZE = (900, 600)

# URLs Pronote courantes (pour suggestions)
COMMON_PRONOTE_URLS = [
    "https://demo.index-education.net/pronote/eleve.html",
    # Ajoutez d'autres URLs courantes ici
]

# Configuration du cache
CACHE_DURATION_MINUTES = {
    "schedule": 30,      # Emploi du temps: 30 minutes
    "grades": 60,        # Notes: 1 heure
    "homework": 15,      # Devoirs: 15 minutes
    "messages": 5,       # Messages: 5 minutes
}

# Configuration des notifications
NOTIFICATIONS_ENABLED = True
CHECK_HOMEWORK_INTERVAL = 3600  # Vérifier les devoirs toutes les heures
HOMEWORK_REMINDER_DAYS = [1, 2]  # Rappels à J-1 et J-2

# Thèmes
THEMES = {
    "dark": {
        "mode": "dark",
        "color_theme": "blue",
    },
    "light": {
        "mode": "light",
        "color_theme": "blue",
    }
}

DEFAULT_THEME = "dark"

# Couleurs par matière (pour l'emploi du temps)
SUBJECT_COLORS = {
    "Mathématiques": "#3b82f6",
    "Français": "#ef4444",
    "Anglais": "#10b981",
    "Histoire": "#f59e0b",
    "Géographie": "#8b5cf6",
    "Physique": "#06b6d4",
    "Chimie": "#ec4899",
    "SVT": "#84cc16",
    "EPS": "#f97316",
    "Technologie": "#6366f1",
    "default": "#6b7280",
}

# Messages d'erreur
ERROR_MESSAGES = {
    "connection": "Impossible de se connecter à Pronote. Vérifiez votre connexion internet et vos identifiants.",
    "invalid_url": "URL Pronote invalide. Veuillez vérifier l'adresse.",
    "session_expired": "Votre session a expiré. Reconnexion en cours...",
    "network_error": "Erreur réseau. Vérifiez votre connexion internet.",
}
