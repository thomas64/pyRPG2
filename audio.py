
"""
class: Audio
"""

import os
import pickle

import pygame


MUSICPATH = 'resources/music'
MAINMENUMUSIC = os.path.join(MUSICPATH,  'mainmenu.ogg')
OVERWORLDMUSIC = os.path.join(MUSICPATH, 'overworld.ogg')

SOUNDSPATH = 'resources/sounds'
MENUSWITCHSOUND = os.path.join(SOUNDSPATH, 'menu_switch.wav')
MENUSELECTSOUND = os.path.join(SOUNDSPATH, 'menu_select.wav')
MENUERRORSOUND = os.path.join(SOUNDSPATH,  'menu_error.wav')

# todo, op andere ondergrond, ander stap geluid
STEP_GRASS_L = os.path.join(SOUNDSPATH, 'step_grass_l.wav')
STEP_GRASS_R = os.path.join(SOUNDSPATH, 'step_grass_r.wav')


class Audio(object):
    """
    Alle geluiden.
    """
    def __init__(self):
        self.music = 0
        self.sound = 0
        self._load_cfg()

        self.current = pygame.mixer.Channel(7)
        self.mainmenu = pygame.mixer.Sound(MAINMENUMUSIC)
        self.overworld = pygame.mixer.Sound(OVERWORLDMUSIC)

        self.switch = pygame.mixer.Sound(MENUSWITCHSOUND)
        self.select = pygame.mixer.Sound(MENUSELECTSOUND)
        self.error = pygame.mixer.Sound(MENUERRORSOUND)
        self.step_left = pygame.mixer.Sound(STEP_GRASS_L)
        self.step_right = pygame.mixer.Sound(STEP_GRASS_R)

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        try:
            with open('options.cfg', 'rb') as f:
                self.music, self.sound = pickle.load(f)
        except (pickle.UnpicklingError, FileNotFoundError):
            print('Corrupt options file.')
            self.music, self.sound = 1, 1
            with open('options.cfg', 'wb') as f:
                pickle.dump([self.music, self.sound], f)

    def play_music(self, music):
        """
        Als mag, fade dan de huidige. Volume max, fade nieuwe muziek in.
        :param music: een muziekfragment uit de init.
        """
        if self.music == 1:
            self.fade_music()
            self.current.set_volume(1)
            self.current.play(music, -1, fade_ms=3000)

    def play_sound(self, sound):
        """
        Als mag, speel dan geluid.
        :param sound: een geluidsfragment uit de init.
        """
        if self.sound == 1:
            sound.play()

    def fade_music(self):
        """
        Als er muziek speelt, fade die out.
        """
        if self.current.get_sound() is not None:
            self.current.fadeout(1000)
