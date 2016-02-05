
"""
class: GearType
class: GearItem
"""

import enum


class GearType(enum.Enum):
    """
    Alle gear typen op een rij.
    """
    weapon = 1
    shield = 2
    helmet = 3
    necklace = 4
    armor = 5
    cloak = 6
    gloves = 7
    lring = 8
    rring = 9
    belt = 10
    boots = 11
    accessory = 12


class GearItem(object):
    """
    Een GearItem object met attributen als de waarden van de extra's die het item heeft zoals THF.
    """
    def __init__(self, geartype, **kwargs):
        self.TYPE = geartype                        # enum
        self.quantity = 1

        for key, value in kwargs.items():
            setattr(self, key.upper(), value)       # zet de dict van kwargs om in attributen

    # noinspection PyUnusedLocal
    def __getattr__(self, item):                    # als de attribute niet bestaat, geef dan 0 terug.
        return 0
