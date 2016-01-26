
"""
class: Sound
"""

import os

import pygame


MUSICPATH = 'resources/music'
MAINMENUMUSIC = os.path.join(MUSICPATH,  'mainmenu.ogg')
OVERWORLDMUSIC = os.path.join(MUSICPATH, 'overworld.ogg')

SOUNDSPATH = 'resources/sounds'
MENUSWITCHSOUND = os.path.join(SOUNDSPATH, 'menu_switch.wav')
MENUSELECTSOUND = os.path.join(SOUNDSPATH, 'menu_select.wav')
MENUERRORSOUND = os.path.join(SOUNDSPATH,  'menu_error.wav')


class Sound(object):
    """
    Alle geluiden.
    """
    def __init__(self):
        self.current = pygame.mixer.Channel(7)
        self.mainmenu = pygame.mixer.Sound(MAINMENUMUSIC)
        self.overworld = pygame.mixer.Sound(OVERWORLDMUSIC)

        self.switch = pygame.mixer.Sound(MENUSWITCHSOUND)
        self.select = pygame.mixer.Sound(MENUSELECTSOUND)
        self.error = pygame.mixer.Sound(MENUERRORSOUND)
