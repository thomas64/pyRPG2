
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
    Value[1] en [2] zijn strings, omdat ik ze niet direct kan importeren, ze worden later omgezet bijv in de
    inventory container naar packages modules en class names.
    value[0] wordt gebruikt in hero.get_item_equipped_of_type()
    value[1] en [2] worden gebruikt in inv_container.get_sorted_of_type()
    """
    weapon = 'wpn',    'items.weapon',    'WeaponsData'
    shield = 'sld',    'items.shield',    'ShieldsData'
    helmet = 'hlm',    'items.helmet',    'HelmetsData'
    amulet = 'amu',    'items.amulet',    'AmuletsData'
    armor = 'arm',     'items.armor',     'ArmorsData'
    cloak = 'clk',     'items.cloak',     'CloaksData'
    gloves = 'glv',    'items.gloves',    'GlovesData'
    ring = 'rng',      'items.ring',      'RingsData'
    belt = 'blt',      'items.belt',      'BeltsData'
    boots = 'bts',     'items.boots',     'BootsData'
    accessory = 'acy', 'items.accessory', 'AccessoriesData'


class GearItem(object):
    """
    Een GearItem object met attributen als de waarden van de extra's die het item heeft zoals THF.
    """
    def __init__(self, geartype, sprite, **kwargs):
        self.TYP = geartype                        # enum
        self.SPR = sprite
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

    def get_value_of(self, attr):
        """
        Vraagt een attribute op van een GearItem. De RAW van bijv een skill is in lower zoals 'alc', maar de 'alc' van
        een GearItem is self.ALC, vandaar de upper().
        :param attr: sting, het opgevraagde attribute
        :return: de waarde van het attribute, en zo niet bestaand, nul.
        """
        return getattr(self, attr.upper(), 0)

    def is_not_empty(self):
        """
        Bekijkt of de GearItem een 'empty' is, door te checken op attribute NAM.
        :return: True wanneer de NAM bestaat, want hij is niet empty. Anders False, want hij ís empty.
        """
        if hasattr(self, 'NAM'):
            return True
        return False
