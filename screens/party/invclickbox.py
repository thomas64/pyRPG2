
"""
class: InvClickBox
"""

import pygame

import equipment
import keys

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")
SELECTCOLOR = pygame.Color("gray24")

BOXTRANS = 224  # 1-255 hoger is zwarter

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 68
COLUMN4X = 102
COLUMNSY = 0
ROWHEIGHT = 34
EXTRABOXWIDTH = 20
MAXBOXHEIGHT = COLUMNSY + 9.5 * ROWHEIGHT       # 9.5 zodat er een halve zichtbaar is
ICONOFFSET = 1
TEXTOFFSET = 7
SUBSURW, SUBSURH = 32, 32

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
NORMALFONTSIZE = 15

SCROLLSPEED = 17

TRANSP = 'resources/sprites/transp.png'


class InvClickBox(object):
    """
    Wanneer je klikt in de inventorybox op een equipment_item_box.
    """
    def __init__(self, position, equipment_type, party, inventory):

        normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.equipment_type = equipment_type
        self.inventory = inventory

        self.table_data = list()

        black_spr = pygame.image.load(TRANSP).convert_alpha()

        # de eerste rij
        empty_equipment_item = equipment.EquipmentType.get_empty_equipment_item_of_this_type(self.equipment_type)
        self.table_data.append(
            # row[0],   row[1],  row[2],        row[3],                   row[4],         row[5]
            [black_spr, black_spr, "", "Unequip " + self.equipment_type, empty_equipment_item, None]
        )
        # de rijen van equipment van hero's
        for hero in party:
            # todo, bij rng en rrg en lrg zijn er nog problemen.
            # haal de equipment item op uit het type
            equipment_item = hero.get_equipped_item_of_type(self.equipment_type)
            if equipment_item.is_not_empty():
                # laad de hero subsprite
                hero_spr = pygame.image.load(hero.SPR).subsurface(32, 0, SUBSURW, SUBSURW).convert_alpha()
                # laad de item subsprite
                equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
                # als een equipment item een skill waarde heeft, zoals eigenlijk alleen bij wapens
                if equipment_item.get_value_of('SKL'):
                    # zet dat dan voor de naam
                    equipment_item_nam = "[" + equipment_item.SKL + "] " + equipment_item.NAM
                    # maar bij een schild niet, (want die heeft ook een skill waarde, maar niet om zichtbaar te maken
                    if "Shield" in equipment_item_nam:
                        equipment_item_nam = equipment_item.NAM
                else:
                    # en anders gewoon de naam
                    equipment_item_nam = equipment_item.NAM
                self.table_data.append(
                    # row[0],       row[1],       row[2],     row[3],           row[4],     row[5]
                    [hero_spr, equipment_item_spr, "1", equipment_item_nam, equipment_item, None]
                )
        # de rijen van equipment uit inventory.
        for equipment_item in self.inventory.get_all_equipment_items_of_type(self.equipment_type):
            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                            equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
            if equipment_item.get_value_of('SKL'):
                equipment_item_nam = "[" + equipment_item.SKL + "] " + equipment_item.NAM
                if "Shield" in equipment_item_nam:
                    equipment_item_nam = equipment_item.NAM
            else:
                equipment_item_nam = equipment_item.NAM
            self.table_data.append(
                # row[0],        row[1],            row[2],                     row[3],          row[4],     row[5]
                [black_spr, equipment_item_spr, str(equipment_item.qty), equipment_item_nam, equipment_item, None]
            )

        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(row[1])
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[3], True, FONTCOLOR).convert_alpha())

        # bepaal het breedste item wat naam betreft en gebruik dat als boxbreedte
        list_widths = []
        for row in self.table_data:
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
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = position

        self.background = pygame.Surface((self.box_width, self.layer_height))
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.cur_item = None

        self._update_rects_in_layer_rect_with_offset()

    def _update_rects_in_layer_rect_with_offset(self):
        """
        Voeg de rects toe in row[5] van table_data waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.table_data):
            row[5] = pygame.Rect(self.lay_rect.x + COLUMN1X, self.lay_rect.y + COLUMNSY + index * ROWHEIGHT,
                                 self.box_width, ROWHEIGHT+1)

    def mouse_scroll(self, event):
        """
        Registreert of scrolwiel gebruikt wordt. Verplaatst de layer dan omhoog of omlaag.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        """
        if event.button == keys.SCROLLUP:
            if self.lay_rect.y - self.rect.y < 0:
                self.lay_rect.y += SCROLLSPEED
        elif event.button == keys.SCROLLDOWN:
            if self.lay_rect.y - self.rect.y > self.rect.height - self.layer_height:
                self.lay_rect.y -= SCROLLSPEED

        self._update_rects_in_layer_rect_with_offset()

    def mouse_hover(self, event):
        """
        Als de muis over een item uit row[5] van table_data gaat. Dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: row[4] is de kolom met het Object EquipmentItem.
        """
        for index, row in enumerate(self.table_data):
            if row[5].collidepoint(event.pos):
                self.cur_item = index
                equipment_item = row[4]
                if equipment_item.is_not_empty():
                    return equipment_item.display(), equipment_item
                return None, equipment_item

    def mouse_click(self, event, hero):
        """
        Equip het geselecteerde item.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :param hero: de huidige geselecteerde hero uit partyscreen
        """
        for index, row in enumerate(self.table_data):
            if row[5].collidepoint(event.pos):
                self.cur_item = index
                selected_item = row[4]
                equipped_item = hero.get_equipped_item_of_type(self.equipment_type)

                # equip
                # als de geselecteerde geen lege is
                if selected_item.is_not_empty():
                    # als de geselecteerde niet dezelfde is als die je al aan hebt
                    if selected_item.get_value_of('RAW') != equipped_item.get_value_of('RAW'):
                        # als hij in de inventory zit
                        if self.inventory.contains(selected_item):
                            # als het aankleden gelukt is
                            if hero.set_equipment_item(selected_item):
                                # verwijder hem dan uit de inventory
                                self.inventory.remove(selected_item)
                                # als degene die je aan had niet een lege is
                                if equipped_item.is_not_empty():
                                    # voeg die dan toe aan de inventory
                                    self.inventory.add(equipped_item)

                # unequip
                # als de geselecteerde wel een lege is
                else:
                    # als degene die je al aan hebt geen lege is
                    if equipped_item.is_not_empty():
                        # trek dan de lege aan
                        hero.set_equipment_item(selected_item)
                        # en voeg degene die je aan had toe aan de inventory
                        self.inventory.add(equipped_item)

    def render(self, screen):
        """
        Surface tekent layer, de rest gaat op de layer, en screen tekent de surface.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.layer, (0, self.lay_rect.y - self.rect.y))
        self.layer.blit(self.background, (0, 0))
        # omranding
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)
        # verticale lijnen
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN2X, COLUMNSY), (COLUMN2X, MAXBOXHEIGHT))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN3X, COLUMNSY), (COLUMN3X, MAXBOXHEIGHT))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN4X, COLUMNSY), (COLUMN4X, MAXBOXHEIGHT))

        # horizontale vierkanten
        for index, row in enumerate(self.table_view):
            if index == self.cur_item:
                pygame.draw.rect(self.layer, SELECTCOLOR,
                                 (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 0)
            pygame.draw.rect(self.layer, LINECOLOR,
                             (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 1)

        for index, row in enumerate(self.table_view):
            self.layer.blit(row[0], (COLUMN1X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[1], (COLUMN2X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[2], (COLUMN3X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[3], (COLUMN4X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
