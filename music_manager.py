# music_manager.py
import pygame
import os
import json

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = self.load_volume()
        self.music_playing = False
        
    def load_volume(self):
        """Charge le volume depuis les paramètres"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    return settings.get("volume", 0.5)  # Volume par défaut : 50%
            return 0.5
        except:
            return 0.5
    
    def save_volume(self):
        """Sauvegarde le volume dans les paramètres"""
        try:
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
            
            settings["volume"] = self.volume
            
            with open("settings.json", "w") as f:
                json.dump(settings, f)
        except:
            pass
    
    def set_volume(self, volume):
        """Définit le volume (0.0 à 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        self.save_volume()
    
    def get_volume(self):
        """Retourne le volume actuel"""
        return self.volume
    
    def play_music(self, music_path="assets/music.mp3", loop=True):
        """Lance la musique de fond"""
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.volume)
                if loop:
                    pygame.mixer.music.play(-1)  # -1 = boucle infinie
                else:
                    pygame.mixer.music.play()
                self.music_playing = True
        except pygame.error as e:
            print(f"Erreur lors du chargement de la musique: {e}")
    
    def stop_music(self):
        """Arrête la musique"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def pause_music(self):
        """Met en pause la musique"""
        pygame.mixer.music.pause()
    
    def resume_music(self):
        """Reprend la musique"""
        pygame.mixer.music.unpause()
    
    def is_playing(self):
        """Vérifie si la musique joue"""
        return pygame.mixer.music.get_busy() and self.music_playing

# Instance globale du gestionnaire de musique
music_manager = MusicManager()
