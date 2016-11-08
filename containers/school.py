
"""
class: School
"""

from constants import SchoolType


class School(dict):
    """
    ...
    """
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.NAM = name

    def get_all_spells(self):
        """
        Geeft een gesorteerde lijst terug.
        """
        return sorted(self.values(), key=lambda xx: xx.SRT)

    def get_qty_of_spell(self, spell_raw):
        """
        ...
        :param spell_raw:
        :return:
        """
        if spell_raw in self:
            return self[spell_raw].qty
        else:
            return 0

    def is_able_to_learn(self, spell_object, wiz_qty, xp_amount, gold_amount):
        """
        ...
        :param spell_object:
        :param wiz_qty: hoe hoog de wizard skill is van een hero.
        :param xp_amount: hoeveel xp de hero heeft
        :param gold_amount: hoeveel gold de party heeft
        :return:
        """
        if self.NAM == SchoolType.non:
            return False, ["Only wizards can learn spells."]

        elif wiz_qty < 1:
            return False, ["You need the Wizard Skill to learn spells."]

        elif spell_object.SCL != self.NAM and spell_object.SCL != SchoolType.ntl and self.NAM != SchoolType.spl:
            return False, ["You cannot learn {} as".format(spell_object.NAM),
                           "you are of the wrong school."]
        elif wiz_qty < spell_object.MIN:
            return False, ["Your Wizard rank is not high",
                           "enough to learn {}.".format(spell_object.NAM)]
        elif type(spell_object.nxt_lev) == str:  # maw, als hij "Max" is.
            return False, ["You cannot learn the spell",
                           "{} any further.".format(spell_object.NAM)]
        elif spell_object.xp_cost > xp_amount:
            return False, ["You need {} more XP to".format(spell_object.xp_cost - xp_amount),
                           "learn {}.".format(spell_object.NAM)]
        elif spell_object.gold_cost > gold_amount:
            return False, ["You need {} more gold to".format(spell_object.gold_cost - gold_amount),
                           "learn {}.".format(spell_object.NAM)]
        else:
            return True, None

    def add_s(self, spell_object):
        """
        Het spell_object en gelijknamige spell in de school zijn 2 verschillende objecten.
        """
        # deze is alleen voor in een school. bij de start van het spel staat .qty veel hoger.
        if spell_object.qty == 0:
            # anders staat hij nog gelijk aan die van de hero. is nu +1
            spell_object.upgrade()

        if spell_object.RAW in self:
            # deze maakt helemaal geen gebruik van het spell_object. dus 0 of 1, maakt niet uit.
            self[spell_object.RAW].upgrade()
        else:
            # het spell_object.qty is op 1 gezet als het op 0 stond.
            self[spell_object.RAW] = spell_object
