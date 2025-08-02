@echo off
echo Creation de l'executable du jeu de puzzle...
echo.

REM Activer l'environnement virtuel et utiliser PyInstaller
C:\Users\nicol\Documents\Projets_perso\puzzle_game\.venv\Scripts\pyinstaller.exe --clean puzzle_game.spec

echo.
echo Executable cree dans le dossier dist/
echo.
pause
