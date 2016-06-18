
"""
class: StatsBox
"""

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.

import pygame

from screens.party.basebox import BaseBox


LINECOLOR = pygame.Color("white")

TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 160
COLUMN3X = 200
COLUMN4X = 240
COLUMNSY = 60
ROWHEIGHT = 22

TITLE = "Stats"

WHT_DESC = 'wht'
MVP_DESC = 'mvp'
PRT_DESC = 'prt'
HIT_DESC = 'hit'


class StatsBox(BaseBox):
    """
    Alle weergegeven informatie van alle stats van een hero.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()

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
        self.table_data = [
            # row[0],               row[1],                    row[2],           row[3],        row[4],         row[5]
            ["XP Remaining :", str(hero.exp.rem),       "",                        None,    "",                   ""],
            ["Total XP :",     str(hero_exp_tot),       "",                        None,    "",                   ""],
            ["Next Level :",   str(hero_lev_next),      "",                        None,    "",                   ""],
            ["",               "",                      "",                        None,    "",                   ""],
            ["Weight :",       str(hero.tot_wht),       "",                        None,    self._desc(WHT_DESC), wht],
            ["Movepoints :",   str(hero.sta_mvp),       hero.dif_mvp,              None,    self._desc(MVP_DESC), mvp],
            ["Protection :",   str(hero.prt),           hero.sld_prt,              None,    self._desc(PRT_DESC), prt],
            ["Defense :",      str(hero.sld_des),       "",                        None,    "",                   des],
            ["Base Hit :",     str(hero.wpn_hit)+" %",  hero.war.bonus(hero.wpn),  None,    self._desc(HIT_DESC), hit],
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
            row[3] = self._create_rect_with_offset(index, row[0], COLUMN1X, COLUMNSY, ROWHEIGHT)

        # maak dan een nieuwe tabel aan met de tekst, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(self.normalfont.render(row[0], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[1], True, self.fontcolor1).convert_alpha())
            self._set_color(row[2], self.table_view[index], 1)
            self._set_color(row[5], self.table_view[index], 2, row[0])  # dit is om weight te bepalen

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
    def _desc(stat):
        if stat == WHT_DESC:
            # Weight
            return (
                "Defines how heavy your character is equipped with equipment. "
                "Weight has negative impact on movepoints and agility.")

        elif stat == MVP_DESC:
            # Movepoints
            return (
                "Defines how many steps your character is able to take in one turn. The more stamina your character "
                "has, the more movepoints. The more weight your character has, the less movepoints. The first column "
                "shows the number of movepoints calculated from your stamina. The second (red) column shows the "
                "calculated weight subtracted.")

        elif stat == PRT_DESC:
            # Protection
            return (
                "Protection decreases the amount of health your character loses when hit in combat. There is no "
                "Shield Protection when attacked from behind. The first column shows all the protection points from "
                "your equipment combined, minus the shield. The second (green) column shows the protection points "
                "from your shield.")

        elif stat == HIT_DESC:
            # Base Hit
            return (
                "Defines how much chance the weapon of your character has in striking the enemy successfully. "
                "The higher the percentage, the higher the chance to hit. The first column shows the percentage "
                "of the weapon. The second (green) column shows the amount your Warrior Skill adds to your Base Hit.")
