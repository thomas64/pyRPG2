
"""
class: GearData
class: GearDataClass
class: GearType
class: GearItem
"""

import collections
import enum

# todo, uit colornote app:
# - geen empty items meer
# - min int gebruiken voor items?
# - mvp aan items


class GearData(enum.Enum):
    """
    Alle Enum gears data erven van deze class en krijgen deze methode mee.
    """
    def __getitem__(self, item):        # als er iets wordt gevraagd wat niet kan aan een enum, zoals [0] of [1]
        if item == 0:                   # voor een OrderedDict (zoals ShieldsData) dan wordt deze uitgevoerd.
            return self.name            # hij returned dan een waarde die een enum wel kan, namelijk .name en .value
        elif item == 1:
            return self.value


class GearDataClass(object):
    """
    Alle data classes die geen Enum zijn kunnen erven van deze class. Weapons, Shields en Armors.
    """
    def __init__(self):
        self.inside = collections.OrderedDict()

    def __iter__(self):                 # om gesorteerd op winkelvolgorde te laten zien
        return iter(sorted(self.inside.items(), key=lambda xx: xx[1]['sort']))      # [1] dan zijn het de .values()

    def __getattr__(self, key):         # om een nieuwe aan te kunnen maken met factory
        return self.inside[key]


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
    ring = 8
    belt = 9
    boots = 10
    accessory = 11


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
