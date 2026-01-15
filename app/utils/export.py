"""
Fonctions d'export de données
"""
import csv
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Exportateur de données vers différents formats"""
    
    @staticmethod
    def export_to_json(data: Any, filepath: Path) -> bool:
        """
        Exporter des données vers JSON
        
        Args:
            data: Données à exporter
            filepath: Chemin du fichier
            
        Returns:
            True si succès, False sinon
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"Export JSON réussi: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erreur export JSON: {e}")
            return False
    
    @staticmethod
    def export_grades_to_csv(grades_data: Dict[str, Any], filepath: Path) -> bool:
        """
        Exporter les notes vers CSV
        
        Args:
            grades_data: Données des notes
            filepath: Chemin du fichier
            
        Returns:
            True si succès, False sinon
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                # En-têtes
                writer.writerow(['Période', 'Matière', 'Note', 'Sur', 'Coefficient', 'Date'])
                
                # Données
                for period in grades_data.get("periods", []):
                    period_name = period.get("name", "")
                    for grade in period.get("grades", []):
                        writer.writerow([
                            period_name,
                            grade.get("subject", ""),
                            grade.get("grade", ""),
                            grade.get("out_of", ""),
                            grade.get("coefficient", "1"),
                            grade.get("date", ""),
                        ])
            
            logger.info(f"Export CSV notes réussi: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur export CSV notes: {e}")
            return False
    
    @staticmethod
    def export_homework_to_csv(homework_data: List[Dict[str, Any]], filepath: Path) -> bool:
        """
        Exporter les devoirs vers CSV
        
        Args:
            homework_data: Données des devoirs
            filepath: Chemin du fichier
            
        Returns:
            True si succès, False sinon
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                # En-têtes
                writer.writerow(['Matière', 'Description', 'Date', 'Fait'])
                
                # Données
                for hw in homework_data:
                    writer.writerow([
                        hw.get("subject", ""),
                        hw.get("description", ""),
                        hw.get("date", ""),
                        "Oui" if hw.get("done", False) else "Non",
                    ])
            
            logger.info(f"Export CSV devoirs réussi: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur export CSV devoirs: {e}")
            return False
