
"""
class: InventoryBox
"""

import pygame
import pygame.gfxdraw

import equipment

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 329
BOXHEIGHT = 640
TITLEX, TITLEY = 7, 1

TITLE = "Inventory"
STICKMANPATH = "resources/sprites/stickman.png"
STICKMANPOS = 60
EQUIPMENTITEMBOXCOLOR = (100, 0, 0, 128)
WPNBOX = pygame.Rect(77,  165, 33, 33), equipment.WeaponDatabase.factory(None)
SLDBOX = pygame.Rect(213, 165, 33, 33), equipment.ShieldDatabase.factory(None)
HLMBOX = pygame.Rect(143,  70, 33, 33), equipment.HelmetDatabase.factory(None)
AMUBOX = pygame.Rect(143, 130, 33, 33), equipment.AmuletDatabase.factory(None)
ARMBOX = pygame.Rect(160, 165, 33, 33), equipment.ArmorDatabase.factory(None)
CLKBOX = pygame.Rect(128, 165, 33, 33), equipment.CloakDatabase.factory(None)
GLVBOX = pygame.Rect(77,  197, 33, 33), equipment.GlovesDatabase.factory(None)
LRGBOX = pygame.Rect(213, 229, 33, 33), equipment.RingDatabase.factory(None)
RRGBOX = pygame.Rect(77,  229, 33, 33), equipment.RingDatabase.factory(None)
BLTBOX = pygame.Rect(143, 207, 33, 33), equipment.BeltDatabase.factory(None)
BTSBOX = pygame.Rect(143, 270, 33, 33), equipment.BootsDatabase.factory(None)
ACYBOX = pygame.Rect(213, 197, 33, 33), equipment.AccessoryDatabase.factory(None)
# de volgorde van deze lijst is belangrijk. hij moet gelijk zijn aan Hero.equipment_tuple()
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
        self.equipment_items = []

        # stel de offset in voor de boxen in een self.kopie van de BOXLIJST
        self.offset_boxes = []
        for BOX in EQUIPMENTITEMBOXES:
            self.offset_boxes.append(BOX[0].copy())  # zonder .copy() stelt hij de offset in voor de originele rects
        for box in self.offset_boxes:
            box.topleft = self.rect.left + box.left, self.rect.top + box.top

    def mouse_hover(self, event):
        """
        Registreert of de muis over een boxje beweegt. Gebruik hiervoor de self.offset_boxes.
        Haal dan uit de equipment_items lijst het item. Die was er bij update() in gestopt.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: visuele weergave uit equipment_item.display(), of niets.
        """
        for index, box in enumerate(self.offset_boxes):
            if box.collidepoint(event.pos):
                equipment_item = self.equipment_items[index]
                if equipment_item.is_not_empty():
                    return equipment_item.display()
                return None

    def mouse_click(self, event):
        """
        Registreert of de muis op het boxje klikt. Gebruik hiervoor de self.offset_boxes.
        Deze moet van de display de muispositie en een lege EquipmentItem teruggeven.
        Daar vraagt display om, zodat er een clickbox opgezet kan worden.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :return: None als er mis geklikt wordt.
        """
        for index, box in enumerate(self.offset_boxes):
            if box.collidepoint(event.pos):
                return event.pos, EQUIPMENTITEMBOXES[index][1]
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
            pygame.gfxdraw.box(self.surface, BOX[0], EQUIPMENTITEMBOXCOLOR)
            # teken het lijntje eromheen
            pygame.draw.rect(self.surface, LINECOLOR, BOX[0], 1)
            # teken de icon
            self.surface.blit(self.equipment_item_sprites[index], BOX[0])

        screen.blit(self.surface, self.rect.topleft)
