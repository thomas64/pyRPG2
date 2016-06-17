
"""
class: School
"""


class School(dict):
    """
    ...
    """
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.NAM = name

    def add(self, spell_object, quantity=1):
        """
        ...
        :param spell_object:
        :param quantity: is alleen maar voor het upgraden, de quantity zit in de spell_object zelf.
        :return:
        """
        if spell_object.SCL != self.NAM:
            return print("Verkeerde school, kan niet.")
        elif spell_object.RAW in self:
            return spell_object.upgrade(quantity)
        else:
            self[spell_object.RAW] = spell_object
            return print("Spell geleerd, gelukt.")
