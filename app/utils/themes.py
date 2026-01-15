"""
Gestion des thèmes de l'application
"""
import customtkinter as ctk
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ThemeManager:
    """Gestionnaire de thèmes pour l'application"""
    
    def __init__(self, settings_file: Path):
        self.settings_file = settings_file
        self.current_theme = self._load_theme_preference()
        
    def _load_theme_preference(self) -> str:
        """Charger la préférence de thème depuis les settings"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return settings.get("theme", "dark")
            except Exception as e:
                logger.error(f"Erreur chargement préférence thème: {e}")
        return "dark"
    
    def _save_theme_preference(self, theme: str):
        """Sauvegarder la préférence de thème"""
        settings = {}
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            except Exception:
                pass
        
        settings["theme"] = theme
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur sauvegarde préférence thème: {e}")
    
    def apply_theme(self, theme: str = None):
        """
        Appliquer un thème
        
        Args:
            theme: 'dark' ou 'light', ou None pour utiliser le thème actuel
        """
        if theme is None:
            theme = self.current_theme
        
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
        else:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
        
        self.current_theme = theme
        self._save_theme_preference(theme)
        logger.info(f"Thème appliqué: {theme}")
    
    def toggle_theme(self):
        """Basculer entre thème clair et sombre"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        return new_theme
    
    def get_current_theme(self) -> str:
        """Retourner le thème actuel"""
        return self.current_theme
