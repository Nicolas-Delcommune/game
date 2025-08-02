# 🧩 Jeu de Puzzle - Le Puzzle Authentique

Un jeu de puzzle moderne et immersif avec des pièces aux formes réalistes et authentiques. Redécouvrez le plaisir du puzzle traditionnel dans une version numérique soignée !

## 🎮 Caractéristiques du Jeu

### ✨ **Gameplay Authentique**
- **Pièces réalistes** avec formes irrégulières et connexions authentiques
- **Système de verrouillage précis** - placez les pièces exactement au bon endroit
- **Glisser-déposer intuitif** avec détection intelligente des positions
- **Animation de réussite** avec célébration visuelle

### **Niveaux de Difficulté**
- **🟢 Facile** : 3x3 (9 pièces) - Parfait pour débuter
- **🟡 Moyen** : 4x4 (16 pièces) - Un défi équilibré  
- **🟠 Difficile** : 5x5 (25 pièces) - Pour les experts
- **🔴 Impossible** : 6x6 (36 pièces) - Le défi ultime !

### 🖼️ **Images Variées**
- **10 images magnifiques** incluses
- **Progression par niveaux** - débloquez de nouveaux défis
- **Système de temps** - battez vos meilleurs scores
- **Sauvegarde automatique** de votre progression

### 🎵 **Expérience Immersive**
- **Musique de fond relaxante** (volume ajustable)
- **Effets visuels soignés** avec animations fluides
- **Interface moderne** avec thème coloré adaptatif
- **Mode plein écran** disponible

### ⚙️ **Fonctionnalités Avancées**
- **Menu pause** avec options complètes
- **Animation d'abandon** - regardez le puzzle se compléter automatiquement
- **Paramètres personnalisables** (volume, plein écran)
- **Progression sauvegardée** entre les sessions

## 📥 Téléchargement et Installation

### 🚀 **Option 1 : Exécutable (Recommandé)**
1. Téléchargez le dossier `Jeu/` complet
2. Lancez `main.exe`
3. Jouez immédiatement ! ✨

*Aucune installation requise - tout est inclus !*

### 🛠️ **Option 2 : Code Source Python**
```bash
# Prérequis : Python 3.8+ et pip
git clone https://github.com/Nicolas-Delcommune/game.git
cd game
pip install pygame
python main.py
```

## 🎮 Comment Jouer

### 🎯 **Objectif**
Reconstituez l'image en plaçant toutes les pièces du puzzle à leur position correcte.

### 🖱️ **Contrôles**
- **Clic gauche + Glisser** : Déplacer une pièce
- **Relâcher** près de la bonne position : La pièce se verrouille automatiquement
- **Échap** : Ouvrir le menu pause
- **Clic sur ?** : Afficher l'image de référence

### 📋 **Étapes de Jeu**
1. **Choisissez votre difficulté** dans le menu principal
2. **Sélectionnez un niveau** (les niveaux se débloquent progressivement)
3. **Glissez les pièces** vers leurs positions correctes
4. **Utilisez la référence** (bouton ?) si nécessaire
5. **Célébrez votre victoire** ! 🎉

### 💡 **Conseils de Pro**
- Commencez par les **pièces des coins et des bords**
- Utilisez l'**image de référence** pour vous guider
- La **zone de verrouillage** est précise - soyez patient !
- En cas de blocage, utilisez **"Abandonner"** pour voir la solution

## ⚙️ Menu Pause

Appuyez sur **Échap** pendant le jeu pour accéder aux options :
- **▶️ Reprendre** - Continuer le puzzle
- **🏠 Menu Principal** - Retourner au menu (progression sauvée)
- **🏳️ Abandonner** - Voir l'animation de completion automatique
- **❌ Quitter** - Fermer le jeu

## 🔧 Paramètres

Accessible depuis le menu principal :
- **🔊 Volume** - Ajustez la musique (glissez sur la barre)
- **🖥️ Plein Écran** - Basculer entre fenêtré et plein écran
- **💾 Sauvegarde automatique** - Vos réglages sont conservés

## 📊 Système de Progression

- **Temps enregistrés** pour chaque niveau complété
- **Déblocage progressif** des niveaux suivants
- **Sauvegarde automatique** dans `progress.json`
- **Battez vos records** personnels !

## 🎨 Technologies Utilisées

- **Python 3.12** - Langage principal
- **Pygame** - Moteur graphique et audio
- **PyInstaller** - Création de l'exécutable
- **JSON** - Sauvegarde des données

## 📁 Structure du Projet

```
puzzle_game/
├── 🎮 main.exe              # Exécutable principal
├── 📁 assets/               # Images et musique
├── ⚙️ settings.json         # Paramètres utilisateur
├── 📊 progress.json         # Progression sauvegardée
└── 📖 README.md            # Ce fichier
```

## 🐛 Dépannage

### **Le jeu ne se lance pas ?**
- Vérifiez que le dossier `assets/` est présent
- Sous Windows : Autorisez l'exécution si Windows Defender bloque

### **Pas de son ?**
- Vérifiez vos paramètres audio système
- Ajustez le volume dans les paramètres du jeu

### **Performance lente ?**
- Fermez les autres applications gourmandes
- Réduisez la résolution de votre écran si nécessaire

## 🤝 Contribution

Ce projet est ouvert aux contributions ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Ajouter de nouvelles images
- Améliorer le code

## 📄 Licence

Ce projet est sous licence libre. Vous pouvez l'utiliser, le modifier et le distribuer librement.

## 👨‍💻 Auteur

**Nicolas Delcommune**
- GitHub: [@Nicolas-Delcommune](https://github.com/Nicolas-Delcommune)

---

### 🎉 Amusez-vous bien et bon puzzle ! 🧩

*"Un puzzle bien fait est comme une méditation interactive"*