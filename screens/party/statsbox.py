
"""
class: StatsBox
"""

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.

import pygame

from constants import StatType as StTy
from .basebox import BaseBox


LINECOLOR = pygame.Color("white")

TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 160
COLUMN3X = 200
COLUMN4X = 240
COLUMNSY = 60
ROWHEIGHT = 22

TITLE = "Stats"


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
        wht = self._get_difference(hero, hovered_equipment_item, StTy.wht.name)
        mvp = self._get_difference(hero, hovered_equipment_item, StTy.mvp.name)
        prt = self._get_difference(hero, hovered_equipment_item, StTy.prt.name)
        des = self._get_difference(hero, hovered_equipment_item, StTy.des.name)
        hit = self._get_difference(hero, hovered_equipment_item, StTy.hit.name)
        dam = self._get_difference(hero, hovered_equipment_item, StTy.dam.name)

        # zet dan alles in deze tabel met zes kolommen. de vierde kolom is leeg voor de rects van de eerste kolom
        self.table_data = [
            # row[0],             row[1],                 row[2],      row[3],       row[4],                     row[5]
            ["",                  "",                     "",           None, "",                                  ""],
            ["XP Remaining :",    str(hero.exp.rem),      "",           None, "",                                  ""],
            ["Total XP :",        hero_exp_tot,           "",           None, "",                                  ""],
            ["Next Level :",      hero_lev_next,          "",           None, "",                                  ""],
            ["",                  "",                     "",           None, "",                                  ""],
            [StTy.wht.value+" :", str(hero.eqp_wht),      "",           None, self._desc(StTy.wht),               wht],
            [StTy.mvp.value+" :", str(hero.sta_mvp),      hero.dif_mvp, None, self._desc(StTy.mvp),               mvp],
            [StTy.prt.value+" :", str(hero.tot_prt),      "",           None, self._desc(StTy.prt, hero.sld_prt), prt],
            [StTy.des.value+" :", str(hero.sld_des),      "",           None, "",                                 des],
            [StTy.hit.value+" :", str(hero.sub_hit)+" %", hero.eqp_hit, None, self._desc(StTy.hit, hero.war_hit), hit],
            [StTy.dam.value+" :", str(hero.wpn_dam),      "",           None, "",                                 dam]
        ]
        # voeg ook de 7 stats aan de table_data toe
        for i, stat in enumerate(hero.stats_tuple):
            preview_value = self._get_difference(hero, hovered_equipment_item, stat.RAW)
            #                           row[0],          row[1],       row[2], row[3], row[4],       row[5]
            self.table_data.insert(i, [stat.NAM+" :", str(stat.qty), stat.ext, None, stat.DESC, preview_value])

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
    def _desc(stat, ext_stat=None):
        if stat == StTy.wht:
            # Weight
            return (
                "Defines how heavy your character is equipped with equipment. "
                "Weight has negative impact on movepoints and agility.")

        elif stat == StTy.mvp:
            # Movepoints
            return (
                "Defines how many steps your character is able to take in one turn. The more stamina your character "
                "has, the more movepoints. The more weight your character has, the less movepoints. The first column "
                "shows the number of movepoints calculated from your character's stamina. The second (red) column "
                "shows the calculated weight subtracted. If that column is green, it means that your character has "
                "special movepoints enhancers in his/her equipment.")

        elif stat == StTy.prt:
            # Protection
            return (
                "Protection decreases the amount of health your character loses when hit in combat. There is no "
                "Shield Protection when attacked from behind. The number shows all the protection points from "
                "your character's equipment combined.",
                " ",
                "{}pt from Shield Protection.".format(ext_stat))
        elif stat == StTy.hit:
            # Chance to Hit
            return (
                "Defines how much chance the weapon of your character has in striking the enemy successfully. "
                "The higher the percentage, the higher the chance to hit. The first column shows the hit chance from "
                "your character's weapon plus a possible calculated warrior skill. The second (green) column shows "
                "the special hit chance enhancers in your character's equipment.",
                " ",
                "{}% from Warrior Skill.".format(ext_stat))
