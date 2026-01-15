"""
Système de notifications
"""
from plyer import notification
import logging

logger = logging.getLogger(__name__)


class NotificationManager:
    """Gestionnaire de notifications système"""
    
    def __init__(self, app_name: str = "Pronote Amélioré"):
        self.app_name = app_name
        self.enabled = True
    
    def send(self, title: str, message: str, timeout: int = 10):
        """
        Envoyer une notification
        
        Args:
            title: Titre de la notification
            message: Message de la notification
            timeout: Durée d'affichage en secondes
        """
        if not self.enabled:
            return
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=timeout,
            )
            logger.info(f"Notification envoyée: {title}")
        except Exception as e:
            logger.error(f"Erreur envoi notification: {e}")
    
    def notify_new_homework(self, count: int):
        """Notification pour nouveaux devoirs"""
        if count > 0:
            self.send(
                "Nouveaux devoirs",
                f"Vous avez {count} nouveau{'x' if count > 1 else ''} devoir{'s' if count > 1 else ''}."
            )
    
    def notify_homework_due(self, subject: str, days: int):
        """Notification pour devoir à rendre bientôt"""
        if days == 0:
            message = f"Devoir de {subject} à rendre aujourd'hui !"
        elif days == 1:
            message = f"Devoir de {subject} à rendre demain !"
        else:
            message = f"Devoir de {subject} à rendre dans {days} jours."
        
        self.send("Rappel de devoir", message)
    
    def notify_new_grade(self, subject: str, grade: str):
        """Notification pour nouvelle note"""
        self.send(
            "Nouvelle note",
            f"Nouvelle note en {subject}: {grade}"
        )
    
    def notify_new_message(self, count: int):
        """Notification pour nouveaux messages"""
        if count > 0:
            self.send(
                "Nouveaux messages",
                f"Vous avez {count} nouveau{'x' if count > 1 else ''} message{'s' if count > 1 else ''}."
            )
    
    def set_enabled(self, enabled: bool):
        """Activer/désactiver les notifications"""
        self.enabled = enabled
        logger.info(f"Notifications {'activées' if enabled else 'désactivées'}")
