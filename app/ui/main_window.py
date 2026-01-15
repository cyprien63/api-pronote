"""
Fenêtre principale de l'application
"""
import customtkinter as ctk
from typing import Optional
import logging

from app.config import APP_NAME, WINDOW_SIZE, MIN_WINDOW_SIZE
from app.pronote_api.client import PronoteClient
from app.utils.themes import ThemeManager
from app.ui.schedule import SchedulePage
from app.ui.grades import GradesPage
from app.ui.homework import HomeworkPage
from app.ui.messages import MessagesPage

logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """Fenêtre principale de l'application"""
    
    def __init__(self, pronote_client: PronoteClient, theme_manager: ThemeManager):
        super().__init__()
        
        self.pronote_client = pronote_client
        self.theme_manager = theme_manager
        
        # Configuration de la fenêtre
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.minsize(MIN_WINDOW_SIZE[0], MIN_WINDOW_SIZE[1])
        
        # Variables
        self.current_page = None
        self.user_info = None
        
        # Créer l'interface
        self.create_widgets()
        
        # Charger les infos utilisateur
        self.load_user_info()
        
        # Afficher la première page
        self.show_schedule()
        
    def create_widgets(self):
        """Créer les widgets de l'interface"""
        
        # Configuration du grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # === SIDEBAR ===
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)  # Spacer
        
        # Logo / Titre
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="📚 Pronote",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Nom utilisateur
        self.user_label = ctk.CTkLabel(
            self.sidebar,
            text="Chargement...",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.user_label.grid(row=1, column=0, padx=20, pady=(0, 30))
        
        # Boutons de navigation
        self.schedule_button = ctk.CTkButton(
            self.sidebar,
            text="📅 Emploi du temps",
            command=self.show_schedule,
            height=40,
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        self.schedule_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.grades_button = ctk.CTkButton(
            self.sidebar,
            text="📊 Notes",
            command=self.show_grades,
            height=40,
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        self.grades_button.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.homework_button = ctk.CTkButton(
            self.sidebar,
            text="📝 Devoirs",
            command=self.show_homework,
            height=40,
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        self.homework_button.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        self.messages_button = ctk.CTkButton(
            self.sidebar,
            text="✉️ Messages",
            command=self.show_messages,
            height=40,
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        self.messages_button.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.grid(row=6, column=0, sticky="nsew")
        
        # Bouton thème
        self.theme_button = ctk.CTkButton(
            self.sidebar,
            text="🌙 Mode sombre" if self.theme_manager.get_current_theme() == "dark" else "☀️ Mode clair",
            command=self.toggle_theme,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.theme_button.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        
        # Bouton déconnexion
        logout_button = ctk.CTkButton(
            self.sidebar,
            text="🚪 Déconnexion",
            command=self.logout,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=2
        )
        logout_button.grid(row=8, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # === ZONE DE CONTENU ===
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
    def load_user_info(self):
        """Charger les informations utilisateur"""
        self.user_info = self.pronote_client.get_user_info()
        if self.user_info:
            self.user_label.configure(text=f"👤 {self.user_info['name']}")
        else:
            self.user_label.configure(text="👤 Utilisateur")
    
    def clear_content(self):
        """Effacer le contenu actuel"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_page = None
    
    def reset_button_colors(self):
        """Réinitialiser les couleurs des boutons de navigation"""
        buttons = [
            self.schedule_button,
            self.grades_button,
            self.homework_button,
            self.messages_button
        ]
        for button in buttons:
            button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
    
    def show_schedule(self):
        """Afficher la page emploi du temps"""
        if isinstance(self.current_page, SchedulePage):
            return
        
        self.clear_content()
        self.reset_button_colors()
        self.schedule_button.configure(fg_color=["#2B7DC0", "#164A75"])
        
        self.current_page = SchedulePage(self.content_frame, self.pronote_client)
        self.current_page.pack(fill="both", expand=True)
        
        logger.info("Page emploi du temps affichée")
    
    def show_grades(self):
        """Afficher la page notes"""
        if isinstance(self.current_page, GradesPage):
            return
        
        self.clear_content()
        self.reset_button_colors()
        self.grades_button.configure(fg_color=["#2B7DC0", "#164A75"])
        
        self.current_page = GradesPage(self.content_frame, self.pronote_client)
        self.current_page.pack(fill="both", expand=True)
        
        logger.info("Page notes affichée")
    
    def show_homework(self):
        """Afficher la page devoirs"""
        if isinstance(self.current_page, HomeworkPage):
            return
        
        self.clear_content()
        self.reset_button_colors()
        self.homework_button.configure(fg_color=["#2B7DC0", "#164A75"])
        
        self.current_page = HomeworkPage(self.content_frame, self.pronote_client)
        self.current_page.pack(fill="both", expand=True)
        
        logger.info("Page devoirs affichée")
    
    def show_messages(self):
        """Afficher la page messages"""
        if isinstance(self.current_page, MessagesPage):
            return
        
        self.clear_content()
        self.reset_button_colors()
        self.messages_button.configure(fg_color=["#2B7DC0", "#164A75"])
        
        self.current_page = MessagesPage(self.content_frame, self.pronote_client)
        self.current_page.pack(fill="both", expand=True)
        
        logger.info("Page messages affichée")
    
    def toggle_theme(self):
        """Basculer le thème"""
        new_theme = self.theme_manager.toggle_theme()
        
        # Mettre à jour le texte du bouton
        if new_theme == "dark":
            self.theme_button.configure(text="🌙 Mode sombre")
        else:
            self.theme_button.configure(text="☀️ Mode clair")
        
        logger.info(f"Thème changé: {new_theme}")
    
    def logout(self):
        """Déconnexion"""
        from tkinter import messagebox
        
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            logger.info("Déconnexion demandée")
            self.pronote_client.logout()
            
            # Fermer l'application proprement
            self.quit()
            self.destroy()
