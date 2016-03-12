
"""
class: StatsBox
"""

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 329
BOXHEIGHT = 490
TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 160
COLUMN3X = 200
COLUMN4X = 240
COLUMNSY = 60
ROWHEIGHT = 22

TITLE = "Stats"

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

POSCOLOR1 = pygame.Color("green")
POSCOLOR2 = pygame.Color("lightgreen")
NEGCOLOR1 = pygame.Color("red")
NEGCOLOR2 = pygame.Color("orangered")

WHT_DESC = 'wht'
MVP_DESC = 'mvp'
PRT_DESC = 'prt'


class StatsBox(object):
    """
    Alle weergegeven informatie van alle stats van een hero.
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

    def update(self, hero, hovered_equipment_item):
        """
        Update eerst alle data.
        Let op: self.table_view bevat maar 3 kolommen in tegenstelling tot self.table_data met 5
        :param hero: de huidige geselecteerde hero uit partyscreen
        :param hovered_equipment_item: het item waar de muis overheen hovered in invclickbox
        """
        # zet eerst even wat bepaalde waarden vast.
        if hero.lev.qty >= hero.lev.MAX:
            hero_exp_tot = "Max"
            hero_lev_next = "Max"
        else:
            hero_exp_tot = str(hero.exp.tot)
            hero_lev_next = str(hero.lev.next(hero.exp.tot))

        # de preview waarden, voor is row[5]
        wht = self._get_difference(hero, hovered_equipment_item, 'WHT')
        mvp = self._get_difference(hero, hovered_equipment_item, 'MVP')
        prt = self._get_difference(hero, hovered_equipment_item, 'PRT')
        des = self._get_difference(hero, hovered_equipment_item, 'DES')
        hit = self._get_difference(hero, hovered_equipment_item, 'HIT')
        dam = self._get_difference(hero, hovered_equipment_item, 'DAM')

        # zet dan alles in deze tabel met zes kolommen. de vierde kolom is leeg voor de rects van de eerste kolom
        # todo, testen hoe dit: hero.war.bonus(hero.wpn), gaat met hero zonder wapen. bonus() checken.
        self.table_data = [
            # row[0],               row[1],                    row[2],           row[3],        row[4],         row[5]
            ["XP Remaining :", str(hero.exp.rem),       "",                        None,    "",                   ""],
            ["Total XP :",     str(hero_exp_tot),       "",                        None,    "",                   ""],
            ["Next Level :",   str(hero_lev_next),      "",                        None,    "",                   ""],
            ["",               "",                      "",                        None,    "",                   ""],
            ["Weight :",       str(hero.tot_wht),       "",                        None,    self._desc(WHT_DESC), wht],
            ["Movepoints :",   str(hero.sta_mvp),       hero.dif_mvp,              None,    self._desc(MVP_DESC), mvp],
            ["Protection :",   str(hero.prt),           hero.sld_prt,              None,    self._desc(PRT_DESC), prt],
            ["Defense :",      str(hero.tot_des),       "",                        None,    "",                   des],
            ["Base Hit :",     str(hero.tot_hit)+" %",  hero.war.bonus(hero.wpn),  None,    "",                   hit],
            ["Damage :",       str(hero.tot_dam),       "",                        None,    "",                   dam],
            ["",               "",                      "",                        None,    "",                   ""]
        ]
        # voeg ook de 7 stats aan de table_data toe
        for stat in hero.stats_tuple:
            preview_value = self._get_difference(hero, hovered_equipment_item, stat.RAW)
            self.table_data.append(
                # row[0],           row[1],       row[2], row[3], row[4],       row[5]
                [stat.NAM + " :", str(stat.qty), stat.ext, None, stat.DESC, preview_value]
            )

        # vul de vierde lege kolom. hierin staan de rects van de eerste kolom. rect is voor muisklik.
        for index, row in enumerate(self.table_data):
            row[3] = self._create_rect_with_offset(index, row[0])

        # maak dan een nieuwe tabel aan met de tekst, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            if index == self.cur_item:              # als de index van deze rij gelijk is aan waar de muis over zit,
                color = FONTCOLOR2                  # maak hem geel
            else:                                   # anders gewoon wit.
                color = FONTCOLOR1
            self.table_view[index].append(self.normalfont.render(row[0], True, color).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[1], True, FONTCOLOR1).convert_alpha())
            self._set_color(row[2], self.table_view[index], POSCOLOR1, NEGCOLOR1, None)
            self._set_color(row[5], self.table_view[index], POSCOLOR2, NEGCOLOR2, row[0])  # dit is om weight te bepalen

    def render(self, screen):
        """
        En teken dan al die data op de surface en die op de screen.
        Let op: self.table_view bevat maar 3 kolommen in tegenstelling tot self.table_data met 5
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[0], (COLUMN1X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[1], (COLUMN2X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[2], (COLUMN3X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[3], (COLUMN4X, COLUMNSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)

    @staticmethod
    def _get_difference(hero, hovered_equipment_item, stat):
        """
        Berekent het verschil van het equipte item en hoverde item voor in col[6]. Voor de betreffende skill.
        :return: hij moet bij niets "" en niet None teruggeven, vanwege de verwachting in _set_color().
        """
        if hovered_equipment_item:
            eqp_stat = hero.get_equipped_item_of_type(hovered_equipment_item.TYP).get_value_of(stat)
            new_stat = hovered_equipment_item.get_value_of(stat)
            return new_stat - eqp_stat
        return ""

    def _create_rect_with_offset(self, index, text):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + COLUMN1X, (self.rect.top + COLUMNSY) + index * ROWHEIGHT
        return rect

    def _set_color(self, value, col, poscolor, negcolor, weight_check):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param col: in welke kolom de regel zich bevind
        :param poscolor: welke kleuren moet hij weergeven
        """
        # hele lelijke weight check, maar omdat weight de enige is, doe ik dit zo.
        # weight is de enige waarvan een grotere waarde niet positief is, vandaar de omdraaiing.
        if weight_check is "Weight :":
            poscolor, negcolor = negcolor, poscolor

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

    @staticmethod
    def _desc(stat):
        if stat == WHT_DESC:
            # Weight
            return (
                "Defines how heavy your character is equipped with equipment. "
                "Weight has negative impact on movepoints and agility.")

        if stat == MVP_DESC:
            # Movepoints
            return (
                "Defines how many steps your character is able to take in one turn. The more stamina your character "
                "has, the more movepoints. The more weight your character has, the less movepoints. The first column "
                "shows the number of movepoints calculated from your stamina. The second (red) column shows the "
                "calculated weight subtracted.")

        if stat == PRT_DESC:
            # Protection
            return (
                "Protection decreases the amount of health your character loses when hit in combat. There is no "
                "Shield Protection when attacked from behind. The first column shows all the protection points from "
                "your equipment combined, minus the shield. The second (green) column show the protection points from "
                "your shield.")
