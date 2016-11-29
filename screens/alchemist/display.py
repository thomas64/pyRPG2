
"""
class: Display
"""

import pygame

from components import Button
from components import Transition
from constants import GameState
from constants import Keys


BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'
COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(object):
    """
    ...
    """
    def __init__(self, engine):
        self.engine = engine

        self.screen = pygame.display.get_surface()
        self.name = GameState.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        if event.type == pygame.MOUSEMOTION:
            pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == Keys.Leftclick.value:
                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        ...
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        ...
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Teken alles op het scherm.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.close_button.render(self.screen, FONTCOLOR, True)

    def _close(self):
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
