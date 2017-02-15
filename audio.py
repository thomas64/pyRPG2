
"""
class: Audio
"""

import os
import pickle
import random

import pygame

from console import Console
from constants import GameState
from constants import MapMusic
from constants import SFX


SETTINGSPATH = 'settings'
SETTINGSFILE = os.path.join(SETTINGSPATH, 'audio.cfg')
MUSICPATH = 'resources/music'
SOUNDSPATH = 'resources/sounds'

FADEOUTTIME = 500

# Alle niet overworld kaart muziek.
TITLESCREEN = 'titlescreen'

DEFAULTSTEPSOUND = "step_grass"


class Audio(object):
    """
    De audio handler.
    """
    def __init__(self, engine):
        self.engine = engine
        self.music = False
        self.sound = False
        self._load_cfg()

        self.bg_music_channel = pygame.mixer.Channel(7)
        self.bg_sound_channel1 = pygame.mixer.Channel(6)
        self.bg_sound_channel2 = pygame.mixer.Channel(5)

        self.mfx = self._load_all_sfx(MUSICPATH)
        self.sfx = self._load_all_sfx(SOUNDSPATH)

        self.footstep = DEFAULTSTEPSOUND

    @staticmethod
    def _load_all_sfx(path):
        """
        Laadt alle geluiden uit de map in een dict.
        :return: de dict
        """
        effects = {}
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            effects[name] = pygame.mixer.Sound(os.path.join(path, file))
        return effects

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        if not os.path.exists(SETTINGSPATH):
            os.makedirs(SETTINGSPATH)

        try:
            with open(SETTINGSFILE, 'rb') as f:
                self.music, self.sound = pickle.load(f)
            Console.load_settings()
        except (pickle.UnpicklingError, FileNotFoundError, EOFError):
            Console.corrupt_settings()
            self.music, self.sound = True, True
            self.write_cfg()

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(SETTINGSFILE, 'wb') as f:
            pickle.dump([self.music, self.sound], f)
        Console.write_settings()

    def flip_sound(self):
        """
        Zet geluid aan als het uit staat en vice versa.
        """
        if self.sound:
            self.stop_sound(SFX.menu_select)         # vanwege de enter knop in menu's speelt hij dit geluid af,
            self.sound = False                       # stop hem daarom alsnog.
            self.stop_bg_sounds()
        else:
            self.sound = True
            self.play_sound(SFX.menu_select)         # en speel weer een geluid af omdat er geluid is.
            self.set_bg_sounds(force=True)

    def flip_music(self):
        """
        Zet muziek aan als het uit staat en vice versa.
        """
        if self.music:
            self.music = False
            self.stop_bg_music()
        else:
            self.music = True
            self.set_bg_music(force=True)

    # todo, muziek van mainmenu later in laten komen?
    def set_bg_music(self, force=False):
        """
        Alle bg music voorwaardelijke mogelijkheden op een rij afgehandeld.
        """
        curr_state = self.engine.gamestate.peek().name
        prev_state = self.engine.gamestate.prev_state

        if curr_state == GameState.MainMenu and \
                (prev_state is None or
                 prev_state == GameState.MainMenu or
                 prev_state == GameState.LoadMenu):
            self.bg_music_channel.set_volume(1)
            self.play_bg_music(TITLESCREEN)
        elif curr_state == GameState.MainMenu and \
                prev_state == GameState.SettingsMenu:
            pass
        elif curr_state == GameState.LoadMenu and \
                prev_state == GameState.MainMenu:
            self.fade_bg_music()
        elif curr_state == GameState.SettingsMenu and \
                prev_state == GameState.MainMenu and \
                force is True:
            self.bg_music_channel.set_volume(1)
            self.play_bg_music(TITLESCREEN)
        elif curr_state == GameState.SettingsMenu:
            pass
        elif curr_state == GameState.PauseMenu:
            self.fade_bg_music()
        elif curr_state == GameState.PartyScreen:
            self.fade_bg_music()
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.MessageBox or
                 prev_state == GameState.LoadScreen) and \
                force is True:
            self.bg_music_channel.set_volume(1)
            self.play_bg_music(MapMusic[self.engine.data.map_name].value[0])
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.PauseMenu or
                 prev_state == GameState.PartyScreen):
            self.bg_music_channel.set_volume(1)
            self.play_bg_music(MapMusic[self.engine.data.map_name].value[0])
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.Shop or
                 prev_state == GameState.ConfirmBox):
            pass
        elif curr_state == GameState.Overworld and \
                prev_state == GameState.Overworld:
            if self._new_map_has_different_bg_music():
                self.bg_music_channel.set_volume(1)
                self.play_bg_music(MapMusic[self.engine.data.map_name].value[0])

    def set_bg_sounds(self, force=False):
        """
        Alle bg sounds voorwaardelijke mogelijkheden op een rij afgehandeld.
        """
        curr_state = self.engine.gamestate.peek().name
        prev_state = self.engine.gamestate.prev_state

        if curr_state == GameState.MainMenu and \
                (prev_state is None or
                 prev_state == GameState.MainMenu or
                 prev_state == GameState.LoadMenu):
            self.bg_sound_channel1.set_volume(1)
            self.bg_sound_channel2.set_volume(1)
            # self.play_sound(RIVER, loop=-1, channel=self.bg_sound_channel1)
            # self.play_sound(WIND, loop=-1, channel=self.bg_sound_channel2)
        elif curr_state == GameState.MainMenu and \
                prev_state == GameState.SettingsMenu:
            pass
        elif curr_state == GameState.LoadMenu and \
                prev_state == GameState.MainMenu:
            self.fade_bg_sounds()
        elif curr_state == GameState.SettingsMenu and \
                prev_state == GameState.MainMenu and \
                force is True:
            self.bg_sound_channel1.set_volume(1)
            self.bg_sound_channel2.set_volume(1)
            # self.play_sound(RIVER, loop=-1, channel=self.bg_sound_channel1)
            # self.play_sound(WIND, loop=-1, channel=self.bg_sound_channel2)
        elif curr_state == GameState.SettingsMenu:
            pass
        elif curr_state == GameState.PauseMenu:
            self.fade_bg_sounds()
        elif curr_state == GameState.PartyScreen:
            self.fade_bg_sounds()
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.MessageBox or
                 prev_state == GameState.LoadScreen) and \
                force is True:
            self.bg_sound_channel1.set_volume(1)
            self.bg_sound_channel2.set_volume(1)
            self.play_sound(MapMusic[self.engine.data.map_name].value[1],
                            loop=-1, channel=self.bg_sound_channel1)
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.PauseMenu or
                 prev_state == GameState.PartyScreen):
            self.bg_sound_channel1.set_volume(1)
            self.bg_sound_channel2.set_volume(1)
            self.play_sound(MapMusic[self.engine.data.map_name].value[1],
                            loop=-1, channel=self.bg_sound_channel1)
        elif curr_state == GameState.Overworld and \
                (prev_state == GameState.Shop or
                 prev_state == GameState.ConfirmBox):
            pass
        elif curr_state == GameState.Overworld and \
                prev_state == GameState.Overworld:
            if self._new_map_has_different_bg_sounds():
                self.bg_sound_channel1.set_volume(1)
                self.bg_sound_channel2.set_volume(1)
                self.play_sound(MapMusic[self.engine.data.map_name].value[1],
                                loop=-1, channel=self.bg_sound_channel1)

    def play_sound(self, sound, loop=0, channel=None):
        """
        Als mag, speel dan geluid.
        :param sound: de naam van het geluidsfragment. is een Enum SFX, maar niet als het een bgsound is.
        :param loop: -1 is oneindig loopen
        :param channel: het kanaal waar de geluiden op afgespeeld moeten worden, is alleen voor bg_sounds
        """
        if self.sound:
            # als het aangestuurde geluid None is, niets doen natuurlijk.
            if sound:
                # het kan ook niet altijd een enum zijn, maar een string, voornamelijk bij bgsound en voetstappen.
                import enum
                if isinstance(sound, enum.Enum):
                    sound = sound.name

                if channel:
                    channel.play(self.sfx[sound], loops=loop)
                else:
                    self.sfx[sound].play()

    def play_bg_music(self, music):
        """
        Als mag, speel dan muziek.
        :param music: de naam van het geluidsfragment
        """
        if self.music:
            self.bg_music_channel.play(self.mfx[music], loops=-1)

    def stop_sound(self, sound):
        """
        Stop het huidige geluid onmiddelijk.
        :param sound: een geluidsfragment uit de init. is een Enum SFX
        """
        self.sfx[sound.name].stop()

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

    def fade_bg_music_when_loading_a_new_map(self):
        """..."""
        if self._new_map_has_different_bg_music():
            self.fade_bg_music()

    def fade_bg_sounds_when_loading_a_new_map(self):
        """..."""
        if self._new_map_has_different_bg_sounds():
            self.fade_bg_sounds()

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
        Speel de juiste voetstap geluiden af op de juiste ondergrond.
        """
        # todo, deze magic numbers moeten nog weg
        sfx_num = str(random.randint(1, 4))
        self.play_sound(self.footstep+sfx_num)

    def _new_map_has_different_bg_music(self):
        """..."""
        # eerst 2 korte vars ipv lange functies
        prev_map = self.engine.gamestate.peek().window.prev_map_name
        new_map = self.engine.data.map_name
        # zet eerst prev_music op None
        prev_music = None
        # vind de nieuwe muziek door de nieuwe map naam als key te gebruiken in de MapMusic Enum.
        new_music = MapMusic[new_map].value[0]
        # uit prev_map kan None uitkomen, als hier geen None uit komt, gebruik dan die waarde als Enum key.
        if prev_map:
            prev_music = MapMusic[prev_map].value[0]
        # als de oude en nieuwe niet gelijk zijn, speel dan de nieuwe muziek.
        if new_music != prev_music:
            return True
        else:
            return False

    def _new_map_has_different_bg_sounds(self):
        """..."""
        prev_map = self.engine.gamestate.peek().window.prev_map_name
        new_map = self.engine.data.map_name
        prev_bgs = None
        new_bgs = MapMusic[new_map].value[1]
        if prev_map:
            prev_bgs = MapMusic[prev_map].value[1]
        if new_bgs != prev_bgs:
            return True
        else:
            return False
