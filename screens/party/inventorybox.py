
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

    def _update(self, hero):
        self.title = self.largefont.render(TITLE, True, FONTCOLOR)
        self.stickman = pygame.image.load(STICKMANPATH).convert()

        self.equipment_item_sprites = []
        for equipment_item in hero.equipment_tuple:
            # todo, de 'and' voorwaarde mag weg wanneer alle equipment een spritepath gekregen heeft.
            if equipment_item.is_not_empty() and equipment_item.SPR:
                # laat het gekozen icon zien van de equipment item
                self.equipment_item_sprites.append(pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha())
            else:
                self.equipment_item_sprites.append(pygame.Surface((0, 0)))

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

    def mouse_click(self, event, hero):
        """
        Deze moet van de display de muispositie en het EquipmentType teruggeven. Daar vraagt display om, zodat er een
        clickbox opgezet kan worden.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        :param hero: self.cur_hero uit party/display.py
        :return: None als er mis geklikt wordt.
        """
        rel_pos_x = event.pos[0] - self.rect.left
        rel_pos_y = event.pos[1] - self.rect.top
        if WPNBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.wpn.TYP
        elif SLDBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.sld.TYP
        elif HLMBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.hlm.TYP
        elif AMUBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.amu.TYP
        elif ARMBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.arm.TYP
        elif CLKBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.clk.TYP
        elif GLVBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.glv.TYP
        elif LRGBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.lrg.TYP
        elif RRGBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.rrg.TYP
        elif BLTBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.blt.TYP
        elif BTSBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.bts.TYP
        elif ACYBOX.collidepoint(rel_pos_x, rel_pos_y):
            return event.pos, hero.acy.TYP
        return None, None
