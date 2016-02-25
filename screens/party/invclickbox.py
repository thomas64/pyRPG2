
"""
class: InvClickBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class InvClickBox(object):
    """
    Wanneer je klikt in de inventorybox op een gear.
    """
    def __init__(self, position, equipment_type):
        self.surface = pygame.Surface((300, 200))
        self.surface.set_alpha(224)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.equipment_type = equipment_type

    def _update(self, party, inventory):

        self.table_data = []
        self.table_data.append("{} {} {} {}".format("", "", "Unequip " + self.equipment_type.value, ""))

        for hero in party:
            # todo, bij rng en rrg en lrg zijn er nog problemen.
            equipment_item = hero.get_equipped_item_of_type(self.equipment_type)
            if equipment_item:
                self.table_data.append("{} {} {} {}".format(hero.NAM, "Icon", "1", equipment_item.NAM))

        for equipment_item in inventory.get_all_equipment_items_of_type(self.equipment_type):
            self.table_data.append("{} {} {} {}".format("X", "Icon", equipment_item.qty, equipment_item.NAM))

        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(self.normalfont.render(row, True, FONTCOLOR))

    def draw(self, screen, party, inventory):

        self._update(party, inventory)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        for index, row in enumerate(self.table_view):
            self.surface.blit(row, (10, 10 + index * 35))

        screen.blit(self.surface, self.rect.topleft)

    def mouse_scroll(self, event):

        # todo, scrollen door het vakje maken

        if event.button == 4:
            self.rect = self.rect.move(0, -1)
        elif event.button == 5:
            print("Down")
        else:
            print("Error")
