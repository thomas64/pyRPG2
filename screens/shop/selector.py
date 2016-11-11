
"""
class: Selector
"""

import os

import pygame

LINECOLOR = pygame.Color("black")
SELECTCOLOR = pygame.Color("red")
LINETHICKNESS = 1
PATH = 'resources/sprites/icons/shop/'


class Selector(pygame.sprite.Sprite):
    """
    ...
    """
    def __init__(self, x, y, shop_type):
        super().__init__()

        self.shop_type = shop_type

        # hij komt binnen met een hoofdletter van de enum, maar de bestandsnaam heeft een kleine letter
        self.image = self._load_selected_image(PATH, shop_type.value.lower())
        pygame.draw.rect(self.image, LINECOLOR, self.image.get_rect(), LINETHICKNESS)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    @staticmethod
    def _load_selected_image(path, shop_type):
        """
        Loopt langs alle plaatjes uit de map en controleert of de naam overeenkomt met de opgevraagde type.
        :return: het gevonden plaatje.
        """
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            if name == shop_type:
                return pygame.image.load(os.path.join(path, file)).convert_alpha()

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        if self.rect.collidepoint(event.pos):
            return self.shop_type

    def update(self, shop_type):
        """
        ...
        """
        if shop_type == self.shop_type:
            pygame.draw.rect(self.image, SELECTCOLOR, self.image.get_rect(), LINETHICKNESS)
        else:
            pygame.draw.rect(self.image, LINECOLOR, self.image.get_rect(), LINETHICKNESS)
