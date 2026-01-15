"""
Client Pronote - Wrapper autour de pronotepy
"""
import pronotepy
import datetime
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PronoteClient:
    """Wrapper pour gérer la connexion et les requêtes à Pronote"""
    
    def __init__(self):
        self.client: Optional[pronotepy.Client] = None
        self.logged_in = False
        
    def login(self, url: str, username: str, password: str) -> tuple[bool, str]:
        """
        Se connecter à Pronote
        
        Args:
            url: URL de Pronote
            username: Nom d'utilisateur
            password: Mot de passe
            
        Returns:
            (succès, message)
        """
        try:
            self.client = pronotepy.Client(url, username=username, password=password)
            
            if self.client.logged_in:
                self.logged_in = True
                logger.info(f"Connexion réussie pour {username}")
                return True, "Connexion réussie"
            else:
                self.logged_in = False
                return False, "Échec de la connexion. Vérifiez vos identifiants."
                
        except Exception as e:
            error_str = str(e)
            logger.error(f"Erreur de connexion: {e}")
            self.logged_in = False
            
            # Messages d'erreur plus clairs
            if "bad decryption" in error_str.lower() or "bad username/password" in error_str.lower():
                return False, "Identifiants incorrects. Vérifiez votre nom d'utilisateur et mot de passe."
            elif "connection" in error_str.lower() or "network" in error_str.lower():
                return False, "Impossible de se connecter au serveur Pronote. Vérifiez votre connexion internet."
            elif "url" in error_str.lower():
                return False, "URL Pronote invalide. Vérifiez l'adresse (elle doit se terminer par /eleve.html)."
            else:
                return False, f"Erreur de connexion: {error_str}"
    
    def login_with_token(self, credentials: Dict[str, Any]) -> tuple[bool, str]:
        """
        Se connecter avec des credentials sauvegardés
        
        Args:
            credentials: Dictionnaire de credentials exportés
            
        Returns:
            (succès, message)
        """
        try:
            self.client = pronotepy.Client.token_login(**credentials)
            
            if self.client.logged_in:
                self.logged_in = True
                logger.info("Connexion par token réussie")
                return True, "Connexion réussie"
            else:
                self.logged_in = False
                return False, "Token expiré. Veuillez vous reconnecter."
                
        except Exception as e:
            logger.error(f"Erreur de connexion par token: {e}")
            self.logged_in = False
            return False, f"Erreur: {str(e)}"
    
    def export_credentials(self) -> Optional[Dict[str, Any]]:
        """Exporter les credentials pour réutilisation"""
        if self.client and self.logged_in:
            try:
                return self.client.export_credentials()
            except Exception as e:
                logger.error(f"Erreur export credentials: {e}")
                return None
        return None
    
    def check_session(self) -> bool:
        """Vérifier et rafraîchir la session si nécessaire"""
        if self.client and self.logged_in:
            try:
                return self.client.session_check()
            except Exception as e:
                logger.error(f"Erreur vérification session: {e}")
                return False
        return False
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Récupérer les informations de l'utilisateur"""
        if not self.client or not self.logged_in:
            return None
            
        try:
            self.check_session()
            return {
                "name": self.client.info.name,
                "start_day": self.client.start_day,
            }
        except Exception as e:
            logger.error(f"Erreur récupération infos utilisateur: {e}")
            return None
    
    def get_schedule(self, date_from: datetime.date, date_to: datetime.date) -> List[Dict[str, Any]]:
        """
        Récupérer l'emploi du temps
        
        Args:
            date_from: Date de début
            date_to: Date de fin
            
        Returns:
            Liste des cours
        """
        if not self.client or not self.logged_in:
            return []
            
        try:
            self.check_session()
            lessons = self.client.lessons(date_from, date_to)
            
            result = []
            for lesson in lessons:
                result.append({
                    "id": lesson.id,
                    "subject": lesson.subject.name if lesson.subject else "Aucune matière",
                    "teacher": lesson.teacher_name if hasattr(lesson, 'teacher_name') else "",
                    "classroom": lesson.classroom if hasattr(lesson, 'classroom') else "",
                    "start": lesson.start,
                    "end": lesson.end,
                    "status": lesson.status if hasattr(lesson, 'status') else "",
                    "background_color": lesson.background_color if hasattr(lesson, 'background_color') else "#6b7280",
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur récupération emploi du temps: {e}")
            return []
    
    def get_homework(self, date_from: datetime.date) -> List[Dict[str, Any]]:
        """
        Récupérer les devoirs
        
        Args:
            date_from: Date de début
            
        Returns:
            Liste des devoirs
        """
        if not self.client or not self.logged_in:
            return []
            
        try:
            self.check_session()
            homework_list = self.client.homework(date_from)
            
            result = []
            for hw in homework_list:
                result.append({
                    "id": hw.id,
                    "subject": hw.subject.name if hw.subject else "Aucune matière",
                    "description": hw.description,
                    "done": hw.done,
                    "date": hw.date,
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur récupération devoirs: {e}")
            return []
    
    def get_grades(self) -> Dict[str, Any]:
        """
        Récupérer les notes par période
        
        Returns:
            Dictionnaire avec les périodes et notes
        """
        if not self.client or not self.logged_in:
            return {}
            
        try:
            self.check_session()
            periods = self.client.periods
            
            result = {
                "periods": [],
                "current_period": None,
            }
            
            for period in periods:
                period_data = {
                    "id": period.id,
                    "name": period.name,
                    "grades": [],
                }
                
                for grade in period.grades:
                    period_data["grades"].append({
                        "id": grade.id,
                        "grade": grade.grade,
                        "out_of": grade.out_of,
                        "subject": grade.subject.name if grade.subject else "Aucune matière",
                        "date": grade.date,
                        "coefficient": grade.coefficient if hasattr(grade, 'coefficient') else 1,
                    })
                
                result["periods"].append(period_data)
            
            # Période actuelle
            if self.client.current_period:
                result["current_period"] = self.client.current_period.name
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur récupération notes: {e}")
            return {}
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Récupérer les messages
        
        Returns:
            Liste des messages/discussions
        """
        if not self.client or not self.logged_in:
            return []
            
        try:
            self.check_session()
            # Note: L'implémentation exacte dépend de la version de pronotepy
            # Cette partie peut nécessiter des ajustements
            messages = []
            
            # TODO: Implémenter la récupération des messages
            # Cela dépend de l'API pronotepy disponible
            
            return messages
            
        except Exception as e:
            logger.error(f"Erreur récupération messages: {e}")
            return []
    
    def logout(self):
        """Se déconnecter"""
        self.client = None
        self.logged_in = False
        logger.info("Déconnexion effectuée")
