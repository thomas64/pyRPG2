
"""
class: SkillsBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 329
BOXHEIGHT = 640
TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 190
COLUMN4X = 220
COLUMN5X = 250
COLUMNSY = 60
ROWHEIGHT = 30
ICONOFFSET = -6

TITLE = "Skills"

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

POSCOLOR1 = pygame.Color("green")
POSCOLOR2 = pygame.Color("lightgreen")
NEGCOLOR1 = pygame.Color("red")
NEGCOLOR2 = pygame.Color("orangered")


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

        self.title = self.largefont.render(TITLE, True, FONTCOLOR1).convert_alpha()
        self.table_data = []
        self.table_view = []

    def mouse_hover(self, event):
        """
        Als de muis over een item in de uit row[4] geregistreerde rects gaat.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: row[5] is de kolom met de info.
        """
        self.cur_item = None
        for index, row in enumerate(self.table_data):
            if row[4].collidepoint(event.pos):
                self.cur_item = index
                return row[5]

    def update(self, hero, hovered_equipment_item):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        :param hovered_equipment_item: het item waar de muis overheen hovered in invclickbox
        """
        self.table_data = []
        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                preview_value = self._get_difference(hero, hovered_equipment_item, skill)
                self.table_data.append(
                    # row[0],       row[1],           row[2],       row[3],  row[4],  row[5],     row[6]
                    [skill.ICON, skill.NAM + " :", str(skill.qty), skill.ext, None, skill.DESC, preview_value]
                )

        # vul de vijfde lege kolom. hierin staan de rects van de tweede kolom. rect is voor muisklik.
        for index, row in enumerate(self.table_data):
            row[4] = self._create_rect_with_offset(index, row[1])

        # maak dan een nieuwe tabel aan met de tekst en icons, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).convert_alpha())
            if index == self.cur_item:              # als de index van deze rij gelijk is aan waar de muis over zit,
                color = FONTCOLOR2                  # maak hem geel
            else:                                   # anders gewoon wit.
                color = FONTCOLOR1
            self.table_view[index].append(self.normalfont.render(row[1], True, color).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, FONTCOLOR1).convert_alpha())
            self._set_color(row[3], self.table_view[index], POSCOLOR1, NEGCOLOR1)
            self._set_color(row[6], self.table_view[index], POSCOLOR2, NEGCOLOR2)

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
            self.surface.blit(row[3], (COLUMN4X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[4], (COLUMN5X, COLUMNSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)

    @staticmethod
    def _get_difference(hero, hovered_equipment_item, skill):
        """
        Berekent het verschil van het equipte item en hoverde item voor in col[6]. Voor de betreffende skill.
        :return: hij moet bij niets "" en niet None teruggeven, vanwege de verwachting in _set_color().
        """
        if hovered_equipment_item:
            eqp_skl = hero.get_equipped_item_of_type(hovered_equipment_item.TYP).get_value_of(skill.RAW)
            new_skl = hovered_equipment_item.get_value_of(skill.RAW)
            return new_skl - eqp_skl
        return ""

    def _create_rect_with_offset(self, index, text):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + COLUMN2X, (self.rect.top + COLUMNSY) + index * ROWHEIGHT
        return rect

    def _set_color(self, value, col, poscolor, negcolor):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param col: in welke kolom de regel zich bevind
        :param poscolor: welke kleuren moet hij weergeven
        """
        if value == "":
            value = 0
        if value == 0:
            value = ""
            col.append(self.normalfont.render(value, True, FONTCOLOR1).convert_alpha())
        elif value > 0:
            value = "(+"+str(value)+")"
            col.append(self.normalfont.render(value, True, poscolor).convert_alpha())
        elif value < 0:
            value = "("+str(value)+")"
            col.append(self.normalfont.render(value, True, negcolor).convert_alpha())
