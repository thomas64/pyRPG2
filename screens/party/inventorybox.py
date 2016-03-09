
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
EQUIPMENTITEMBOXCOLOR = (100, 0, 0, 128)
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
EQUIPMENTITEMBOXES = (WPNBOX, SLDBOX, HLMBOX, AMUBOX, ARMBOX, CLKBOX, GLVBOX, LRGBOX, RRGBOX, BLTBOX, BTSBOX, ACYBOX)
SUBSURW, SUBSURH = 32, 32

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

        self.title = self.largefont.render(TITLE, True, FONTCOLOR).convert_alpha()
        self.stickman = pygame.image.load(STICKMANPATH).convert()
        self.equipment_item_sprites = []

    def mouse_hover(self, event, hero):
        """
        Registreert of de muis over een boxje beweegt. Vergelijkt dan met TYP uit equipment_tuple om de juiste te vinden
        :param event: pygame.MOUSEMOTION uit partyscreen
        :param hero: self.cur_hero uit party/display.py
        :return: visuele weergave uit equipment_item.display(), of niets.
        """
        rel_pos_x = event.pos[0] - self.rect.left
        rel_pos_y = event.pos[1] - self.rect.top
        for index, box in enumerate(EQUIPMENTITEMBOXES):
            if box.collidepoint(rel_pos_x, rel_pos_y):
                equipment_item = hero.get_equipped_item_of_type(hero.equipment_tuple[index].TYP)
                if equipment_item:
                    return equipment_item.display()
        return None

    def mouse_click(self, event, hero):
        """
        Deze moet van de display de muispositie en het EquipmentType teruggeven. Daar vraagt display om, zodat er een
        clickbox opgezet kan worden.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :param hero: self.cur_hero uit party/display.py
        :return: None als er mis geklikt wordt.
        """
        rel_pos_x = event.pos[0] - self.rect.left
        rel_pos_y = event.pos[1] - self.rect.top
        for index, box in enumerate(EQUIPMENTITEMBOXES):
            if box.collidepoint(rel_pos_x, rel_pos_y):
                return event.pos, hero.equipment_tuple[index].TYP
        return None, None

    def update(self, hero):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        """
        self.equipment_item_sprites = []
        for equipment_item in hero.equipment_tuple:
            if equipment_item.is_not_empty():
                # laat het gekozen icon zien van de equipment item
                self.equipment_item_sprites.append(pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha())
            else:
                # of anders een lege surface
                self.equipment_item_sprites.append(pygame.Surface((0, 0)))

    def render(self, screen):
        """
        En teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))
        # positioneer stickman in het midden
        self.surface.blit(self.stickman, ((self.surface.get_width() - self.stickman.get_width()) / 2, STICKMANPOS))

        for index, box in enumerate(EQUIPMENTITEMBOXES):
            # teken een doorzichtige box
            pygame.gfxdraw.box(self.surface, box, EQUIPMENTITEMBOXCOLOR)
            # teken het lijntje eromheen
            pygame.draw.rect(self.surface, LINECOLOR, box, 1)
            # teken de icon
            self.surface.blit(self.equipment_item_sprites[index], box)

        screen.blit(self.surface, self.rect.topleft)
