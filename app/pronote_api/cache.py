"""
Système de cache pour réduire les appels API
"""
import json
import datetime
from pathlib import Path
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class Cache:
    """Gestion du cache local des données Pronote"""
    
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Charger le cache depuis le fichier"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erreur chargement cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Sauvegarder le cache dans le fichier"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"Erreur sauvegarde cache: {e}")
    
    def get(self, key: str, max_age_minutes: int = 30) -> Optional[Any]:
        """
        Récupérer une valeur du cache si elle n'est pas expirée
        
        Args:
            key: Clé du cache
            max_age_minutes: Durée de validité en minutes
            
        Returns:
            Valeur du cache ou None si expiré/inexistant
        """
        if key not in self.cache_data:
            return None
        
        cache_entry = self.cache_data[key]
        
        # Vérifier l'expiration
        timestamp_str = cache_entry.get("timestamp")
        if not timestamp_str:
            return None
        
        try:
            timestamp = datetime.datetime.fromisoformat(timestamp_str)
            now = datetime.datetime.now()
            age_minutes = (now - timestamp).total_seconds() / 60
            
            if age_minutes > max_age_minutes:
                logger.debug(f"Cache expiré pour {key} (âge: {age_minutes:.1f} min)")
                return None
            
            return cache_entry.get("data")
            
        except Exception as e:
            logger.error(f"Erreur lecture cache: {e}")
            return None
    
    def set(self, key: str, value: Any):
        """
        Stocker une valeur dans le cache
        
        Args:
            key: Clé du cache
            value: Valeur à stocker
        """
        self.cache_data[key] = {
            "timestamp": datetime.datetime.now().isoformat(),
            "data": value,
        }
        self._save_cache()
    
    def clear(self, key: Optional[str] = None):
        """
        Vider le cache
        
        Args:
            key: Clé spécifique à vider, ou None pour tout vider
        """
        if key:
            if key in self.cache_data:
                del self.cache_data[key]
                self._save_cache()
        else:
            self.cache_data = {}
            self._save_cache()
    
    def is_valid(self, key: str, max_age_minutes: int = 30) -> bool:
        """
        Vérifier si une entrée du cache est valide
        
        Args:
            key: Clé du cache
            max_age_minutes: Durée de validité en minutes
            
        Returns:
            True si valide, False sinon
        """
        return self.get(key, max_age_minutes) is not None
