# Comment créer un exécutable du Jeu de Puzzle

## Méthode 1 : Script automatique (Recommandé)

1. Double-cliquez sur `create_executable.bat`
2. L'exécutable sera créé dans le dossier `dist/`
3. Le fichier s'appellera `Puzzle_Game.exe`

## Méthode 2 : Ligne de commande

### Installation de PyInstaller (si pas déjà fait) :
```bash
pip install pyinstaller
```

### Commandes pour créer l'exécutable :

#### Option A - Exécutable simple :
```bash
pyinstaller --onefile --windowed main.py
```

#### Option B - Avec le fichier spec (plus de contrôle) :
```bash
pyinstaller --clean puzzle_game.spec
```

#### Option C - Avec icône personnalisée :
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## Paramètres PyInstaller expliqués :

- `--onefile` : Crée un seul fichier exécutable
- `--windowed` : Lance sans console (pour les jeux GUI)
- `--clean` : Nettoie les fichiers temporaires avant la compilation
- `--icon=fichier.ico` : Ajoute une icône personnalisée

## Fichiers créés :

- `dist/` : Contient l'exécutable final
- `build/` : Fichiers temporaires (peut être supprimé)
- `*.spec` : Fichier de configuration PyInstaller

## Distribution :

Pour distribuer votre jeu :
1. Copiez le fichier `Puzzle_Game.exe` du dossier `dist/`
2. Assurez-vous que le dossier `assets/` soit dans le même répertoire que l'exe
3. Votre jeu est prêt à être partagé !

## Dépannage :

Si l'exécutable ne fonctionne pas :
- Vérifiez que tous les fichiers assets sont inclus
- Testez d'abord avec `--console` pour voir les erreurs
- Vérifiez les imports dans votre code Python

## Taille de l'exécutable :

L'exécutable fera environ 20-30 MB car il inclut Python et toutes les bibliothèques nécessaires.
