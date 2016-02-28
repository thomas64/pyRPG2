
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
MAINMENU = os.path.join(MUSICPATH,  'mainmenu.ogg')
OVERWORLD = os.path.join(MUSICPATH, 'overworld.ogg')

SOUNDSPATH = 'resources/sounds'
MENUSWITCH = os.path.join(SOUNDSPATH, 'menu_switch.ogg')
MENUSELECT = os.path.join(SOUNDSPATH, 'menu_select.ogg')
MENUERROR = os.path.join(SOUNDSPATH,  'menu_error.ogg')

WIND = os.path.join(SOUNDSPATH, 'wind.ogg')
CROWS = os.path.join(SOUNDSPATH, 'crows.ogg')
BIRDS = os.path.join(SOUNDSPATH, 'birds.ogg')
# todo, op andere ondergrond, ander stap geluid
STEPGRASSL = os.path.join(SOUNDSPATH, 'step_grass_l.ogg')
STEPGRASSR = os.path.join(SOUNDSPATH, 'step_grass_r.ogg')

FADEOUTTIME = 500


class Audio(object):
    """
    Alle geluiden.
    """
    def __init__(self):
        self.music = 0
        self.sound = 0
        self._load_cfg()

        self.bg_music_channel = pygame.mixer.Channel(7)
        self.mainmenu = pygame.mixer.Sound(MAINMENU)
        self.overworld = pygame.mixer.Sound(OVERWORLD)

        self.bg_sound_channel1 = pygame.mixer.Channel(6)
        self.bg_sound_channel2 = pygame.mixer.Channel(5)
        self.wind = pygame.mixer.Sound(WIND)
        self.crows = pygame.mixer.Sound(CROWS)
        self.birds = pygame.mixer.Sound(BIRDS)

        self.switch = pygame.mixer.Sound(MENUSWITCH)
        self.select = pygame.mixer.Sound(MENUSELECT)
        self.error = pygame.mixer.Sound(MENUERROR)
        self.step_grass_l = pygame.mixer.Sound(STEPGRASSL)
        self.step_grass_r = pygame.mixer.Sound(STEPGRASSR)

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
            self.stop_bg_sounds()
        elif self.sound == 0:
            self.sound = 1
            self.play_sound(self.select)    # en speel weer een geluid af omdat er geluid is.
            # dit is eigenlijk even een tijdelijke lelijke oplossing, maar makkelijk.
            self.bg_sound_channel1.set_volume(1)                                    #
            self.bg_sound_channel2.set_volume(1)                                    #
            self.bg_sound_channel1.play(self.crows, -1)                             #
            self.bg_sound_channel2.play(self.wind, -1)                              #

    def flip_music(self):
        """
        Zet muziek aan als het uit staat en vice versa.
        """
        if self.music == 1:
            self.music = 0
            self.stop_music()
        elif self.music == 0:
            self.music = 1
            # dit is eigenlijk even een tijdelijke lelijke oplossing, maar makkelijk.
            self.bg_music_channel.set_volume(1)                                     #
            self.bg_music_channel.play(self.mainmenu, -1)                           #

    def handle_music(self, currentstate, state_has_changed):
        """
        Als mag, fade dan de huidige. Volume max, fade nieuwe muziek in.
        :param currentstate: self.statemachine.peek()
        :param state_has_changed: True of False, als een state veranderd is
        """
        if self.music == 1:
            if state_has_changed:
                self.fade_music()
                self.bg_music_channel.set_volume(1)
                if currentstate == states.GameState.MainMenu or \
                   currentstate == states.GameState.OptionsMenu:
                    self.bg_music_channel.play(self.mainmenu, -1)
                elif currentstate == states.GameState.Overworld:
                    self.bg_music_channel.play(self.overworld, -1)

    def handle_bg_sounds(self, currentstate, state_has_changed):
        """
        Zet de achtergrond geluiden aan of uit afhankelijk van een state.
        :param currentstate: self.statemachine.peek()
        :param state_has_changed: True of False, als een state veranderd is
        """
        if self.sound == 1:
            if state_has_changed:
                self.fade_bg_sounds()
                self.bg_sound_channel1.set_volume(1)
                self.bg_sound_channel2.set_volume(1)
                if currentstate == states.GameState.MainMenu or \
                   currentstate == states.GameState.OptionsMenu:
                    self.bg_sound_channel1.play(self.crows, -1)
                    self.bg_sound_channel2.play(self.wind, -1)
                elif currentstate == states.GameState.Overworld:
                    self.bg_sound_channel1.play(self.birds, -1)

    def stop_music(self):
        """
        Laat het muziekkanaal stoppen.
        """
        self.bg_music_channel.stop()

    def stop_bg_sounds(self):
        """
        Laat de 2 achtergrondkanalen stoppen.
        """
        self.bg_sound_channel1.stop()
        self.bg_sound_channel2.stop()

    def play_sound(self, sound, loop=0):
        """
        Als mag, speel dan geluid.
        :param sound: een geluidsfragment uit de init.
        :param loop:
        """
        if self.sound == 1:
            sound.play(loops=loop)

    @staticmethod
    def stop_sound(sound):
        """
        Stop het huidige geluid onmiddelijk.
        :param sound: een geluidsfragment uit de init.
        """
        sound.stop()

    def fade_music(self):
        """
        Als er muziek speelt, fade die out.
        """
        if self.bg_music_channel.get_sound() is not None:
            self.bg_music_channel.fadeout(FADEOUTTIME)

    def fade_bg_sounds(self):
        """
        Als er achtergrondgeluiden zijn, fade die out.
        """
        if self.bg_sound_channel1.get_sound() is not None:
            self.bg_sound_channel1.fadeout(FADEOUTTIME)
        if self.bg_sound_channel2.get_sound() is not None:
            self.bg_sound_channel2.fadeout(FADEOUTTIME)
