
"""
class: Selector
"""

import os

import pygame

LINECOLOR = pygame.Color("black")
PATH = 'resources/sprites/icons/shop/'


class Selector(pygame.sprite.Sprite):
    """
    ...
    """
    def __init__(self, x, y, shop_type):
        super().__init__()

        self.shop_type = shop_type

        # hij komt binnen met een hoofdletter van de enum, maar de bestandsnaam heeft een kleine letter
        self.image = self._load_all_images(PATH)[shop_type.value.lower()]
        pygame.draw.rect(self.image, LINECOLOR, self.image.get_rect(), 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    @staticmethod
    def _load_all_images(path):
        """
        Laadt alle plaatjes uit de map in een dict.
        :return: de dict
        """
        images = {}
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            images[name] = pygame.image.load(os.path.join(path, file)).convert_alpha()
        return images

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        if self.rect.collidepoint(event.pos):
            return self.shop_type
