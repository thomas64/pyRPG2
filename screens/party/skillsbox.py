
"""
class: SkillsBox
"""

import pygame


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 315
BOXHEIGHT = 670
TITLEX, TITLEY = 7, 1
COLUMN1X = 40
COLUMN2X = 80
COLUMN3X = 200
COLUMN4X = 230
COLUMNSY = 60
ROWHEIGHT = 33

TITLE = "Skills"

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

POSCOLOR = pygame.Color("green")
NEGCOLOR = pygame.Color("red")


class SkillsBox(object):
    """
    Alle weergegeven informatie van alle skills van een hero.
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

        self.cur_item = None

    def _update(self, hero):
        self.title = self.largefont.render(TITLE, True, FONTCOLOR1)

        self.table_data = []

        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                self.table_data.append(
                    [skill.ICON,  str(skill.NAM) + " :",  str(skill.qty),  skill.ext,   None,   skill.DESC]
                )

        # vul de vijfde lege kolom. hierin staan de rects van de tweede kolom. rect is voor muisklik.
        for index, row in enumerate(self.table_data):
            row[4] = self._rect(index, row[1])

        # maak dan een nieuwe tabel aan met de tekst, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]))
            if index == self.cur_item:              # als de index van deze rij gelijk is aan waar de muis over zit,
                color = FONTCOLOR2                  # maak hem geel
            else:                                   # anders gewoon wit.
                color = FONTCOLOR1
            self.table_view[index].append(self.normalfont.render(row[1], True, color))
            self.table_view[index].append(self.normalfont.render(row[2], True, FONTCOLOR1))
            self._line(row[3], self.table_view[index])

    def _rect(self, index, text):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + COLUMN1X, (self.rect.top + COLUMNSY) + index * ROWHEIGHT
        return rect

    def _line(self, value, col):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param col: in welke kolom de regel zich bevind
        """
        if value == "":
            value = 0
        if value == 0:
            value = ""
            col.append(self.normalfont.render(value, True, FONTCOLOR1))
        elif value > 0:
            value = "(+"+str(value)+")"
            col.append(self.normalfont.render(value, True, POSCOLOR))
        elif value < 0:
            value = "("+str(value)+")"
            col.append(self.normalfont.render(value, True, NEGCOLOR))

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
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[0], (COLUMN1X, COLUMNSY - 5 + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[1], (COLUMN2X, COLUMNSY + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[2], (COLUMN3X, COLUMNSY + index * ROWHEIGHT))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[3], (COLUMN4X, COLUMNSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
