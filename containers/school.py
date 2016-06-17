
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

    def add(self, spell_object):
        """
        ...
        :param spell_object:
        :return:
        """
        if spell_object.SCL != self.NAM:
            return print("Kan niet.")
        else:
            self[spell_object.RAW] = spell_object

# todo, check of hij al bestaat.
# todo, check op quantity oid
