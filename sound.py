
"""
class: Sound
"""

import os

import pygame

SOUNDSPATH = 'resources/sounds'
MENUSWITCHSOUND = os.path.join(SOUNDSPATH, 'menu_switch.wav')
MENUSELECTSOUND = os.path.join(SOUNDSPATH, 'menu_select.wav')
MENUERRORSOUND = os.path.join(SOUNDSPATH,  'menu_error.wav')


class Sound(object):
    """
    Alle geluiden.
    """
    def __init__(self):
        self.switch = pygame.mixer.Sound(MENUSWITCHSOUND)
        self.select = pygame.mixer.Sound(MENUSELECTSOUND)
        self.error = pygame.mixer.Sound(MENUERRORSOUND)
