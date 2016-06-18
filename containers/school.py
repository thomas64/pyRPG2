
"""
class: School
"""

from database import SchoolType


class School(dict):
    """
    ...
    """
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.NAM = name

    def add(self, spell_object, wiz_qty, quantity=1, force=False):
        """
        ...
        :param spell_object:
        :param wiz_qty:
        :param quantity: is alleen maar voor het upgraden, de quantity zit in de spell_object zelf.
        :param force: forceer bij opstarten van game sommige spells op characters wat eigenlijk niet kan.
         bijvoorbeeld elias, teleportation, level 7 -> 8.
        :return:
        """
        if self.NAM == SchoolType.non:
            return print("Je bent geen wizard, kan niet.")

        elif wiz_qty < 1:
            return print("Je hebt geen wizard skill, kan niet.")

        elif wiz_qty < spell_object.MIN and force is False:
            return print("Je wizard level is te laag, kan niet.")

        elif spell_object.RAW in self:
            return spell_object.upgrade(quantity)

        elif spell_object.SCL == SchoolType.ntl:
            self[spell_object.RAW] = spell_object
            return print("Spell geleerd, gelukt.")

        elif self.NAM == SchoolType.spl:
            self[spell_object.RAW] = spell_object
            return print("Spell geleerd, gelukt.")

        elif spell_object.SCL != self.NAM:
            return print("Verkeerde school, kan niet.")

        else:
            self[spell_object.RAW] = spell_object
            return print("Spell geleerd, gelukt.")
