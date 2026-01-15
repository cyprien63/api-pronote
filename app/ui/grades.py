"""
Page des notes
"""
import customtkinter as ctk
from typing import Dict, List, Any
import logging

from app.pronote_api.client import PronoteClient
from app.utils.export import DataExporter
from tkinter import filedialog, messagebox

logger = logging.getLogger(__name__)


class GradesPage(ctk.CTkScrollableFrame):
    """Page d'affichage des notes"""
    
    def __init__(self, parent, pronote_client: PronoteClient):
        super().__init__(parent, fg_color="transparent")
        
        self.pronote_client = pronote_client
        self.grades_data = {}
        self.current_period_index = 0
        
        self.create_widgets()
        self.load_grades()
    
    def create_widgets(self):
        """Créer les widgets de la page"""
        
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Notes",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Bouton export
        export_button = ctk.CTkButton(
            header_frame,
            text="📥 Exporter CSV",
            command=self.export_grades,
            width=130,
            font=ctk.CTkFont(size=12)
        )
        export_button.pack(side="right", padx=5)
        
        # Sélecteur de période
        self.period_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.period_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        period_label = ctk.CTkLabel(
            self.period_frame,
            text="Période:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        period_label.pack(side="left", padx=(0, 10))
        
        self.period_selector = ctk.CTkSegmentedButton(
            self.period_frame,
            values=[],
            command=self.on_period_changed,
            font=ctk.CTkFont(size=13)
        )
        self.period_selector.pack(side="left", fill="x", expand=True)
        
        # Zone de contenu
        self.grades_container = ctk.CTkFrame(self)
        self.grades_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def load_grades(self):
        """Charger les notes"""
        try:
            self.grades_data = self.pronote_client.get_grades()
            
            periods = self.grades_data.get("periods", [])
            
            if not periods:
                no_data_label = ctk.CTkLabel(
                    self.grades_container,
                    text="Aucune note disponible",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
                return
            
            # Mettre à jour le sélecteur de période
            period_names = [p["name"] for p in periods]
            self.period_selector.configure(values=period_names)
            
            # Sélectionner la première période
            if period_names:
                self.period_selector.set(period_names[0])
                self.display_period_grades(periods[0])
        
        except Exception as e:
            logger.error(f"Erreur chargement notes: {e}")
            error_label = ctk.CTkLabel(
                self.grades_container,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def on_period_changed(self, period_name: str):
        """Gérer le changement de période"""
        # Nettoyer le conteneur
        for widget in self.grades_container.winfo_children():
            widget.destroy()
        
        # Trouver la période correspondante
        periods = self.grades_data.get("periods", [])
        for period in periods:
            if period["name"] == period_name:
                self.display_period_grades(period)
                break
    
    def display_period_grades(self, period: Dict[str, Any]):
        """Afficher les notes d'une période"""
        grades = period.get("grades", [])
        
        if not grades:
            no_grades_label = ctk.CTkLabel(
                self.grades_container,
                text="Aucune note pour cette période",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_grades_label.pack(pady=50)
            return
        
        # Organiser par matière
        grades_by_subject = {}
        for grade in grades:
            subject = grade["subject"]
            if subject not in grades_by_subject:
                grades_by_subject[subject] = []
            grades_by_subject[subject].append(grade)
        
        # Afficher par matière
        for subject, subject_grades in grades_by_subject.items():
            self.create_subject_card(subject, subject_grades)
    
    def create_subject_card(self, subject: str, grades: List[Dict[str, Any]]):
        """Créer une carte pour une matière"""
        
        # Carte de la matière
        card = ctk.CTkFrame(self.grades_container)
        card.pack(fill="x", pady=10, padx=10)
        
        # En-tête de la matière
        header = ctk.CTkFrame(card, fg_color=["#D0D0D0", "#3B3B3B"])
        header.pack(fill="x", padx=5, pady=5)
        
        subject_label = ctk.CTkLabel(
            header,
            text=subject,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subject_label.pack(side="left", padx=15, pady=10)
        
        # Calculer la moyenne
        total_points = 0
        total_coef = 0
        
        for grade in grades:
            try:
                grade_value = float(grade["grade"])
                out_of = float(grade["out_of"])
                coef = float(grade.get("coefficient", 1))
                
                # Convertir sur 20
                grade_on_20 = (grade_value / out_of) * 20
                total_points += grade_on_20 * coef
                total_coef += coef
            except (ValueError, ZeroDivisionError):
                pass
        
        if total_coef > 0:
            average = total_points / total_coef
            avg_label = ctk.CTkLabel(
                header,
                text=f"Moyenne: {average:.2f}/20",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=["#2B7DC0", "#4A9FD8"]
            )
            avg_label.pack(side="right", padx=15, pady=10)
        
        # Liste des notes
        for grade in grades:
            self.create_grade_row(card, grade)
    
    def create_grade_row(self, parent, grade: Dict[str, Any]):
        """Créer une ligne pour une note"""
        
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)
        
        # Note
        grade_text = f"{grade['grade']}/{grade['out_of']}"
        grade_label = ctk.CTkLabel(
            row,
            text=grade_text,
            font=ctk.CTkFont(size=15, weight="bold"),
            width=80
        )
        grade_label.pack(side="left", padx=(0, 15))
        
        # Coefficient
        coef = grade.get("coefficient", 1)
        coef_label = ctk.CTkLabel(
            row,
            text=f"Coef. {coef}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            width=70
        )
        coef_label.pack(side="left", padx=(0, 15))
        
        # Date
        date_str = str(grade.get("date", ""))
        if date_str:
            date_label = ctk.CTkLabel(
                row,
                text=date_str,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            date_label.pack(side="right")
    
    def export_grades(self):
        """Exporter les notes en CSV"""
        if not self.grades_data:
            messagebox.showerror("Erreur", "Aucune note à exporter")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="notes_pronote.csv"
        )
        
        if filepath:
            from pathlib import Path
            success = DataExporter.export_grades_to_csv(self.grades_data, Path(filepath))
            
            if success:
                messagebox.showinfo("Succès", f"Notes exportées avec succès vers:\n{filepath}")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'export")
