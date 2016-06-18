
"""
class: BaseBox
"""

import pygame


BACKGROUNDCOLOR = pygame.Color("black")

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

POSCOLOR1 = pygame.Color("green")
POSCOLOR2 = pygame.Color("lightgreen")
NEGCOLOR1 = pygame.Color("red")
NEGCOLOR2 = pygame.Color("orangered")


class BaseBox(object):
    """
    De base class voor de boxen, de andere boxen kunnen hiervan erven.
    """
    def __init__(self, position, width, height):
        self.surface = pygame.Surface((width, height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.fontcolor1 = FONTCOLOR1
        self.fontcolor2 = FONTCOLOR2

        self.cur_item = None

        self.table_data = []
        self.table_view = []

    def mouse_hover(self, event):
        """
        Als de muis over een item in de uit row[3] geregistreerde rects gaat.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: row[4] is de kolom met de info.
        """
        self.cur_item = None
        for index, row in enumerate(self.table_data):
            if row[3].collidepoint(event.pos):
                self.cur_item = index
                return row[4]

    @staticmethod
    def _get_difference(hero, hovered_equipment_item, skill_raw):
        """
        Berekent het verschil van het equipte item en hoverde item voor in col[6]. Voor de betreffende skill.
        :return: hij moet bij niets "" en niet None teruggeven, vanwege de verwachting in _set_color().
        """
        # hovered_equipment_item is None als er niets gehoverd is in party Display
        if hovered_equipment_item:
            eqp_skl = hero.get_equipped_item_of_type(hovered_equipment_item.TYP).get_value_of(skill_raw)
            new_skl = hovered_equipment_item.get_value_of(skill_raw)
            return new_skl - eqp_skl
        return ""

    def _create_rect_with_offset(self, index, text, columnxx, columnsy, rowheight):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + columnxx, (self.rect.top + columnsy) + index * rowheight
        return rect

    def _get_color(self, index):
        """
        Als de index van deze rij gelijk is aan waar de muis over zit, maak hem geel anders gewoon wit.
        :param index: enumerate van for loop
        """
        if index == self.cur_item:
            return self.fontcolor2
        else:
            return self.fontcolor1

    def _set_color(self, value, col, color, weight_check=None):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param col: in welke kolom de regel zich bevind
        :param color: integer, welke kleuren moet hij weergeven? color: 1 of color: 2?
        """

        if color == 1:
            poscolor = POSCOLOR1
            negcolor = NEGCOLOR1
        else:
            poscolor = POSCOLOR2
            negcolor = NEGCOLOR2

        # hele lelijke weight check, maar omdat weight de enige is, doe ik dit zo.
        # weight is de enige waarvan een grotere waarde niet positief is, vandaar de omdraaiing.
        if weight_check == "Weight :":
            poscolor, negcolor = negcolor, poscolor

        if value == "":
            value = 0

        if value == 0:
            value = ""
            col.append(self.normalfont.render(value, True, self.fontcolor1).convert_alpha())
        elif value > 0:
            value = "(+" + str(value) + ")"
            col.append(self.normalfont.render(value, True, poscolor).convert_alpha())
        elif value < 0:
            value = "(" + str(value) + ")"
            col.append(self.normalfont.render(value, True, negcolor).convert_alpha())
