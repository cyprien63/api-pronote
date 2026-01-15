"""
Page emploi du temps
"""
import customtkinter as ctk
import datetime
from typing import List, Dict, Any
import logging

from app.pronote_api.client import PronoteClient
from app.config import SUBJECT_COLORS

logger = logging.getLogger(__name__)


class SchedulePage(ctk.CTkScrollableFrame):
    """Page d'affichage de l'emploi du temps"""
    
    def __init__(self, parent, pronote_client: PronoteClient):
        super().__init__(parent, fg_color="transparent")
        
        self.pronote_client = pronote_client
        self.current_week_offset = 0  # 0 = semaine actuelle, -1 = précédente, +1 = suivante
        
        self.create_widgets()
        self.load_schedule()
    
    def create_widgets(self):
        """Créer les widgets de la page"""
        
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📅 Emploi du temps",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Navigation semaine
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(side="right")
        
        prev_button = ctk.CTkButton(
            nav_frame,
            text="◀ Semaine précédente",
            command=self.prev_week,
            width=150,
            font=ctk.CTkFont(size=12)
        )
        prev_button.pack(side="left", padx=5)
        
        self.week_label = ctk.CTkLabel(
            nav_frame,
            text="Semaine actuelle",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.week_label.pack(side="left", padx=15)
        
        next_button = ctk.CTkButton(
            nav_frame,
            text="Semaine suivante ▶",
            command=self.next_week,
            width=150,
            font=ctk.CTkFont(size=12)
        )
        next_button.pack(side="left", padx=5)
        
        # Zone de contenu
        self.schedule_container = ctk.CTkFrame(self)
        self.schedule_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def get_week_dates(self) -> tuple[datetime.date, datetime.date]:
        """Obtenir les dates de début et fin de la semaine"""
        today = datetime.date.today()
        # Calculer le lundi de la semaine
        monday = today - datetime.timedelta(days=today.weekday())
        # Appliquer l'offset
        monday = monday + datetime.timedelta(weeks=self.current_week_offset)
        # Dimanche
        sunday = monday + datetime.timedelta(days=6)
        
        return monday, sunday
    
    def prev_week(self):
        """Semaine précédente"""
        self.current_week_offset -= 1
        self.load_schedule()
    
    def next_week(self):
        """Semaine suivante"""
        self.current_week_offset += 1
        self.load_schedule()
    
    def load_schedule(self):
        """Charger l'emploi du temps"""
        # Nettoyer le conteneur
        for widget in self.schedule_container.winfo_children():
            widget.destroy()
        
        # Obtenir les dates
        monday, sunday = self.get_week_dates()
        
        # Mettre à jour le label de semaine
        if self.current_week_offset == 0:
            week_text = "Semaine actuelle"
        elif self.current_week_offset == -1:
            week_text = "Semaine précédente"
        elif self.current_week_offset == 1:
            week_text = "Semaine suivante"
        else:
            week_text = f"Semaine du {monday.strftime('%d/%m/%Y')}"
        
        self.week_label.configure(text=week_text)
        
        # Récupérer l'emploi du temps
        try:
            lessons = self.pronote_client.get_schedule(monday, sunday)
            
            if not lessons:
                no_data_label = ctk.CTkLabel(
                    self.schedule_container,
                    text="Aucun cours pour cette semaine",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
                return
            
            # Organiser par jour
            lessons_by_day = self.organize_by_day(lessons, monday)
            
            # Afficher par jour
            for day_offset in range(7):
                day_date = monday + datetime.timedelta(days=day_offset)
                day_name = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][day_offset]
                
                day_lessons = lessons_by_day.get(day_date, [])
                
                if day_lessons or day_offset < 5:  # Afficher les jours de semaine même sans cours
                    self.create_day_section(day_name, day_date, day_lessons)
        
        except Exception as e:
            logger.error(f"Erreur chargement emploi du temps: {e}")
            error_label = ctk.CTkLabel(
                self.schedule_container,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def organize_by_day(self, lessons: List[Dict[str, Any]], monday: datetime.date) -> Dict[datetime.date, List[Dict[str, Any]]]:
        """Organiser les cours par jour"""
        by_day = {}
        
        for lesson in lessons:
            start = lesson["start"]
            if isinstance(start, datetime.datetime):
                day = start.date()
            else:
                day = start
            
            if day not in by_day:
                by_day[day] = []
            by_day[day].append(lesson)
        
        # Trier les cours de chaque jour par heure
        for day in by_day:
            by_day[day].sort(key=lambda l: l["start"])
        
        return by_day
    
    def create_day_section(self, day_name: str, day_date: datetime.date, lessons: List[Dict[str, Any]]):
        """Créer une section pour un jour"""
        
        # Frame du jour
        day_frame = ctk.CTkFrame(self.schedule_container)
        day_frame.pack(fill="x", pady=10, padx=10)
        
        # En-tête du jour
        header = ctk.CTkFrame(day_frame, fg_color=["#E0E0E0", "#2B2B2B"])
        header.pack(fill="x", padx=5, pady=5)
        
        day_label = ctk.CTkLabel(
            header,
            text=f"{day_name} {day_date.strftime('%d/%m')}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        day_label.pack(side="left", padx=15, pady=10)
        
        count_label = ctk.CTkLabel(
            header,
            text=f"{len(lessons)} cours",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        count_label.pack(side="right", padx=15, pady=10)
        
        # Cours du jour
        if lessons:
            for lesson in lessons:
                self.create_lesson_card(day_frame, lesson)
        else:
            no_lesson_label = ctk.CTkLabel(
                day_frame,
                text="Aucun cours",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            )
            no_lesson_label.pack(pady=15)
    
    def create_lesson_card(self, parent, lesson: Dict[str, Any]):
        """Créer une carte pour un cours"""
        
        # Couleur basée sur la matière
        subject = lesson.get("subject", "")
        color = SUBJECT_COLORS.get(subject, SUBJECT_COLORS["default"])
        
        # Carte
        card = ctk.CTkFrame(parent, border_width=2, border_color=color)
        card.pack(fill="x", padx=10, pady=5)
        
        # Frame interne
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Barre colorée à gauche (visual indicator)
        color_bar = ctk.CTkFrame(content_frame, width=4, fg_color=color)
        color_bar.pack(side="left", fill="y", padx=(0, 15))
        
        # Infos du cours
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Matière
        subject_label = ctk.CTkLabel(
            info_frame,
            text=subject,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        subject_label.pack(anchor="w")
        
        # Détails
        start = lesson["start"]
        end = lesson["end"]
        
        if isinstance(start, datetime.datetime):
            time_str = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        else:
            time_str = "Horaire non disponible"
        
        teacher = lesson.get("teacher", "")
        classroom = lesson.get("classroom", "")
        
        details = []
        if time_str:
            details.append(f"⏰ {time_str}")
        if teacher:
            details.append(f"👨‍🏫 {teacher}")
        if classroom:
            details.append(f"📍 {classroom}")
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=" • ".join(details),
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        details_label.pack(anchor="w", pady=(5, 0))
