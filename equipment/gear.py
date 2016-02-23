
"""
class: EquipmentDatabase
class: GearType
class: GearItem
"""

import collections
import enum

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items


class EquipmentDatabase(collections.OrderedDict):
    """
    Alle gear data classes kunnen erven van deze class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):                 # om er in een winkel doorheen te kunnen gaan loopen
        return iter(self.items())

    def __getattr__(self, key):         # om een nieuwe aan te kunnen maken met factory. anders herkent hij de woodenb.
        return self[key]                # niet als een attribute: piet = ShieldsData.factory(ShieldsData.woodenbuckler)

    def set_shop(self):
        """
        Shop uitzetten voor sommige gear items.
        """
        for gear_key, gear_value in self.items():
            if "+" in gear_key or "titanium" in gear_key:
                gear_value['shp'] = False
        # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

    def rearrage(self):
        """
        Herschik de volgorde van de gecreerde dataset.
        """
        temp_dict = collections.OrderedDict()
        for gear_key, gear_value in sorted(self.items(), key=lambda xx: xx[1]['srt']):
            temp_dict[gear_key] = gear_value
        self.items() = temp_dict.items()


class GearType(enum.Enum):
    """
    Alle gear typen op een rij.
    """
    wpn = "Weapon"
    sld = "Shield"
    hlm = "Helmet"
    amu = "Amulet"
    arm = "Armor"
    clk = "Cloak"
    glv = "Gloves"
    rng = "Ring"
    blt = "Belt"
    bts = "Boots"
    acy = "Accessory"


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
