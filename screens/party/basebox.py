
"""
class: BaseBox
"""

import pygame

from console import Console
from constants import Keys

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

POSCOLOR1 = pygame.Color("green")
POSCOLOR2 = pygame.Color("lightgreen")
NEGCOLOR1 = pygame.Color("red")
NEGCOLOR2 = pygame.Color("orangered")

TITLEX, TITLEY = 7, 1
SCROLLSPEED = 20
BOTTOMSPACER = 20  # tegen bottom ghosting. deze maakt de layerheight net iets langer.
ICONOFFSET = -6

COLFORRECTS = 1  # in alle party boxen zitten de rects in data_list[X][1], behalve statsbox nog(!)
MOUSEHOVERWIDTH = 200

TITLERECT = (1, 1, 327, 35)  # 327 = boxwidth - 2


class BaseBox(object):
    """
    De base class voor de boxen, de andere boxen kunnen hiervan erven.
    """
    def __init__(self, position, width, height):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.fontcolor1 = FONTCOLOR1
        self.fontcolor2 = FONTCOLOR2

        self.cur_item = None

        self.linecolor = LINECOLOR
        self.title_x, self.title_y = TITLEX, TITLEY
        self.iconoffset = ICONOFFSET

        self.title = None
        self.rowheight = None
        self.total_columns = []
        self.column1x = None
        self.columnsy = None

        self.view_matrix = []
        self.data_matrix = []

        self.run_once = True    # eenmalig voor de _setup_scroll_layer te doen voor de child classes.

    def _setup_scroll_layer(self):
        # stel de scroll layer in
        self.layer_height = BOTTOMSPACER + self.columnsy + len(self.view_matrix) * self.rowheight
        if self.layer_height < self.box_height:
            self.layer_height = self.box_height
        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = self.rect.topleft

        self.background = pygame.Surface((self.box_width, self.layer_height))
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

    def _update_rects_in_layer_rect_with_offset(self):
        """
        Voeg de rects toe in row[1] van data_matrix waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.data_matrix):
            row[COLFORRECTS] = pygame.Rect(self.lay_rect.x + self.column1x,
                                           self.lay_rect.y + self.columnsy + index * self.rowheight,
                                           MOUSEHOVERWIDTH, self.rowheight+1)

    def mouse_scroll(self, event):
        """
        Registreert of scrolwiel gebruikt wordt. Verplaatst de layer dan omhoog of omlaag.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        """
        if event.button == Keys.Scrollup.value:
            if self.lay_rect.y - self.rect.y < 0:
                self.lay_rect.y += SCROLLSPEED
        elif event.button == Keys.Scrolldown.value:
            if self.lay_rect.y - self.rect.y > self.rect.height - self.layer_height:
                self.lay_rect.y -= SCROLLSPEED

        self._update_rects_in_layer_rect_with_offset()

    def mouse_hover(self, event):
        """
        Als de muis over een item in de uit row[1] geregistreerde rects gaat.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit partyscreen
        :return: row[2] is de kolom met de description.
        """
        self.cur_item = None
        for index, row in enumerate(self.data_matrix):
            if row[COLFORRECTS].collidepoint(event.pos):
                self.cur_item = index
                return row[2]

    def mouse_click(self, event):
        """
        Als je klikt op een item in de uit row[1] geregistreerde rects.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :return: row[0] is de kolom met het object.
        """
        for row in self.data_matrix:
            if row[1].collidepoint(event.pos):
                if row[0] is not None:  # de extra waarden in statsbox zijn geen objecten en hebben hier None staan.
                    return True, row[0]
        return False, None

    @staticmethod
    def _get_difference(hero, hovered_equipment_item, skill_raw):
        """
        Berekent het verschil van het equipte item en hoverde item voor in preview_value (row[4] bij skillbox).
        Voor de betreffende skill.
        :return: hij moet bij niets "" en niet None teruggeven, vanwege de verwachting in _set_color().
        """
        # hovered_equipment_item is None als er niets gehoverd is in party Display
        if hovered_equipment_item:
            eqp_skl = hero.get_equipped_item_of_type(hovered_equipment_item.TYP).get_value_of(skill_raw)
            new_skl = hovered_equipment_item.get_value_of(skill_raw)

            # bekijk of de oude penalty kleiner is dan het nieuwe verschil.
            old_pen = 999
            for skl in hero.skills_tuple:
                if skl.RAW == skill_raw:
                    old_pen = skl.ext
                    break

            diff = new_skl - eqp_skl
            # als dat zo is, geef die dan weer, maar niet als de oude penalty gewoon 0 is zoals standaard.
            if diff > abs(old_pen) and not old_pen == 0:
                return abs(old_pen)
            else:
                return diff
        return ""

    def _create_rect_with_offset(self, index, text, columnxx, columnsy, rowheight):
        """
        OP DIT MOMENT NIET MEER IN GEBRUIK! toen het scrollen van de boxen er was, is deze vervangen door update_rects()
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

    def _set_color(self, value, color, weight_check=None):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param color: integer, welke kleuren moet hij weergeven? color: 1 of color: 2?
        :return: de juiste tekens met de juiste kleuren
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
            return self.normalfont.render(value, True, self.fontcolor1).convert_alpha()
        elif value > 0:
            value = "(+" + str(value) + ")"
            return self.normalfont.render(value, True, poscolor).convert_alpha()
        elif value < 0:
            value = "(" + str(value) + ")"
            return self.normalfont.render(value, True, negcolor).convert_alpha()

    def render(self, screen):
        """
        Surface tekent layer, de rest gaat op de layer, en screen tekent de surface.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.layer, (0, self.lay_rect.y - self.rect.y))
        self.layer.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, self.linecolor, self.surface.get_rect(), 1)

        # zwarte background achter de titel. is voor scrollen.
        pygame.draw.rect(self.surface, BACKGROUNDCOLOR, pygame.Rect(TITLERECT))
        self.surface.blit(self.title, (self.title_x, self.title_y))

        for index, row in enumerate(self.view_matrix):
            for row_nr, columnx in enumerate(self.total_columns):
                if columnx[0] == 'icon':
                    self.layer.blit(
                        row[row_nr],
                        (columnx[1], self.columnsy + self.iconoffset + index * self.rowheight))
                elif columnx[0] == 'text':
                    self.layer.blit(
                        row[row_nr],
                        (columnx[1], self.columnsy + index * self.rowheight))
                else:
                    Console.error_unknown_column_key()
                    raise KeyError

        screen.blit(self.surface, self.rect.topleft)
