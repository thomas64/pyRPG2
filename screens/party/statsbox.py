
"""
class: StatsBox
"""

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.

from constants import StatType
from .basebox import BaseBox


COLUMN1X = 50   # naam
COLUMN2X = 160  # base stat
COLUMN3X = 200  # ext value
COLUMN4X = 240  # tot stat
COLUMN5X = 280  # preview value
COLUMNSY = 50
ROWHEIGHT = 22

TITLE = "Stats"
TOTALCOLUMNS = (('text', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X))


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

    def update(self, hero, hovered_equipment_item):
        """
        Update eerst alle data.
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

        xpr_name = "XP Remaining :"
        txp_name = "Total XP :"
        nxt_name = "Next Level :"
        wht_name = StatType.wht.value + " :"
        mvp_name = StatType.mvp.value + " :"
        prt_name = StatType.prt.value + " :"
        des_name = StatType.des.value + " :"
        hit_name = StatType.hit.value + " :"
        dam_name = StatType.dam.value + " :"

        xpr_bval = str(hero.exp.rem)
        txp_bval = hero_exp_tot
        nxt_bval = hero_lev_next
        wht_bval = str(hero.eqp_wht)
        mvp_bval = str(hero.sta_mvp)
        prt_bval = str(hero.tot_prt)
        des_bval = str(hero.sld_des)
        hit_bval = str(hero.sub_hit)+" %"
        dam_bval = str(hero.wpn_dam)

        xpr_diff = ""
        txp_diff = ""
        nxt_diff = ""
        wht_diff = ""
        mvp_diff = hero.dif_mvp
        prt_diff = ""
        des_diff = ""
        hit_diff = hero.eqp_hit
        dam_diff = ""

        xpr_tval = ""
        txp_tval = ""
        nxt_tval = ""
        wht_tval = ""
        mvp_tval = "("+str(hero.tot_mvp)+")"
        prt_tval = ""
        des_tval = ""
        hit_tval = "("+str(hero.tot_hit)+" %)"
        dam_tval = ""

        xpr_prev = ""
        txp_prev = ""
        nxt_prev = ""
        wht_prev = self._get_difference(hero, hovered_equipment_item, StatType.wht.name)
        mvp_prev = self._get_difference(hero, hovered_equipment_item, StatType.mvp.name)
        prt_prev = self._get_difference(hero, hovered_equipment_item, StatType.prt.name)
        des_prev = self._get_difference(hero, hovered_equipment_item, StatType.des.name)
        hit_prev = self._get_difference(hero, hovered_equipment_item, StatType.hit.name)
        dam_prev = self._get_difference(hero, hovered_equipment_item, StatType.dam.name)

        xpr_desc = ""
        txp_desc = ""
        nxt_desc = ""
        wht_desc = self._desc(StatType.wht)
        mvp_desc = self._desc(StatType.mvp)
        prt_desc = self._desc(StatType.prt, hero.sld_prt)
        des_desc = ""
        hit_desc = self._desc(StatType.hit, hero.war_hit)
        dam_desc = ""

        no1_dict = dict(name="",       bval="",       diff="",       tval="",       prev="",       desc="")
        xpr_dict = dict(name=xpr_name, bval=xpr_bval, diff=xpr_diff, tval=xpr_tval, prev=xpr_prev, desc=xpr_desc)
        txp_dict = dict(name=txp_name, bval=txp_bval, diff=txp_diff, tval=txp_tval, prev=txp_prev, desc=txp_desc)
        nxt_dict = dict(name=nxt_name, bval=nxt_bval, diff=nxt_diff, tval=nxt_tval, prev=nxt_prev, desc=nxt_desc)
        no2_dict = dict(name="",       bval="",       diff="",       tval="",       prev="",       desc="")
        wht_dict = dict(name=wht_name, bval=wht_bval, diff=wht_diff, tval=wht_tval, prev=wht_prev, desc=wht_desc)
        mvp_dict = dict(name=mvp_name, bval=mvp_bval, diff=mvp_diff, tval=mvp_tval, prev=mvp_prev, desc=mvp_desc)
        prt_dict = dict(name=prt_name, bval=prt_bval, diff=prt_diff, tval=prt_tval, prev=prt_prev, desc=prt_desc)
        des_dict = dict(name=des_name, bval=des_bval, diff=des_diff, tval=des_tval, prev=des_prev, desc=des_desc)
        hit_dict = dict(name=hit_name, bval=hit_bval, diff=hit_diff, tval=hit_tval, prev=hit_prev, desc=hit_desc)
        dam_dict = dict(name=dam_name, bval=dam_bval, diff=dam_diff, tval=dam_tval, prev=dam_prev, desc=dam_desc)

        data_list = [no1_dict, xpr_dict, txp_dict, nxt_dict, no2_dict,
                     wht_dict, mvp_dict, prt_dict, des_dict, hit_dict, dam_dict]

        self.view_matrix = []
        self.data_matrix = []

        index = 0   # de index telt door in twee for loops.
        for stat in hero.stats_tuple:
            preview_value = self._get_difference(hero, hovered_equipment_item, stat.RAW)

            self.view_matrix.append(
                [self.normalfont.render(stat.NAM + " :", True, self._get_color(index)).convert_alpha(),
                 self.normalfont.render(str(stat.qty), True, self.fontcolor1).convert_alpha(),
                 self._set_color(stat.ext, 1),
                 self.normalfont.render("("+str(stat.tot)+")", True, self.fontcolor1).convert_alpha(),
                 self._set_color(preview_value, 2)
                 ]
            )
            self.data_matrix.append([stat, None, stat.DESC])
            index += 1

        for itm_list in data_list:
            self.view_matrix.append(
                [self.normalfont.render(itm_list["name"], True, self._get_color(index)).convert_alpha(),
                 self.normalfont.render(itm_list["bval"], True, self.fontcolor1).convert_alpha(),
                 self._set_color(itm_list["diff"], 1),
                 self.normalfont.render(itm_list["tval"], True, self.fontcolor1).convert_alpha(),
                 self._set_color(itm_list["prev"], 2, itm_list["name"])  # dit is om weight te bepalen
                 ]
            )
            self.data_matrix.append([None, None, itm_list["desc"]])
            index += 1

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul row[3] kolom. hierin staan de rects van row[1]. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()

    @staticmethod
    def _desc(stat, ext_stat=None):
        if stat == StatType.wht:
            # Weight
            return (
                "Defines how heavy your character is equipped with equipment. "
                "Weight has negative impact on movepoints and agility.")

        elif stat == StatType.mvp:
            # Movepoints
            return (
                "Defines how many steps your character is able to take in one turn. The more stamina your character "
                "has, the more movepoints. The more weight your character has, the less movepoints. The first column "
                "shows the number of movepoints calculated from your character's stamina. The second (red) column "
                "shows the calculated weight subtracted. If that column is green, it means that your character has "
                "special movepoints enhancers in his/her equipment. The column in parenthesis shows the total value.")

        elif stat == StatType.prt:
            # Protection
            return (
                "Protection decreases the amount of health your character loses when hit in combat. There is no "
                "Shield Protection when attacked from behind. The number shows all the protection points from "
                "your character's equipment combined.",
                " ",
                "{}pt from Shield Protection.".format(ext_stat))
        elif stat == StatType.hit:
            # Chance to Hit
            return (
                "Defines how much chance the weapon of your character has in striking the enemy successfully. "
                "The higher the percentage, the higher the chance to hit. The first column shows the hit chance from "
                "your character's weapon plus a possible calculated warrior skill. The second (green) column shows "
                "the special hit chance enhancers in your character's equipment. The column in parenthesis shows "
                "the total value.",
                " ",
                "{}% from Warrior Skill.".format(ext_stat))
