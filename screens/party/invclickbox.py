
"""
class: InvClickBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")

LINECOLOR = pygame.Color("white")


class InvClickBox(object):
    """
    Wanneer je klikt in de inventorybox op een gear.
    """
    def __init__(self, position, gear):
        self.surface = pygame.Surface((200, 200))
        self.surface.set_alpha(224)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

    def draw(self, screen, hero):

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)



        screen.blit(self.surface, self.rect.topleft)
