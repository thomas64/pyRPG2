
"""
class: Audio
"""

import os
import pickle

import pygame

import console
import states


OPTIONSPATH = 'options'
OPTIONSFILE = os.path.join(OPTIONSPATH, 'audio.cfg')

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

FADEOUTTIME = 500


class Audio(object):
    """
    Alle geluiden.
    """
    def __init__(self, statemachine):
        self.statemachine = statemachine
        self.music = 0
        self.sound = 0
        self._load_cfg()

        self.current_music_channel = pygame.mixer.Channel(7)
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
        if not os.path.exists(OPTIONSPATH):
            os.makedirs(OPTIONSPATH)

        try:
            with open(OPTIONSFILE, 'rb') as f:
                self.music, self.sound = pickle.load(f)
        except (pickle.UnpicklingError, FileNotFoundError):
            console.corrupt_options()
            self.music, self.sound = 1, 1
            with open(OPTIONSFILE, 'wb') as f:
                pickle.dump([self.music, self.sound], f)

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(OPTIONSFILE, 'wb') as f:
            pickle.dump([self.music, self.sound], f)

    def flip_sound(self):
        """
        Zet geluid aan als het uit staat en vice versa.
        """
        if self.sound == 1:
            self.stop_sound(self.select)    # vanwege de enter knop in menu's speelt hij dit geluid af,
            self.sound = 0                  # stop hem daarom alsnog.
        elif self.sound == 0:
            self.sound = 1
            self.play_sound(self.select)    # en speel weer een geluid af omdat er geluid is.

    def flip_music(self):
        """
        Zet muziek aan als het uit staat en vice versa.
        """
        if self.music == 1:
            self.music = 0
            self.stop_music()
        elif self.music == 0:
            self.music = 1
            self.play_music()

    def play_music(self):
        """
        Als mag, fade dan de huidige. Volume max, fade nieuwe muziek in.
        """
        if self.music == 1:
            self.fade_music()
            self.current_music_channel.set_volume(1)
            currentstate = self.statemachine.peek()
            if currentstate == states.GameState.MainMenu or \
               currentstate == states.GameState.OptionsMenu:
                self.current_music_channel.play(self.mainmenu, -1)
            elif currentstate == states.GameState.Overworld:
                self.current_music_channel.play(self.overworld, -1)

    def stop_music(self):
        """
        Laat het muziekkanaal stoppen.
        """
        self.current_music_channel.stop()

    def play_sound(self, sound):
        """
        Als mag, speel dan geluid.
        :param sound: een geluidsfragment uit de init.
        """
        if self.sound == 1:
            sound.play()

    @staticmethod
    def stop_sound(sound):
        """
        "Stop het huidige geluid onmiddelijk.
        :param sound: een geluidsfragment uit de init.
        """
        sound.stop()

    def fade_music(self):
        """
        Als er muziek speelt, fade die out.
        """
        if self.current_music_channel.get_sound() is not None:
            self.current_music_channel.fadeout(FADEOUTTIME)
