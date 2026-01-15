"""
Point d'entrée principal de l'application Pronote Amélioré
"""
import customtkinter as ctk
import json
import logging
from pathlib import Path
from tkinter import messagebox

from app.config import (
    APP_NAME,
    CREDENTIALS_FILE,
    SETTINGS_FILE,
    DATA_DIR
)
from app.pronote_api.client import PronoteClient
from app.utils.themes import ThemeManager
from app.ui.login import LoginWindow
from app.ui.main_window import MainWindow

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class App:
    """Application principale"""
    
    def __init__(self):
        self.pronote_client = PronoteClient()
        self.theme_manager = ThemeManager(SETTINGS_FILE)
        self.current_window = None
        
        # Appliquer le thème
        self.theme_manager.apply_theme()
    
    def run(self):
        """Lancer l'application"""
        logger.info(f"Démarrage de {APP_NAME}")
        
        # Vérifier s'il existe des credentials sauvegardés
        if self.try_auto_login():
            # Connexion automatique réussie
            self.show_main_window()
        else:
            # Afficher la fenêtre de login
            self.show_login_window()
        
        # Démarrer la boucle principale
        if self.current_window:
            self.current_window.mainloop()
    
    def try_auto_login(self) -> bool:
        """
        Essayer une connexion automatique avec les credentials sauvegardés
        
        Returns:
            True si connexion réussie, False sinon
        """
        if not CREDENTIALS_FILE.exists():
            return False
        
        try:
            with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
                credentials = json.load(f)
            
            # Vérifier qu'on a les informations nécessaires pour token_login
            if "username" in credentials and "url" in credentials:
                logger.info("Tentative de connexion automatique...")
                
                # Essayer la connexion par token si disponible
                if "cookies" in credentials or "token" in credentials:
                    success, message = self.pronote_client.login_with_token(credentials)
                    
                    if success:
                        logger.info("Connexion automatique réussie")
                        # Sauvegarder les nouveaux credentials
                        self.save_credentials(self.pronote_client.export_credentials())
                        return True
                    else:
                        logger.warning(f"Échec connexion automatique: {message}")
                        # Supprimer les credentials invalides
                        logger.info("Suppression des credentials invalides")
                        CREDENTIALS_FILE.unlink(missing_ok=True)
                
        except Exception as e:
            logger.error(f"Erreur lors de la connexion automatique: {e}")
            # Supprimer le fichier corrompu
            logger.info("Suppression du fichier credentials corrompu")
            CREDENTIALS_FILE.unlink(missing_ok=True)
        
        return False
    
    def show_login_window(self):
        """Afficher la fenêtre de connexion"""
        self.current_window = LoginWindow(self.handle_login)
    
    def show_main_window(self):
        """Afficher la fenêtre principale"""
        # Cacher la fenêtre de login au lieu de la détruire
        if self.current_window:
            self.current_window.withdraw()
        
        # Créer la fenêtre principale
        self.current_window = MainWindow(self.pronote_client, self.theme_manager)
        
        # S'assurer que la fenêtre est visible et au premier plan
        self.current_window.deiconify()
        self.current_window.lift()
        self.current_window.focus_force()
        
        # Protocole de fermeture de fenêtre pour nettoyer proprement
        self.current_window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def handle_login(self, credentials: dict):
        """
        Gérer la connexion depuis la fenêtre de login
        
        Args:
            credentials: Dictionnaire avec url, username, password, remember
        """
        url = credentials["url"]
        username = credentials["username"]
        password = credentials["password"]
        remember = credentials.get("remember", False)
        
        # Tenter la connexion
        success, message = self.pronote_client.login(url, username, password)
        
        if success:
            logger.info("Connexion réussie")
            
            # Sauvegarder les credentials si demandé
            if remember:
                exported_creds = self.pronote_client.export_credentials()
                if exported_creds:
                    # Ajouter l'URL et le username pour référence
                    exported_creds["url"] = url
                    exported_creds["username"] = username
                    self.save_credentials(exported_creds)
            
            # Afficher la fenêtre principale
            self.show_main_window()
        else:
            logger.error(f"Échec de connexion: {message}")
            
            # Réinitialiser l'état de chargement de la fenêtre de login
            if isinstance(self.current_window, LoginWindow):
                self.current_window.reset_loading_state()
            
            # Afficher l'erreur
            messagebox.showerror("Erreur de connexion", message)
    
    def save_credentials(self, credentials: dict):
        """Sauvegarder les credentials"""
        if credentials:
            try:
                with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(credentials, f, indent=2, default=str)
                logger.info("Credentials sauvegardés")
            except Exception as e:
                logger.error(f"Erreur sauvegarde credentials: {e}")
    
    def on_closing(self):
        """Gérer la fermeture de l'application"""
        logger.info("Fermeture de l'application")
        if self.current_window:
            self.current_window.quit()
            self.current_window.destroy()


def main():
    """Fonction principale"""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
