
"""
class: Audio
"""

import os
import pickle
import random

import pygame

import console
import maps
import statemachine


OPTIONSPATH = 'options'
OPTIONSFILE = os.path.join(OPTIONSPATH, 'audio.cfg')

MUSICPATH = 'resources/music'
MAINMENU = os.path.join(MUSICPATH,  'mainmenu.ogg')
OVERWORLD = os.path.join(MUSICPATH, 'overworld.ogg')

SOUNDSPATH = 'resources/sounds'

FADEOUTTIME = 500

# Alle geluiden.
MENUSWITCH = 'menu_switch'
MENUSELECT = 'menu_select'
MENUERROR = 'menu_error'
STEPGRASS = 'step_grass'
STEPSTONE = 'step_stone'
BIRDS = 'birds'
CROWS = 'crows'
WIND = 'wind'


class Audio(object):
    """
    De audio handler.
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

        self.sfx = self._load_all_sfx()

    @staticmethod
    def _load_all_sfx():
        """
        Laadt alle geluiden uit de map in een dict.
        :return: de dict
        """
        effects = {}
        for fx in os.listdir(SOUNDSPATH):
            name, ext = os.path.splitext(fx)
            effects[name] = pygame.mixer.Sound(os.path.join(SOUNDSPATH, fx))
        return effects

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        if not os.path.exists(OPTIONSPATH):
            os.makedirs(OPTIONSPATH)

        try:
            with open(OPTIONSFILE, 'rb') as f:
                self.music, self.sound = pickle.load(f)
            console.load_options()
        except (pickle.UnpicklingError, FileNotFoundError, EOFError):
            console.corrupt_options()
            self.music, self.sound = 1, 1
            self.write_cfg()

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(OPTIONSFILE, 'wb') as f:
            pickle.dump([self.music, self.sound], f)
        console.write_options()

    def flip_sound(self):
        """
        Zet geluid aan als het uit staat en vice versa.
        """
        if self.sound == 1:
            self.stop_sound(MENUSELECT)     # vanwege de enter knop in menu's speelt hij dit geluid af,
            self.sound = 0                      # stop hem daarom alsnog.
            self.stop_bg_sounds()
        elif self.sound == 0:
            self.sound = 1
            self.play_sound(MENUSELECT)     # en speel weer een geluid af omdat er geluid is.
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
                    if self.engine.gamestate.peek().window.map1.name in (maps.STARTFOREST,
                                                                         maps.BELOWSTARTFOREST):
                        self.bg_music_channel.play(self.overworld, -1)

    def set_bg_sounds(self, currentstate):
        """
        Zet de achtergrond geluiden aan of uit afhankelijk van een state.
        :param currentstate: self.statemachine.peek()
        """
        if currentstate != statemachine.States.OptionsMenu and \
           self.engine.gamestate.prev_state != statemachine.States.OptionsMenu:
            self.fade_bg_sounds()
            self.bg_sound_channel1.set_volume(1)
            self.bg_sound_channel2.set_volume(1)
            if currentstate == statemachine.States.MainMenu:
                self.play_sound(CROWS, loop=-1, channel=self.bg_sound_channel1)
                self.play_sound(WIND, loop=-1, channel=self.bg_sound_channel2)
            elif currentstate == statemachine.States.Overworld:
                if self.engine.gamestate.peek().window.map1.name in (maps.STARTFOREST,
                                                                     maps.BELOWSTARTFOREST):
                    self.play_sound(BIRDS, loop=-1, channel=self.bg_sound_channel1)

    def play_sound(self, sound, loop=0, channel=None):
        """
        Als mag, speel dan geluid.
        :param sound: een geluidsfragment uit de init.
        :param loop: -1 is oneindig loopen
        :param channel: het kanaal waar de geluiden op afgespeeld moeten worden, is alleen voor bg_sounds
        """
        if self.sound == 1:
            if channel:
                channel.play(self.sfx[sound], loops=loop)
            else:
                self.sfx[sound].play()

    def stop_sound(self, sound):
        """
        Stop het huidige geluid onmiddelijk.
        :param sound: een geluidsfragment uit de init.
        """
        self.sfx[sound].stop()

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

    def play_step_sound(self):
        """
        Speel de juiste voetstap geluiden af op de juiste maps.
        """
        # todo, deze magic numbers moeten nog weg
        if self.engine.gamestate.peek().window.map1.name in (maps.STARTFOREST,
                                                             maps.BELOWSTARTFOREST):
            sfx_num = str(random.randint(1, 2))
            self.play_sound(STEPGRASS+sfx_num)
        elif self.engine.gamestate.peek().window.map1.name in (maps.STARTTOWN,
                                                               maps.STARTTOWNARMORSHOP):
            sfx_num = str(random.randint(1, 6))
            self.play_sound(STEPSTONE+sfx_num)
