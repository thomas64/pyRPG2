
"""
class: Spell
"""

from database import School


class Spell(object):
    """
    ...
    """
    TRAININGSCOSTS = (200, 80, 120, 160, 200, 240, 280, 320, 360, 400, "Max")
    MAXIMUM = 10

    # todo, icon en descriptions en docstrings

    def __init__(self, name, raw, school, minimum_rank, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.ICON = ''
        self.SCL = school
        self.MIN = minimum_rank
        self.UPG = upgrade
        self.qty = quantity


class AirShield(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Air Shield", 'air_sld', School.elm, 1, 320, quantity)
        self.DESC = "test"
