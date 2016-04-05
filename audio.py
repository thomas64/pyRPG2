
"""
class: MapMusic
class: Audio
"""

import enum
import os
import pickle
import random

import pygame

import console
import statemachine


OPTIONSPATH = 'options'
OPTIONSFILE = os.path.join(OPTIONSPATH, 'audio.cfg')
MUSICPATH = 'resources/music'
SOUNDSPATH = 'resources/sounds'

FADEOUTTIME = 500

# Alle geluiden.
MENUSWITCH = 'menu_switch'
MENUSELECT = 'menu_select'
MENUERROR = 'menu_error'
STEPGRASS = 'step_grass'
STEPSTONE = 'step_stone'
STEPWOOD = 'step_wood'
CHEST = 'chest'
CROWS = 'crows'
RIVER = 'river'
WIND = 'wind'

# Alle niet overworld kaart muziek.
TITLESCREEN = 'titlescreen'


class MapMusic(enum.Enum):
    """
    Alle tmx kaarten op een rij, met de muziek erachter en ambient sound.
    """
    StartForest = 'start_forest',                    'start_forest',     'birds'
    StartForestBelow = 'start_forest_below',         'start_forest',     'birds'
    StartForestWaterfall = 'start_forest_waterfall', 'start_forest',     'river'
    StartTown = 'start_town',                        'start_town',       'town'
    StartTownArmorShop = 'start_town_armor_shop',    'start_town',       None
    StartTownWeaponShop = 'start_town_weapon_shop',  'start_town',       None


class Audio(object):
    """
    De audio handler.
    """
    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.music = 0
        self.sound = 0
        self._load_cfg()

        self.bg_music_channel = pygame.mixer.Channel(7)
        self.bg_sound_channel1 = pygame.mixer.Channel(6)
        self.bg_sound_channel2 = pygame.mixer.Channel(5)

        self.mfx = self._load_all_sfx(MUSICPATH)
        self.sfx = self._load_all_sfx(SOUNDSPATH)

        self.footstep = None

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
            self.stop_sound(MENUSELECT)         # vanwege de enter knop in menu's speelt hij dit geluid af,
            self.sound = 0                      # stop hem daarom alsnog.
            self.stop_bg_sounds()
        elif self.sound == 0:
            self.sound = 1
            self.play_sound(MENUSELECT)         # en speel weer een geluid af omdat er geluid is.
            # kijkt 1 laag dieper om te zien of hij in mainmenu of pausemenu zit
            self.set_bg_sounds(self.gamestate.deep_peek().name)

    def flip_music(self):
        """
        Zet muziek aan als het uit staat en vice versa.
        """
        if self.music == 1:
            self.music = 0
            self.stop_bg_music()
        elif self.music == 0:
            self.music = 1
            self.set_bg_music(self.gamestate.deep_peek().name)

    # todo, muziek van mainmenu later in laten komen?
    def set_bg_music(self, currentstate):
        """
        Als mag, fade dan de huidige. Volume max, fade nieuwe muziek in.
        :param currentstate: self.gamestate.peek().name
        """
        # bij options menu moet er niets veranderen, en ook niet als hij van options komt.
        # ook niet als hij van messagebox komt. todo, dit begint wat lelijk te worden.
        if currentstate == statemachine.States.OptionsMenu or \
           self.gamestate.prev_state == statemachine.States.OptionsMenu or \
           self.gamestate.prev_state == statemachine.States.MessageBox:
            return

        if currentstate == statemachine.States.Overworld:
            for _enum in MapMusic:
                # als de naam in de MapMusic overeenkomt met de naam van de huidige map
                if _enum.value[0] == self.gamestate.peek().window.map1.name:
                    # als de muziek in de MapMusic NIET overeenkomt met de muziek van de vorige map
                    if _enum.value[1] != self._get_prev_bg_audio(1):
                        # speel dan de nieuwe muziek
                        self.fade_bg_music()
                        self.bg_music_channel.set_volume(1)
                        self.play_bg_music(_enum.value[1])
                        break
            return

        self.fade_bg_music()
        self.bg_music_channel.set_volume(1)

        if currentstate == statemachine.States.MainMenu:
            # de fade en setvolume staan nu in de if, want bij muziek moet het niet altijd
            self.play_bg_music(TITLESCREEN)

    def _get_prev_bg_audio(self, index):
        for _enum in MapMusic:
            if _enum.value[0] == self.gamestate.peek().window.prev_map_name:
                return _enum.value[index]

    def set_bg_sounds(self, currentstate):
        """
        Zet de achtergrond geluiden aan of uit afhankelijk van een state.
        :param currentstate: self.statemachine.peek()
        """
        if currentstate == statemachine.States.OptionsMenu or \
           self.gamestate.prev_state == statemachine.States.OptionsMenu or \
           self.gamestate.prev_state == statemachine.States.MessageBox:
            return

        if currentstate == statemachine.States.Overworld:
            for _enum in MapMusic:
                if _enum.value[0] == self.gamestate.peek().window.map1.name:
                    if _enum.value[2] != self._get_prev_bg_audio(2):
                        self.fade_bg_sounds()
                        self.bg_sound_channel1.set_volume(1)
                        self.play_sound(_enum.value[2], loop=-1, channel=self.bg_sound_channel1)
                        break
            return

        self.fade_bg_sounds()
        self.bg_sound_channel1.set_volume(1)
        self.bg_sound_channel2.set_volume(1)

        if currentstate == statemachine.States.MainMenu:
            pass
            # self.play_sound(RIVER, loop=-1, channel=self.bg_sound_channel1)
            # self.play_sound(WIND, loop=-1, channel=self.bg_sound_channel2)

    def play_sound(self, sound, loop=0, channel=None):
        """
        Als mag, speel dan geluid.
        :param sound: de naam van het geluidsfragment
        :param loop: -1 is oneindig loopen
        :param channel: het kanaal waar de geluiden op afgespeeld moeten worden, is alleen voor bg_sounds
        """
        if self.sound == 1:
            # als het aangestuurde geluid None is, niets doen natuurlijk.
            if sound:
                if channel:
                    channel.play(self.sfx[sound], loops=loop)
                else:
                    self.sfx[sound].play()

    def play_bg_music(self, music):
        """
        Als mag, speel dan muziek.
        :param music: de naam van het geluidsfragment
        """
        if self.music == 1:
            self.bg_music_channel.play(self.mfx[music], loops=-1)

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
        Speel de juiste voetstap geluiden af op de juiste ondergrond.
        """
        # todo, deze magic numbers moeten nog weg
        sfx_num = str(random.randint(1, 2))
        self.play_sound(self.footstep+sfx_num)
