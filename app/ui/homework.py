"""
Page des devoirs
"""
import customtkinter as ctk
import datetime
from typing import List, Dict, Any
import logging

from app.pronote_api.client import PronoteClient
from tkinter import messagebox

logger = logging.getLogger(__name__)


class HomeworkPage(ctk.CTkScrollableFrame):
    """Page d'affichage des devoirs"""
    
    def __init__(self, parent, pronote_client: PronoteClient):
        super().__init__(parent, fg_color="transparent")
        
        self.pronote_client = pronote_client
        self.current_filter = "all"  # all, todo, done
        self.homework_data = []
        
        self.create_widgets()
        self.load_homework()
    
    def create_widgets(self):
        """Créer les widgets de la page"""
        
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📝 Devoirs",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Filtres
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Afficher:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        self.filter_selector = ctk.CTkSegmentedButton(
            filter_frame,
            values=["Tous", "À faire", "Terminés"],
            command=self.on_filter_changed,
            font=ctk.CTkFont(size=13)
        )
        self.filter_selector.pack(side="left")
        self.filter_selector.set("Tous")
        
        # Bouton rafraîchir
        refresh_button = ctk.CTkButton(
            filter_frame,
            text="🔄 Rafraîchir",
            command=self.load_homework,
            width=120,
            font=ctk.CTkFont(size=12)
        )
        refresh_button.pack(side="right")
        
        # Zone de contenu
        self.homework_container = ctk.CTkFrame(self)
        self.homework_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def load_homework(self):
        """Charger les devoirs"""
        # Nettoyer le conteneur
        for widget in self.homework_container.winfo_children():
            widget.destroy()
        
        try:
            # Récupérer les devoirs à partir d'aujourd'hui
            today = datetime.date.today()
            self.homework_data = self.pronote_client.get_homework(today)
            
            if not self.homework_data:
                no_data_label = ctk.CTkLabel(
                    self.homework_container,
                    text="Aucun devoir à venir",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
                return
            
            # Appliquer le filtre
            self.apply_filter()
        
        except Exception as e:
            logger.error(f"Erreur chargement devoirs: {e}")
            error_label = ctk.CTkLabel(
                self.homework_container,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def on_filter_changed(self, filter_name: str):
        """Gérer le changement de filtre"""
        filter_map = {
            "Tous": "all",
            "À faire": "todo",
            "Terminés": "done"
        }
        
        self.current_filter = filter_map.get(filter_name, "all")
        self.apply_filter()
    
    def apply_filter(self):
        """Appliquer le filtre actuel"""
        # Nettoyer le conteneur
        for widget in self.homework_container.winfo_children():
            widget.destroy()
        
        # Filtrer les devoirs
        filtered_homework = []
        
        for hw in self.homework_data:
            if self.current_filter == "all":
                filtered_homework.append(hw)
            elif self.current_filter == "todo" and not hw.get("done", False):
                filtered_homework.append(hw)
            elif self.current_filter == "done" and hw.get("done", False):
                filtered_homework.append(hw)
        
        if not filtered_homework:
            no_data_label = ctk.CTkLabel(
                self.homework_container,
                text="Aucun devoir dans cette catégorie",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
            return
        
        # Organiser par date
        homework_by_date = {}
        for hw in filtered_homework:
            date = hw.get("date")
            if isinstance(date, datetime.datetime):
                date = date.date()
            elif isinstance(date, str):
                try:
                    date = datetime.datetime.fromisoformat(date).date()
                except:
                    date = None
            
            if date:
                if date not in homework_by_date:
                    homework_by_date[date] = []
                homework_by_date[date].append(hw)
        
        # Trier par date
        sorted_dates = sorted(homework_by_date.keys())
        
        # Afficher par date
        for date in sorted_dates:
            self.create_date_section(date, homework_by_date[date])
    
    def create_date_section(self, date: datetime.date, homework_list: List[Dict[str, Any]]):
        """Créer une section pour une date"""
        
        # Frame de la date
        date_frame = ctk.CTkFrame(self.homework_container)
        date_frame.pack(fill="x", pady=10, padx=10)
        
        # En-tête de la date
        today = datetime.date.today()
        days_until = (date - today).days
        
        if days_until == 0:
            date_text = f"Aujourd'hui - {date.strftime('%d/%m/%Y')}"
            color = "red"
        elif days_until == 1:
            date_text = f"Demain - {date.strftime('%d/%m/%Y')}"
            color = "orange"
        elif days_until < 0:
            date_text = f"Passé - {date.strftime('%d/%m/%Y')}"
            color = "gray"
        else:
            date_text = f"Dans {days_until} jours - {date.strftime('%d/%m/%Y')}"
            color = "green"
        
        header = ctk.CTkFrame(date_frame, fg_color=["#E0E0E0", "#2B2B2B"])
        header.pack(fill="x", padx=5, pady=5)
        
        date_label = ctk.CTkLabel(
            header,
            text=date_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color
        )
        date_label.pack(side="left", padx=15, pady=10)
        
        count_label = ctk.CTkLabel(
            header,
            text=f"{len(homework_list)} devoir{'s' if len(homework_list) > 1 else ''}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        count_label.pack(side="right", padx=15, pady=10)
        
        # Devoirs
        for hw in homework_list:
            self.create_homework_card(date_frame, hw)
    
    def create_homework_card(self, parent, homework: Dict[str, Any]):
        """Créer une carte pour un devoir"""
        
        # Carte
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=10, pady=5)
        
        # Frame interne
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Checkbox "fait"
        done_var = ctk.BooleanVar(value=homework.get("done", False))
        
        checkbox = ctk.CTkCheckBox(
            content_frame,
            text="",
            variable=done_var,
            width=30,
            command=lambda: self.toggle_homework_done(homework, done_var.get())
        )
        checkbox.pack(side="left", padx=(0, 15))
        
        # Infos du devoir
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Matière
        subject = homework.get("subject", "Matière inconnue")
        subject_label = ctk.CTkLabel(
            info_frame,
            text=subject,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        subject_label.pack(anchor="w")
        
        # Description
        description = homework.get("description", "Pas de description")
        # Limiter la longueur de la description
        if len(description) > 150:
            description = description[:150] + "..."
        
        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
            wraplength=600
        )
        desc_label.pack(anchor="w", pady=(5, 0))
    
    def toggle_homework_done(self, homework: Dict[str, Any], done: bool):
        """Marquer un devoir comme fait/non fait"""
        # Note: pronotepy ne supporte pas forcément la modification de l'état "done"
        # Ceci est une fonctionnalité locale pour l'instant
        homework["done"] = done
        logger.info(f"Devoir {homework.get('subject', '')} marqué comme {'fait' if done else 'non fait'}")
