
"""
class: Display
"""

import pygame

import keys
import screens.shop.buybox
import screens.shop.sellbox
import statemachine

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'

BUYBOXWIDTH = 1/4
BUYBOXHEIGHT = 2/3
BUYBOXPOSX = 1/3
BUYBOXPOSY = 1/6

SELLBOXWIDTH = 1/4      # van het scherm
SELLBOXHEIGHT = 2/3
SELLBOXPOSX = 2/3       # x op 2/3 van het scherm
SELLBOXPOSY = 1/6


class Display(object):
    """
    ...
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.name = statemachine.States.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self._init_boxes()

    def _init_boxes(self):
        width = self.screen.get_width() * SELLBOXWIDTH
        height = self.screen.get_height() * SELLBOXHEIGHT
        x = self.screen.get_width() * SELLBOXPOSX
        y = self.screen.get_height() * SELLBOXPOSY
        self.sellbox = screens.shop.sellbox.SellBox(x, y, width, height)
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT
        x = self.screen.get_width() * BUYBOXPOSX
        y = self.screen.get_height() * BUYBOXPOSY
        self.buybox = screens.shop  .buybox.BuyBox(x, y, width, height)

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Teken
        """
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
