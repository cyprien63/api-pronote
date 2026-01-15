"""
Fenêtre de connexion à Pronote
"""
import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path
import logging
from typing import Callable, Optional

from app.config import CREDENTIALS_FILE, COMMON_PRONOTE_URLS, APP_NAME

logger = logging.getLogger(__name__)


class LoginWindow(ctk.CTk):
    """Fenêtre de connexion"""
    
    def __init__(self, on_login_success: Callable):
        super().__init__()
        
        self.on_login_success = on_login_success
        self.loading = False
        
        # Configuration de la fenêtre
        self.title(f"{APP_NAME} - Connexion")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer l'interface
        self.create_widgets()
        
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Créer les widgets de l'interface"""
        
        # Frame principal avec padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo / Titre
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎓 Pronote Amélioré",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Connectez-vous à votre compte Pronote",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # URL Pronote
        url_header_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        url_header_frame.pack(fill="x", padx=20, pady=(20, 5))
        
        url_label = ctk.CTkLabel(
            url_header_frame,
            text="URL Pronote",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        url_label.pack(side="left")
        
        # Bouton d'aide
        help_button = ctk.CTkButton(
            url_header_frame,
            text="❓ Comment trouver mon URL ?",
            command=self.show_url_help,
            width=180,
            height=25,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            text_color=["#3B8ED0", "#4A9FD8"],
            hover_color=["#E0E0E0", "#2B2B2B"]
        )
        help_button.pack(side="right")
        
        self.url_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="https://votre-etablissement.index-education.net/pronote/eleve.html",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Nom d'utilisateur
        username_label = ctk.CTkLabel(
            form_frame,
            text="Nom d'utilisateur",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", padx=20, pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Votre nom d'utilisateur",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.username_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Mot de passe
        password_label = ctk.CTkLabel(
            form_frame,
            text="Mot de passe",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", padx=20, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Votre mot de passe",
            show="●",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.password_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Case "Se souvenir de moi"
        self.remember_var = ctk.BooleanVar(value=True)
        remember_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Se souvenir de moi",
            variable=self.remember_var,
            font=ctk.CTkFont(size=12)
        )
        remember_checkbox.pack(padx=20, pady=(0, 20))
        
        # Bouton de connexion
        self.login_button = ctk.CTkButton(
            form_frame,
            text="Se connecter",
            command=self.login,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.login_button.pack(fill="x", padx=20, pady=(0, 20))
        
        # Label de chargement
        self.loading_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.loading_label.pack(pady=(0, 10))
        
        # Charger les credentials sauvegardés si disponibles
        self.load_saved_credentials()
    
    def load_saved_credentials(self):
        """Charger les credentials sauvegardés"""
        if CREDENTIALS_FILE.exists():
            try:
                with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
                    creds = json.load(f)
                    
                # Si on a des credentials sauvegardés, remplir les champs
                if creds.get("username") and creds.get("url"):
                    url = creds["url"]
                    # Nettoyer l'URL des paramètres (?identifiant=...)
                    if '?' in url:
                        url = url.split('?')[0]
                    
                    self.url_entry.delete(0, 'end')
                    self.url_entry.insert(0, url)
                    self.username_entry.insert(0, creds["username"])
                    logger.info("Credentials sauvegardés chargés")
                    
            except Exception as e:
                logger.error(f"Erreur chargement credentials: {e}")
    
    def login(self):
        """Gérer la connexion"""
        if self.loading:
            return
        
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Nettoyer l'URL des paramètres (?identifiant=...)
        if '?' in url:
            url = url.split('?')[0]
            logger.info(f"URL nettoyée: {url}")
        
        # Validation
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer l'URL Pronote")
            return
        
        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer votre nom d'utilisateur")
            return
        
        if not password:
            messagebox.showerror("Erreur", "Veuillez entrer votre mot de passe")
            return
        
        # Afficher le chargement
        self.loading = True
        self.login_button.configure(state="disabled", text="Connexion en cours...")
        self.loading_label.configure(text="⏳ Connexion à Pronote en cours...")
        self.update()
        
        # Appeler le callback de connexion
        try:
            credentials = {
                "url": url,
                "username": username,
                "password": password,
                "remember": self.remember_var.get()
            }
            
            # Le callback retournera True si la connexion est réussie
            self.on_login_success(credentials)
            
        except Exception as e:
            logger.error(f"Erreur lors de la connexion: {e}")
            self.loading = False
            self.login_button.configure(state="normal", text="Se connecter")
            self.loading_label.configure(text="")
            messagebox.showerror("Erreur", f"Erreur lors de la connexion: {str(e)}")
    
    def reset_loading_state(self):
        """Réinitialiser l'état de chargement"""
        self.loading = False
        self.login_button.configure(state="normal", text="Se connecter")
        self.loading_label.configure(text="")
    
    def show_url_help(self):
        """Afficher l'aide pour trouver l'URL Pronote"""
        import webbrowser
        
        # Créer une fenêtre d'aide
        help_window = ctk.CTkToplevel(self)
        help_window.title("Comment trouver mon URL Pronote ?")
        help_window.geometry("600x500")
        help_window.resizable(False, False)
        
        # Centrer la fenêtre
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f'600x500+{x}+{y}')
        
        # Contenu avec scroll
        main_frame = ctk.CTkScrollableFrame(help_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title = ctk.CTkLabel(
            main_frame,
            text="🔍 Trouver votre URL Pronote",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Méthode 1
        method1_label = ctk.CTkLabel(
            main_frame,
            text="📝 Méthode 1 : Demander à votre établissement",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        method1_label.pack(fill="x", pady=(0, 10))
        
        method1_text = ctk.CTkLabel(
            main_frame,
            text="• Demandez l'URL Pronote à votre professeur principal\n"
                 "• Ou consultez l'ENT (Espace Numérique de Travail) de votre établissement\n"
                 "• L'URL se termine généralement par /pronote/eleve.html",
            font=ctk.CTkFont(size=12),
            anchor="w",
            justify="left"
        )
        method1_text.pack(fill="x", pady=(0, 20))
        
        # Méthode 2
        method2_label = ctk.CTkLabel(
            main_frame,
            text="🌐 Méthode 2 : Rechercher sur internet",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        method2_label.pack(fill="x", pady=(0, 10))
        
        method2_text = ctk.CTkLabel(
            main_frame,
            text="Recherchez sur Google :",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        method2_text.pack(fill="x", pady=(0, 10))
        
        # Zone de saisie pour le nom d'établissement
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nom de votre établissement + ville",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        def search_pronote():
            etablissement = search_entry.get().strip()
            if etablissement:
                search_query = f"pronote {etablissement}"
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(url)
        
        search_button = ctk.CTkButton(
            search_frame,
            text="🔍 Rechercher",
            command=search_pronote,
            width=120,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        search_button.pack(side="right", padx=(5, 10), pady=10)
        
        # Méthode 3
        method3_label = ctk.CTkLabel(
            main_frame,
            text="📱 Méthode 3 : Depuis l'application mobile",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        method3_label.pack(fill="x", pady=(10, 10))
        
        method3_text = ctk.CTkLabel(
            main_frame,
            text="Si vous avez l'application Pronote sur votre téléphone :\n"
                 "• L'URL s'affiche lors de la configuration initiale\n"
                 "• Vous pouvez la retrouver dans les paramètres de l'app",
            font=ctk.CTkFont(size=12),
            anchor="w",
            justify="left"
        )
        method3_text.pack(fill="x", pady=(0, 20))
        
        # Exemple
        example_label = ctk.CTkLabel(
            main_frame,
            text="💡 Exemples d'URL Pronote :",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        example_label.pack(fill="x", pady=(10, 10))
        
        examples_frame = ctk.CTkFrame(main_frame, fg_color=["#E0E0E0", "#2B2B2B"])
        examples_frame.pack(fill="x", pady=(0, 10))
        
        examples = [
            "https://0061234a.index-education.net/pronote/eleve.html",
            "https://demo.index-education.net/pronote/eleve.html",
            "https://lycee-exemple.index-education.net/pronote/eleve.html"
        ]
        
        for example in examples:
            ex_label = ctk.CTkLabel(
                examples_frame,
                text=f"• {example}",
                font=ctk.CTkFont(size=11, family="Courier"),
                anchor="w"
            )
            ex_label.pack(fill="x", padx=15, pady=5)
        
        # Note importante
        note_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ Important : L'URL doit se terminer par /eleve.html",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=["#f59e0b", "#fbbf24"],
            anchor="w"
        )
        note_label.pack(fill="x", pady=(10, 5))
        
        # Note sur les paramètres
        param_note = ctk.CTkLabel(
            main_frame,
            text="Si votre URL contient '?identifiant=...', supprimez cette partie.\n"
                 "L'application le fera automatiquement pour vous.",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w",
            justify="left"
        )
        param_note.pack(fill="x", pady=(0, 0))
        
        # Bouton fermer
        close_button = ctk.CTkButton(
            help_window,
            text="Fermer",
            command=help_window.destroy,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        close_button.pack(side="bottom", pady=20, padx=20, fill="x")

