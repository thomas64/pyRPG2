
"""
class: Audio
"""

import os
import pickle

import pygame

import console
import statemachine


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
    def __init__(self, engine):
        self.engine = engine
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
            # kijkt 1 laag dieper om te zien of hij in mainmenu of pausemenu zit
            self.set_bg_sounds(self.engine.gamestate.deep_peek().name)

    def flip_music(self):
        """
        Zet muziek aan als het uit staat en vice versa.
        """
        if self.music == 1:
            self.music = 0
            self.stop_bg_music()
        elif self.music == 0:
            self.music = 1
            self.set_bg_music(self.engine.gamestate.deep_peek().name)

    # todo, muziek van mainmenu later in laten komen?
    def set_bg_music(self, currentstate):
        """
        Als mag, fade dan de huidige. Volume max, fade nieuwe muziek in.
        :param currentstate: self.gamestate.peek().name
        """
        if self.music == 1:
            # bij options menu moet er niets veranderen, en ook niet als hij van options komt.
            if currentstate != statemachine.States.OptionsMenu and \
                            self.engine.gamestate.prev_state != statemachine.States.OptionsMenu:
                self.fade_bg_music()
                self.bg_music_channel.set_volume(1)
                if currentstate == statemachine.States.MainMenu:
                    self.bg_music_channel.play(self.mainmenu, -1)
                elif currentstate == statemachine.States.Overworld:
                    self.bg_music_channel.play(self.overworld, -1)

    def set_bg_sounds(self, currentstate):
        """
        Zet de achtergrond geluiden aan of uit afhankelijk van een state.
        :param currentstate: self.statemachine.peek()
        """
        if self.sound == 1:
            if currentstate != statemachine.States.OptionsMenu and \
                            self.engine.gamestate.prev_state != statemachine.States.OptionsMenu:
                self.fade_bg_sounds()
                self.bg_sound_channel1.set_volume(1)
                self.bg_sound_channel2.set_volume(1)
                if currentstate == statemachine.States.MainMenu:
                    self.bg_sound_channel1.play(self.crows, -1)
                    self.bg_sound_channel2.play(self.wind, -1)
                elif currentstate == statemachine.States.Overworld:
                    self.bg_sound_channel1.play(self.birds, -1)

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

    def stop_bg_music(self):
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

    def fade_bg_music(self):
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
