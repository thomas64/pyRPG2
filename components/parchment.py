
"""
class: Parchment
"""

import pygame

from constants import SFX

from .textbox import TextBox
from .transition import Transition

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'
FONT = 'colonna'
SUBFONT = 'verdana'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50
MIDDLEFONTSIZE = 40
SMALLFONTSIZE = 20
TINYFONTSIZE = 12


class Parchment(object):
    """
    ...
    """
    def __init__(self, engine):
        self.engine = engine

        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.middlefont = pygame.font.SysFont(FONT, MIDDLEFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)
        self.tinyfont = pygame.font.SysFont(SUBFONT, TINYFONTSIZE)

        self.info_label = ""

    def _init_infobox(self, w, h, x, y):
        width = self.screen.get_width() * w
        height = self.screen.get_height() * h
        self.infobox = TextBox((self._set_x(x), self._set_y(y)), int(width), int(height))

    # noinspection PyMissingOrEmptyDocstring
    def on_enter(self):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def on_exit(self):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def single_input(self, event):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def multi_input(self, key_input, mouse_pos, dt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def update(self, dt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def render(self):
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.infobox.render(self.screen, self.info_label)

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

    def _close(self):
        self.engine.audio.play_sound(SFX.scroll)
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
