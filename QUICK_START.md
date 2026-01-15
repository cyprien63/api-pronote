# 🚀 Guide de Démarrage Rapide - Pronote Amélioré

## Premier Lancement

### 1. Installer et lancer l'application

Double-cliquez sur `setup.bat` ou exécutez:

```bash
.\setup.bat
```

### 2. Se connecter

#### Option A: Mode DÉMO (pour tester)

✅ **Recommandé pour tester l'application**

- **URL**: `https://demo.index-education.net/pronote/eleve.html`
- **Username**: `demonstration`
- **Password**: `pronotevs`

#### Option B: Votre compte Pronote réel

1. Trouvez votre URL Pronote:

   - Elle ressemble à: `https://[votre-etablissement].index-education.net/pronote/eleve.html`
   - **Important**: Elle doit se terminer par `/eleve.html`

2. Entrez vos identifiants:

   - Nom d'utilisateur: Votre identifiant Pronote
   - Mot de passe: Votre mot de passe Pronote

3. Cochez "Se souvenir de moi" pour une reconnexion automatique

### 3. Profitez de l'application !

Une fois connecté, vous pouvez:

- 📅 **Emploi du temps**: Voir votre semaine, naviguer entre les semaines
- 📊 **Notes**: Consulter vos notes par période, voir vos moyennes
- 📝 **Devoirs**: Gérer vos devoirs, les marquer comme faits
- ✉️ **Messages**: Accéder à votre messagerie (si disponible)

## ⚠️ Problèmes Courants

### ❌ "Identifiants incorrects"

**Causes possibles**:

- Mauvais nom d'utilisateur ou mot de passe
- Credentials sauvegardés expirés/corrompus

**Solutions**:

1. Vérifiez vos identifiants
2. Supprimez le fichier `data/credentials.json` si présent
3. Relancez l'application

### ❌ "Impossible de se connecter au serveur"

**Causes possibles**:

- Pas de connexion internet
- Serveur Pronote indisponible
- Firewall qui bloque la connexion

**Solutions**:

1. Vérifiez votre connexion internet
2. Essayez de vous connecter au site Pronote dans votre navigateur
3. Désactivez temporairement votre antivirus/firewall

### ❌ "URL Pronote invalide"

**Causes possibles**:

- URL incorrecte ou incomplète
- Mauvais type de compte (parent au lieu d'élève)

**Solutions**:

1. Vérifiez que l'URL se termine par `/eleve.html`
2. Pour un compte parent, l'URL se termine par `/parent.html`
3. Copiez l'URL exacte depuis votre navigateur

### ❌ L'application ne se lance pas

**Solutions**:

```bash
# Vérifier Python
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Lancer manuellement
python -m app.main
```

## 💡 Astuces

### Changer de thème

Cliquez sur le bouton "🌙 Mode sombre" / "☀️ Mode clair" dans la sidebar

### Exporter vos notes

Page Notes → Bouton "📥 Exporter CSV"

### Navigation rapide

Utilisez les boutons de la sidebar pour changer de page

### Devoirs

- Marquez les devoirs comme faits avec les checkboxes
- Utilisez les filtres pour voir seulement ce qui vous intéresse

## 📞 Support

En cas de problème:

1. Consultez les logs dans `data/app.log`
2. Vérifiez le README.md pour plus d'informations
3. Ouvrez une issue sur GitHub

## 🎉 Bon usage !

Profitez de votre nouvelle expérience Pronote améliorée !
