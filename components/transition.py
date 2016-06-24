
"""
class Transition
"""

import pygame
import pygame.gfxdraw

from statemachine import GameState

WINDOWW = 900  # todo, dit kan eigenlijk niet. deze waarden zijn gekopieerd uit overworld. dit moet anders.
WINDOWH = 718  # de vraag is hoe kan hij de positie vanuit window meegeven terwijl de positie in overworld bekend is.
WINDOWX = 10
WINDOWY = 40

INCREASE = 150
TOTAL = 75


# noinspection PyMissingOrEmptyDocstring
class Transition(object):
    """
    ...
    """
    def __init__(self, gamestate, full_screen=True):
        self.gamestate = gamestate
        self.screen = pygame.display.get_surface()
        self.surface = self.screen.get_rect()
        if not full_screen:
            self.surface = pygame.Rect(WINDOWX, WINDOWY, WINDOWW, WINDOWH)
        self.name = GameState.FadeBlack
        self.increase = 0
        self.color = (0, 0, 0, self.increase)

    def update(self, dt):
        self.increase += dt * INCREASE
        if self.increase > TOTAL:
            self.gamestate.pop()
            return
        self.color = (0, 0, 0, self.increase)

    def render(self):
        pygame.gfxdraw.box(self.screen, self.surface, self.color)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def single_input(self, event):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        pass
