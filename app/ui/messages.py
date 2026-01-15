"""
Page de messagerie
"""
import customtkinter as ctk
from typing import List, Dict, Any
import logging

from app.pronote_api.client import PronoteClient

logger = logging.getLogger(__name__)


class MessagesPage(ctk.CTkScrollableFrame):
    """Page d'affichage de la messagerie"""
    
    def __init__(self, parent, pronote_client: PronoteClient):
        super().__init__(parent, fg_color="transparent")
        
        self.pronote_client = pronote_client
        self.messages_data = []
        
        self.create_widgets()
        self.load_messages()
    
    def create_widgets(self):
        """Créer les widgets de la page"""
        
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="✉️ Messages",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Bouton rafraîchir
        refresh_button = ctk.CTkButton(
            header_frame,
            text="🔄 Rafraîchir",
            command=self.load_messages,
            width=120,
            font=ctk.CTkFont(size=12)
        )
        refresh_button.pack(side="right")
        
        # Zone de contenu
        self.messages_container = ctk.CTkFrame(self)
        self.messages_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def load_messages(self):
        """Charger les messages"""
        # Nettoyer le conteneur
        for widget in self.messages_container.winfo_children():
            widget.destroy()
        
        try:
            self.messages_data = self.pronote_client.get_messages()
            
            if not self.messages_data:
                # Message informatif
                info_frame = ctk.CTkFrame(self.messages_container)
                info_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                icon_label = ctk.CTkLabel(
                    info_frame,
                    text="📬",
                    font=ctk.CTkFont(size=64)
                )
                icon_label.pack(pady=(40, 20))
                
                title_label = ctk.CTkLabel(
                    info_frame,
                    text="Messagerie",
                    font=ctk.CTkFont(size=20, weight="bold")
                )
                title_label.pack(pady=10)
                
                desc_label = ctk.CTkLabel(
                    info_frame,
                    text="La fonctionnalité de messagerie n'est pas encore disponible\nou aucun message n'a été trouvé.",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                desc_label.pack(pady=10)
                
                note_label = ctk.CTkLabel(
                    info_frame,
                    text="Note: L'accès à la messagerie dépend de la version de Pronote\net des permissions de votre établissement.",
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    wraplength=500
                )
                note_label.pack(pady=(20, 40))
                
                return
            
            # Afficher les messages
            for message in self.messages_data:
                self.create_message_card(message)
        
        except Exception as e:
            logger.error(f"Erreur chargement messages: {e}")
            error_label = ctk.CTkLabel(
                self.messages_container,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def create_message_card(self, message: Dict[str, Any]):
        """Créer une carte pour un message"""
        
        # Carte du message
        card = ctk.CTkFrame(self.messages_container)
        card.pack(fill="x", pady=10, padx=10)
        
        # Frame interne
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Indicateur non lu
        if not message.get("seen", True):
            indicator = ctk.CTkFrame(
                content_frame,
                width=8,
                height=8,
                corner_radius=4,
                fg_color="#3B82F6"
            )
            indicator.pack(side="left", padx=(0, 10))
        
        # Infos du message
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Auteur
        author = message.get("author", "Expéditeur inconnu")
        author_label = ctk.CTkLabel(
            info_frame,
            text=author,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        author_label.pack(anchor="w")
        
        # Contenu
        content = message.get("content", "Pas de contenu")
        if len(content) > 200:
            content = content[:200] + "..."
        
        content_label = ctk.CTkLabel(
            info_frame,
            text=content,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
            wraplength=700
        )
        content_label.pack(anchor="w", pady=(5, 0))
        
        # Date
        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.pack(side="right", padx=(10, 0))
        
        created = message.get("created", "")
        if created:
            date_label = ctk.CTkLabel(
                date_frame,
                text=str(created),
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            date_label.pack()
