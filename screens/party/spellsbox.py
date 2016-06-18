
"""
class: SpellsBox
"""

import pygame

from screens.party.basebox import BaseBox


LINECOLOR = pygame.Color("white")

TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 220
COLUMNSY = 60
ROWHEIGHT = 30
ICONOFFSET = -6


TITLE = "Spells"


class SpellsBox(BaseBox):
    """
    Alle weergegeven informatie van alle spells van een hero.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = None

    def update(self, hero):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        """
        self.title = self.largefont.render(
                                    "{} {}".format(hero.scl.NAM.value, TITLE), True, self.fontcolor1).convert_alpha()

        self.table_data = []
        for spell in hero.scl.get_all_spells():
            self.table_data.append(
                # row[0],       row[1],           row[2],     row[3],  row[4],     row[5],    row[6]
                [spell.ICON, spell.NAM + " :", str(spell.qty), None, spell.DESC, spell.COL, spell.ROW]
            )

        # vul row[3] kolom. hierin staan de rects van row[1]. rect is voor muisklik.
        for index, row in enumerate(self.table_data):
            row[3] = self._create_rect_with_offset(index, row[1], COLUMN2X, COLUMNSY, ROWHEIGHT)

        # maak dan een nieuwe tabel aan met de tekst en icons, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).subsurface(row[5], row[6], 32, 32).convert())
            self.table_view[index].append(self.normalfont.render(row[1], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, self.fontcolor1).convert_alpha())

    def render(self, screen):
        """
        En teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[0], (COLUMN1X, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.surface.blit(row[1], (COLUMN2X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[2], (COLUMN3X, COLUMNSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
