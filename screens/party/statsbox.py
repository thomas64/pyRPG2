
"""
class: StatsBox
"""

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.

from constants import StatType as StTy
from .basebox import BaseBox


COLUMN1X = 50
COLUMN2X = 160
COLUMN3X = 200
COLUMN4X = 240
COLUMNSY = 50
ROWHEIGHT = 22

TITLE = "Stats"
TOTALCOLUMNS = (('text', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X))


class StatsBox(BaseBox):
    """
    Alle weergegeven informatie van alle stats van een hero.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()
        self.rowheight = ROWHEIGHT
        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X
        self.columnsy = COLUMNSY

    def mouse_click(self, event):
        """
        Als je klikt op een item in de uit row[3] geregistreerde rects.
        :param event: pygame.MOUSEBUTTONDOWN uit partyscreen
        :return: row[6] is de kolom met het object. alleen de 7 base stats bevatten een row[6]
        """
        for index, row in enumerate(self.table_data):
            if index in range(7):  # loopt hiermee dus van 0 tot 6
                if row[3].collidepoint(event.pos):
                    return True, row[6]
        return False, None

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
            #                           row[0],          row[1],       row[2], row[3], row[4],       row[5],   row[6]
            self.table_data.insert(i, [stat.NAM+" :", str(stat.qty), stat.ext, None, stat.DESC, preview_value, stat])

        # maak dan een nieuwe tabel aan met de tekst, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(self.normalfont.render(row[0], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[1], True, self.fontcolor1).convert_alpha())
            self._set_color(row[2], self.table_view[index], 1)
            self._set_color(row[5], self.table_view[index], 2, row[0])  # dit is om weight te bepalen

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul row[3] kolom. hierin staan de rects van row[1]. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()

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
