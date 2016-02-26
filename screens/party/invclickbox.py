
"""
class: InvClickBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 250
MAXBOXHEIGHT = 250
STARTBOXHEIGHT = 15
EXTRABOXHEIGHT = 15
BOXTRANS = 224  # 1-255 hoger is zwarter

ROWPOSX, ROWPOSY = 10, 15
ROWHEIGHT = 35

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
NORMALFONTSIZE = 15

SCROLLUP = 4
SCROLLDOWN = 5
SCROLLSPEED = 10


class InvClickBox(object):
    """
    Wanneer je klikt in de inventorybox op een equipment_item_box.
    """
    def __init__(self, position, equipment_type, party, inventory):

        normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        # todo, icons fixen, mousehover fixen, oranje en lichtgroen fixen
        table_data = list()
        table_data.append("{} {} {} {}".format("", "", "Unequip " + equipment_type.value, ""))

        for hero in party:
            # todo, bij rng en rrg en lrg zijn er nog problemen.
            equipment_item = hero.get_equipped_item_of_type(equipment_type)
            if equipment_item:
                table_data.append("{} {} {} {}".format(hero.NAM, "Icon", "1", equipment_item.NAM))

        for equipment_item in inventory.get_all_equipment_items_of_type(equipment_type):
            table_data.append("{} {} {} {}".format("X", "Icon", equipment_item.qty, equipment_item.NAM))

        self.table_view = []
        for index, row in enumerate(table_data):
            self.table_view.append(normalfont.render(row, True, FONTCOLOR))

        # todo, row hoogte gewoon op index bepalen. het kan namelijk makkelijker.

        surface_height = STARTBOXHEIGHT
        self.layer_height = 0
        for row in self.table_view:
            surface_height += row.get_height() + EXTRABOXHEIGHT
            self.layer_height = surface_height
        if surface_height > MAXBOXHEIGHT:
            surface_height = MAXBOXHEIGHT

        self.surface = pygame.Surface((BOXWIDTH, surface_height))
        self.surface.set_alpha(BOXTRANS)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.layer = pygame.Surface((BOXWIDTH, self.layer_height))
        self.layer_offset = 0

        self.background = pygame.Surface((BOXWIDTH, self.layer_height))
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

    def draw(self, screen):
        """
        Surface tekent layer, de rest gaat op de layer, en screen tekent de surface.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.layer, (0, self.layer_offset))
        self.layer.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)

        for index, row in enumerate(self.table_view):
            self.layer.blit(row, (ROWPOSX, ROWPOSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)

    def mouse_scroll(self, event):
        """
        Registreert of scrolwiel gebruikt wordt. Verplaatst de layer dan omhoog of omlaag.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        """
        if event.button == SCROLLUP:
            if self.layer_offset < 0:
                self.layer_offset += SCROLLSPEED
        elif event.button == SCROLLDOWN:
            if self.layer_offset > (self.rect.height - self.layer_height):
                self.layer_offset -= SCROLLSPEED
