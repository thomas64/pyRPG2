
"""
class Transition
"""

import pygame
import pygame.gfxdraw

from constants import GameState

WINDOWW = 900  # todo, dit kan eigenlijk niet. deze waarden zijn gekopieerd uit overworld. dit moet anders.
WINDOWH = 718  # de vraag is hoe kan hij de positie vanuit window meegeven terwijl de positie in overworld bekend is.
WINDOWX = 10
WINDOWY = 40

ALPHA = 1250
TIME = 0.7


# noinspection PyMissingOrEmptyDocstring
class Transition(object):
    """
    ...
    """
    def __init__(self, gamestate, full_screen=True):
        self.gamestate = gamestate
        self.screen = pygame.display.get_surface()
        self.rect = self.screen.get_rect()
        if not full_screen:
            self.rect = pygame.Rect(WINDOWX, WINDOWY, WINDOWW, WINDOWH)
        self.name = GameState.FadeBlack
        self.timer = 0
        self.color = (0, 0, 0, 0)

    def update(self, dt):
        self.timer += dt
        if self.timer > TIME:
            self.gamestate.pop()
            return
        new_alpha = ALPHA * dt
        if new_alpha < 0 or new_alpha > 255:
            new_alpha = 0  # soms om een onbekende reden komt hij boven de 255 uit. hiermee is dat afgevangen.
        self.color = (0, 0, 0, new_alpha)

    def render(self):
        pygame.gfxdraw.box(self.screen, self.rect, self.color)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def single_input(self, event):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        pass
