
"""
class: GearData
class: GearDataClass
class: GearType
class: GearItem
"""

import collections
import enum

# todo, uit colornote app:
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

    def __iter__(self):                 # om er in een winkel doorheen te kunnen gaan loopen
        return iter(self.inside.items())

    def __getattr__(self, key):         # om een nieuwe aan te kunnen maken met factory. anders herkent hij de woodenb.
        return self.inside[key]         # niet als een attribute: piet = ShieldsData.factory(ShieldsData.woodenbuckler)

    def set_shop(self):
        """
        Shop uitzetten voor sommige gear items.
        """
        for gear_key, gear_value in self.inside.items():
            if "+" in gear_key or "titanium" in gear_key:
                gear_value['shp'] = False
        # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

    def rearrage(self):
        """
        Herschik de volgorde van de gecreerde dataset.
        """
        temp_dict = collections.OrderedDict()
        for gear_key, gear_value in sorted(self.inside.items(), key=lambda xx: xx[1]['srt']):
            temp_dict[gear_key] = gear_value
        self.inside = temp_dict


class GearType(enum.Enum):
    """
    Alle gear typen op een rij.
    """
    weapon = 1
    shield = 2
    helmet = 3
    amulet = 4
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
        self.TYP = geartype                        # enum
        self.qty = 1

        for gear_value_key, gear_value_value in kwargs.items():
            setattr(self, gear_value_key.upper(), gear_value_value)     # zet de dict van kwargs om in attributen

        try:
            # noinspection PyUnresolvedReferences
            self.RAW = self.NAM.strip().lower().replace(" ", "")        # als er een NAM is, geef hem een RAW
        except AttributeError:
            pass
        try:
            # noinspection PyUnresolvedReferences
            del self.SRT        # deze zijn niet nodig als gear. alleen voor in de shop, en dan zijn het geen gear nog.
        except AttributeError:
            pass
        try:
            # noinspection PyUnresolvedReferences
            del self.SHP
        except AttributeError:
            pass
