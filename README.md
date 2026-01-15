# 🎓 Pronote Amélioré

Application desktop moderne pour accéder à Pronote avec une interface utilisateur améliorée.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Fonctionnalités

### ✅ Implémentées

- **🔐 Authentification**

  - Connexion avec identifiants Pronote
  - Sauvegarde sécurisée des credentials
  - Reconnexion automatique

- **📅 Emploi du temps**

  - Affichage par semaine
  - Navigation entre les semaines
  - Cartes colorées par matière
  - Informations détaillées (professeur, salle, horaires)

- **📊 Notes**

  - Affichage par période (trimestre/semestre)
  - Organisation par matière
  - Calcul automatique des moyennes
  - Export CSV

- **📝 Devoirs**

  - Liste des devoirs à venir
  - Filtres (Tous, À faire, Terminés)
  - Organisation par date
  - Indication de la proximité (aujourd'hui, demain, etc.)

- **✉️ Messagerie**

  - Interface prête pour la messagerie Pronote
  - (Dépend des permissions de l'établissement)

- **🎨 Interface moderne**

  - Mode sombre/clair
  - Design épuré et intuitif
  - Navigation par sidebar
  - Responsive

- **📥 Export de données**

  - Export CSV des notes
  - Export CSV des devoirs
  - Export JSON

- **🔔 Notifications**
  - Système de notifications préparé
  - Notifications Windows natives

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Windows 10/11 (testé sur Windows)

### Installation automatique

1. **Double-cliquez sur `setup.bat`**

   Le script va automatiquement:

   - Créer un environnement virtuel
   - Installer toutes les dépendances
   - Lancer l'application

### Installation manuelle

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python -m app.main
```

## 📖 Utilisation

### Première connexion

1. Lancez l'application via `setup.bat` ou `python -m app.main`
2. Entrez l'URL de votre Pronote (ex: `https://votre-etablissement.index-education.net/pronote/eleve.html`)
3. Entrez votre nom d'utilisateur et mot de passe
4. Cochez "Se souvenir de moi" pour une reconnexion automatique
5. Cliquez sur "Se connecter"

### Navigation

- **📅 Emploi du temps**: Consultez votre emploi du temps hebdomadaire
  - Utilisez les flèches pour naviguer entre les semaines
- **📊 Notes**: Visualisez vos notes par période
  - Sélectionnez la période dans le menu
  - Exportez vos notes en CSV si besoin
- **📝 Devoirs**: Gérez vos devoirs
  - Filtrez par statut (Tous, À faire, Terminés)
  - Marquez les devoirs comme faits
- **✉️ Messages**: Accédez à votre messagerie
  - (Fonctionnalité dépendante de votre établissement)

### Thèmes

Cliquez sur le bouton "🌙 Mode sombre" / "☀️ Mode clair" dans la barre latérale pour changer de thème.

## 📁 Structure du projet

```
api-pronote/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée
│   ├── config.py               # Configuration
│   ├── pronote_api/
│   │   ├── __init__.py
│   │   ├── client.py           # Client API Pronote
│   │   └── cache.py            # Système de cache
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login.py            # Fenêtre de connexion
│   │   ├── main_window.py      # Fenêtre principale
│   │   ├── schedule.py         # Page emploi du temps
│   │   ├── grades.py           # Page notes
│   │   ├── homework.py         # Page devoirs
│   │   └── messages.py         # Page messagerie
│   └── utils/
│       ├── __init__.py
│       ├── themes.py           # Gestion des thèmes
│       ├── notifications.py    # Notifications
│       └── export.py           # Export de données
├── assets/
│   ├── icons/                  # Icônes (à ajouter)
│   └── images/                 # Images (à ajouter)
├── data/
│   ├── credentials.json        # Credentials sauvegardés
│   ├── settings.json           # Paramètres utilisateur
│   ├── cache.json              # Cache des données
│   └── app.log                 # Logs de l'application
├── requirements.txt            # Dépendances Python
├── setup.bat                   # Script d'installation
├── pronote_liste.txt          # Liste des APIs Pronote
└── README.md                   # Ce fichier
```

## 🔧 Configuration

Les fichiers de configuration se trouvent dans le dossier `data/`:

- **credentials.json**: Credentials de connexion (ne pas partager!)
- **settings.json**: Préférences utilisateur (thème, notifications, etc.)
- **cache.json**: Cache des données Pronote

## 🛠️ Technologies utilisées

- **[Python](https://www.python.org/)** - Langage de programmation
- **[pronotepy](https://github.com/bain3/pronotepy)** - API wrapper pour Pronote
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Interface graphique moderne
- **[Pillow](https://python-pillow.org/)** - Gestion d'images
- **[ReportLab](https://www.reportlab.com/)** - Export PDF
- **[Plyer](https://github.com/kivy/plyer)** - Notifications système

## ⚠️ Notes importantes

1. **DEMO Mode**: Pour tester sans compte réel, utilisez:

   - URL: `https://demo.index-education.net/pronote/eleve.html`
   - Username: `demonstration`
   - Password: `pronotevs`

2. **Limitations**:

   - L'API pronotepy est en mode maintenance (bugs fixés, pas de nouvelles features)
   - Certaines fonctionnalités dépendent des permissions de votre établissement
   - La messagerie peut ne pas être accessible selon la configuration Pronote

3. **Sécurité**:
   - Les credentials sont stockés localement dans `data/credentials.json`
   - Ne partagez jamais ce fichier
   - Utilisez un mot de passe fort pour votre compte Pronote

## 🐛 Dépannage

### L'application ne se lance pas

```bash
# Vérifier la version de Python
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Erreur de connexion

- Vérifiez votre URL Pronote (doit se terminer par `/eleve.html`)
- Vérifiez vos identifiants
- Vérifiez votre connexion internet
- Consultez les logs dans `data/app.log`

### Interface qui ne s'affiche pas correctement

- Réinstallez CustomTkinter: `pip install customtkinter --upgrade`
- Vérifiez la résolution de votre écran (minimum 900x600)

## 📝 Roadmap

- [ ] Notifications push pour nouveaux devoirs
- [ ] Graphiques de progression des notes
- [ ] Mode hors-ligne amélioré
- [ ] Export PDF personnalisé
- [ ] Widget desktop
- [ ] Support multi-comptes

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [bain3/pronotepy](https://github.com/bain3/pronotepy) pour l'API wrapper
- [TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) pour l'interface moderne
- Index Education pour Pronote

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Fait avec ❤️ pour tous les étudiants qui veulent une meilleure expérience Pronote**
