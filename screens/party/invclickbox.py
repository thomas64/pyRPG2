
"""
class: InvClickBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXTRANS = 224  # 1-255 hoger is zwarter

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 68
COLUMN4X = 102
COLUMNSY = 0
ROWHEIGHT = 34
EXTRABOXWIDTH = 20
MAXBOXHEIGHT = COLUMNSY + 10 * ROWHEIGHT
ICONOFFSET = 1
TEXTOFFSET = 7
SUBSURW, SUBSURH = 32, 32

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
NORMALFONTSIZE = 15

SCROLLUP = 4
SCROLLDOWN = 5
SCROLLSPEED = 17

BLACK = 'resources/sprites/black.png'


class InvClickBox(object):
    """
    Wanneer je klikt in de inventorybox op een equipment_item_box.
    """
    def __init__(self, position, equipment_type, party, inventory):

        normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        # todo, mousehover fixen, oranje en lichtgroen fixen
        table_data = list()

        black_spr = pygame.image.load(BLACK).convert()

        # de eerste rij
        table_data.append(
            [black_spr, black_spr, "", "Unequip " + equipment_type.value]
        )
        # de rijen van equipment van hero's
        for hero in party:
            # todo, bij rng en rrg en lrg zijn er nog problemen.
            # haal de equipment item op uit het type
            equipment_item = hero.get_equipped_item_of_type(equipment_type)
            if equipment_item:
                # laad de hero subsprite
                hero_spr = pygame.image.load(hero.SPR).subsurface(32, 0, SUBSURW, SUBSURW).convert_alpha()
                # laad de item subsprite
                equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
                # als een equipment item een skill waarde heeft, zoals eigenlijk alleen bij wapens
                if equipment_item.get_value_of('SKL'):
                    # zet dat dan voor de naam
                    equipment_item_nam = "[" + equipment_item.SKL.value + "] " + equipment_item.NAM
                    # maar bij een schild niet, (want die heeft ook een skill waarde, maar niet om zichtbaar te maken
                    if "Shield" in equipment_item_nam:
                        equipment_item_nam = equipment_item.NAM
                else:
                    # en anders gewoon de naam
                    equipment_item_nam = equipment_item.NAM
                table_data.append(
                    [hero_spr, equipment_item_spr, "1", equipment_item_nam]
                )
        # de rijen van equipment uit inventory.
        for equipment_item in inventory.get_all_equipment_items_of_type(equipment_type):
            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
            if equipment_item.get_value_of('SKL'):
                equipment_item_nam = "[" + equipment_item.SKL.value + "] " + equipment_item.NAM
                if "Shield" in equipment_item_nam:
                    equipment_item_nam = equipment_item.NAM
            else:
                equipment_item_nam = equipment_item.NAM
            table_data.append(
                [black_spr, equipment_item_spr, str(equipment_item.qty), equipment_item_nam]
            )

        self.table_view = []
        for index, row in enumerate(table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(row[1])
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR))
            self.table_view[index].append(normalfont.render(row[3], True, FONTCOLOR))

        # bepaal het breedste item wat naam betreft en gebruik dat als boxbreedte
        list_widths = []
        for row in table_data:
            list_widths.append(normalfont.render(row[3], True, FONTCOLOR).get_width())
        self.box_width = max(list_widths) + COLUMN4X + EXTRABOXWIDTH

        # bepaal de boxhoogte
        self.layer_height = COLUMNSY + len(self.table_view) * ROWHEIGHT
        surface_height = self.layer_height
        if surface_height > MAXBOXHEIGHT:
            surface_height = MAXBOXHEIGHT

        self.surface = pygame.Surface((self.box_width, surface_height))
        self.surface.set_alpha(BOXTRANS)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer_offset = 0

        self.background = pygame.Surface((self.box_width, self.layer_height))
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
        # verticale lijnen
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN2X, COLUMNSY), (COLUMN2X, MAXBOXHEIGHT))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN3X, COLUMNSY), (COLUMN3X, MAXBOXHEIGHT))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN4X, COLUMNSY), (COLUMN4X, MAXBOXHEIGHT))

        for index, row in enumerate(self.table_view):
            self.layer.blit(row[0], (COLUMN1X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.layer.blit(row[1], (COLUMN2X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.layer.blit(row[2], (COLUMN3X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.layer.blit(row[3], (COLUMN4X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            # horizontale lijnen
            pygame.draw.line(self.layer, LINECOLOR,
                             (COLUMN1X, COLUMNSY + index * ROWHEIGHT), (self.box_width, COLUMNSY + index * ROWHEIGHT))

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
