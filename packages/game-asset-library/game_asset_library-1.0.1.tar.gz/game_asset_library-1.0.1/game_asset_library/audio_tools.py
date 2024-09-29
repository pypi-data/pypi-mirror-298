import pygame

def load_sound(file_path):
    """
    Load and return a Pygame sound object.
    
    Parameters:
    - file_path: Path to the sound file
    """
    return pygame.mixer.Sound(file_path)


def play_sound(sound):
    """
    Play a sound.
    
    Parameters:
    - sound: Pygame sound object
    """
    sound.play()
