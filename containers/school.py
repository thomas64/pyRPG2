
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

    def add_s(self, spell_object, wiz_qty, quantity=1, force=False):
        """
        ...
        :param spell_object:
        :param wiz_qty: hoe hoog de wizard skill is van een hero.
        :param quantity: is alleen maar voor het upgraden, de quantity zit in de spell_object zelf.
        :param force: forceer bij opstarten van game sommige spells op characters wat eigenlijk niet kan.
         bijvoorbeeld elias, teleportation, level 7 -> 8.
        :return:
        """
        if self.NAM == SchoolType.non:
            return False, ["Only wizards can learn spells."]

        elif wiz_qty < 1:
            return False, ["You need the Wizard Skill to learn spells."]

        elif wiz_qty < spell_object.MIN and force is False:
            return False, ["Your Wizard rank is not high",
                           "enough to learn {}.".format(spell_object.NAM)]

        elif spell_object.RAW in self:
            return self[spell_object.RAW].upgrade(quantity)

        elif spell_object.SCL == SchoolType.ntl:
            self[spell_object.RAW] = spell_object
            return True, None

        elif self.NAM == SchoolType.spl:
            self[spell_object.RAW] = spell_object
            return True, None

        elif spell_object.SCL != self.NAM:
            return False, ["You cannot learn {} as".format(spell_object.NAM),
                           "you are of the wrong school."]

        else:
            self[spell_object.RAW] = spell_object
            return True, None
