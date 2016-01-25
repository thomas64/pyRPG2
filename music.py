
"""
class: Music
"""

import os

import pygame

import statemachine


MUSICPATH = 'resources/music'
MAINMENUMUSIC = os.path.join(MUSICPATH,  'mainmenu.ogg')
OVERWORLDMUSIC = os.path.join(MUSICPATH, 'overworld.ogg')


class Music(object):
    # todo, optie in hoofmenu om geluid en muziek te kunnen muten
    """
    Alle achtergrondmuziek.
    """
    def __init__(self):
        self.current = pygame.mixer.Channel(7)
        self.mainmenu = pygame.mixer.Sound(MAINMENUMUSIC)
        self.overworld = pygame.mixer.Sound(OVERWORLDMUSIC)

    def play(self, currentstate):
        """
        Zet de volume maximaal.
        Luister naar welke muziek er nu speelt,
        :param currentstate: bovenste state van de stack
        """
        self.current.set_volume(1)
        cur_music = self.current.get_sound()

        if currentstate == statemachine.State.MainMenu:
            if cur_music != self.mainmenu and cur_music is not None:
                self.current.fadeout(1000)
                pygame.time.delay(1000)
            if cur_music != self.mainmenu:
                pygame.time.delay(500)
                self.current.play(self.mainmenu, -1)

        elif currentstate == statemachine.State.PauseMenu:
            if cur_music is not None:
                self.current.fadeout(1000)

        elif currentstate == statemachine.State.OverWorld:
            if cur_music != self.overworld and cur_music is not None:
                self.current.fadeout(1000)
                pygame.time.delay(1000)
            if cur_music != self.overworld:
                pygame.time.delay(500)
                self.current.play(self.overworld, -1)
