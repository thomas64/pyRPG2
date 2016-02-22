
"""
class: InventoryBox
"""

import pygame
import pygame.gfxdraw

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 315
BOXHEIGHT = 670
TITLEX, TITLEY = 7, 1

TITLE = "Inventory"
STICKMANPATH = "resources/sprites/stickman.png"
STICKMANPOS = 60
GEARBOXCOLOR = (100, 0, 0, 128)
WPNBOX = pygame.Rect(70,  165, 33, 33)
SLDBOX = pygame.Rect(206, 165, 33, 33)
HLMBOX = pygame.Rect(136,  70, 33, 33)
AMUBOX = pygame.Rect(136, 130, 33, 33)
ARMBOX = pygame.Rect(153, 165, 33, 33)
CLKBOX = pygame.Rect(121, 165, 33, 33)
GLVBOX = pygame.Rect(70,  197, 33, 33)
LRGBOX = pygame.Rect(206, 229, 33, 33)
RRGBOX = pygame.Rect(70,  229, 33, 33)
BLTBOX = pygame.Rect(136, 207, 33, 33)
BTSBOX = pygame.Rect(136, 270, 33, 33)
ACYBOX = pygame.Rect(206, 197, 33, 33)
GEARBOXES = (WPNBOX, SLDBOX, HLMBOX, AMUBOX, ARMBOX, CLKBOX, GLVBOX, LRGBOX, RRGBOX, BLTBOX, BTSBOX, ACYBOX)

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class InventoryBox(object):
    """
    Alle weergegeven informatie van alle inventory van de party.
    """
    def __init__(self, position):
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

    def _update(self, hero):
        self.title = self.largefont.render(TITLE, True, FONTCOLOR)
        self.stickman = pygame.image.load(STICKMANPATH)

        self.gear_sprites = []
        for gear in hero.equipment_tuple:
            # todo, de 'and' voorwaarde mag weg wanneer alle gear een sprite gekregen heeft.
            if hasattr(gear, 'SPR') and gear.SPR:
                self.gear_sprites.append(pygame.image.load(gear.SPR).subsurface(gear.COL, gear.ROW, 32, 32))
            else:
                self.gear_sprites.append(pygame.Surface((0, 0)))

    def draw(self, screen, hero):
        """
        Update eerst de data, en teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        :param hero: de huidige geselecteerde hero
        """
        self._update(hero)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))
        self.surface.blit(self.stickman, ((self.surface.get_width() - self.stickman.get_width()) / 2, STICKMANPOS))
        for index, box in enumerate(GEARBOXES):
            pygame.gfxdraw.box(self.surface, box, GEARBOXCOLOR)
            pygame.draw.rect(self.surface, LINECOLOR, box, 1)
            self.surface.blit(self.gear_sprites[index], box)

        screen.blit(self.surface, self.rect.topleft)
