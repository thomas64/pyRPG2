
"""
class: Selector
"""

import os

import pygame


LINECOLOR = pygame.Color("black")
PATH = 'resources/sprites/heroes/'

SPRITEPOSX = 32
SPRITEPOSY = 0
SPRITESIZE = 32


class Selector(pygame.sprite.Sprite):
    """
    ...
    """
    def __init__(self, x, y, hero):
        super().__init__()

        self.hero = hero

        self.image = self._load_selected_image(PATH, hero.NAM.lower())
        pygame.draw.rect(self.image, LINECOLOR, self.image.get_rect(), 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    @staticmethod
    def _load_selected_image(path, hero_name):
        """
        Loopt langs alle plaatjes uit de map en controleert of de naam overeenkomt met de opgevraagde type.
        :return: het gevonden plaatje.
        """
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            if name.startswith('s_', 2, 4):
                if name[4:] == hero_name:
                    return pygame.image.load(os.path.join(path, file)).subsurface(SPRITEPOSX, SPRITEPOSY, SPRITESIZE,
                                                                                  SPRITESIZE).convert_alpha()

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        if self.rect.collidepoint(event.pos):
            return self.hero
