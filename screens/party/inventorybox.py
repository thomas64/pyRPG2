
"""
class: InventoryBox
"""

import pygame
import pygame.gfxdraw

from .basebox import BaseBox


LINECOLOR = pygame.Color("white")

TITLEX, TITLEY = 7, 1

TITLE = "Inventory"
STICKMANPATH = "resources/sprites/stickman.png"
STICKMANPOS = 60
EQUIPMENTITEMBOXCOLOR = (100, 0, 0, 128)
WPNBOX = pygame.Rect(77,  165, 33, 33)
SLDBOX = pygame.Rect(213, 165, 33, 33)
HLMBOX = pygame.Rect(143,  70, 33, 33)
AMUBOX = pygame.Rect(143, 130, 33, 33)
ARMBOX = pygame.Rect(160, 165, 33, 33)
CLKBOX = pygame.Rect(128, 165, 33, 33)
BRCBOX = pygame.Rect(77,  197, 33, 33)
GLVBOX = pygame.Rect(77,  229, 33, 33)
RNGBOX = pygame.Rect(213, 229, 33, 33)
BLTBOX = pygame.Rect(143, 207, 33, 33)
BTSBOX = pygame.Rect(143, 270, 33, 33)
ACYBOX = pygame.Rect(213, 197, 33, 33)
# de volgorde van deze lijst is belangrijk. hij moet gelijk zijn aan Hero.equipment_tuple()
EQUIPMENTITEMBOXES = (WPNBOX, SLDBOX, HLMBOX, AMUBOX, ARMBOX, CLKBOX, BRCBOX, GLVBOX, RNGBOX, BLTBOX, BTSBOX, ACYBOX)
SUBSURW, SUBSURH = 32, 32


class InventoryBox(BaseBox):
    """
    Alle weergegeven informatie van alle inventory van de party.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()
        self.stickman = pygame.image.load(STICKMANPATH).convert()
        self.equipment_item_sprites = []
        self.equipment_items = []

        # stel de offset in voor de boxen in een copy() van de BOXLIJST
        self.offset_boxes = []
        for BOX in EQUIPMENTITEMBOXES:
            self.offset_boxes.append(BOX.copy())  # zonder .copy() stelt hij de offset in voor de originele rects
        for box in self.offset_boxes:
            box.topleft = self.rect.left + box.left, self.rect.top + box.top

    def mouse_hover(self, event):
        """
        Registreert of de muis over een boxje beweegt. Gebruik hiervoor de self.offset_boxes.
        Haal dan uit de equipment_items lijst het item. Die was er bij update() in gestopt.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: visuele weergave uit equipment_item.show_info(), of niets.
        """
        for index, box in enumerate(self.offset_boxes):
            if box.collidepoint(event.pos):
                equipment_item = self.equipment_items[index]
                if equipment_item.is_not_empty():
                    return equipment_item.show_info()
                return None

    def mouse_click(self, event):
        """
        Registreert of de muis op het boxje klikt. Gebruik hiervoor de self.offset_boxes.
        Deze moet van de display de muispositie en het EquipmentType teruggeven.
        Daar vraagt display om, zodat er een clickbox opgezet kan worden.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :return: None als er mis geklikt wordt.
        """
        for index, box in enumerate(self.offset_boxes):
            if box.collidepoint(event.pos):
                equipment_item = self.equipment_items[index]
                return event.pos, equipment_item.TYP
        return None, None

    def update(self, hero):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        """
        self.equipment_item_sprites = []
        self.equipment_items = []
        for equipment_item in hero.equipment_tuple:
            if equipment_item.is_not_empty():
                # laat het gekozen icon zien van de equipment item
                self.equipment_item_sprites.append(pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha())
            else:
                # of anders een lege surface
                self.equipment_item_sprites.append(pygame.Surface((0, 0)))
            # en voeg de equipment items toe aan een aparte lijst.
            self.equipment_items.append(equipment_item)

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

        for index, BOX in enumerate(EQUIPMENTITEMBOXES):
            # teken een doorzichtige box
            pygame.gfxdraw.box(self.surface, BOX, EQUIPMENTITEMBOXCOLOR)
            # teken het lijntje eromheen
            pygame.draw.rect(self.surface, LINECOLOR, BOX, 1)
            # teken de icon
            self.surface.blit(self.equipment_item_sprites[index], BOX)

        screen.blit(self.surface, self.rect.topleft)
