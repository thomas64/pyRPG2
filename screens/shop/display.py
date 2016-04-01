
"""
class: Display
"""

import pygame

import statemachine

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'


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

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def single_input(self, event):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass