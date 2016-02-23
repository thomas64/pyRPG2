
"""
class: EquipmentDatabase
class: EquipmentType
class: EquipmentItem
"""

import collections
import enum

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items


class EquipmentDatabase(collections.OrderedDict):
    """
    Alle equipment data classes kunnen erven van deze class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):                 # om er in een winkel doorheen te kunnen gaan loopen
        return iter(self.items())

    def __getattr__(self, key):         # om een nieuwe aan te kunnen maken met factory. anders herkent hij de woodenb.
        return self[key]                # niet als een attribute: piet = ShieldsData.factory(ShieldsData.woodenbuckler)

    def set_shop(self):
        """
        Shop uitzetten voor sommige equipment items.
        """
        for eqp_key, eqp_value in self.items():
            if "+" in eqp_key or "titanium" in eqp_key:
                eqp_value['shp'] = False
        # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

    def rearrage(self):
        """
        Herschik de volgorde van de gecreerde dataset.
        """
        temp_dict = collections.OrderedDict()
        # sorteer en zet in nieuwe database
        for eqp_key, eqp_value in sorted(self.items(), key=lambda xx: xx[1]['srt']):
            temp_dict[eqp_key] = eqp_value
        # maak eigen database leeg
        self.clear()
        # zet de gesorteerde neer
        for eqp_key, eqp_value in temp_dict.items():
            self[eqp_key] = eqp_value


class EquipmentType(enum.Enum):
    """
    Alle equipment typen op een rij.
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


class EquipmentItem(object):
    """
    Een EquipmentItem object met attributen als de waarden van de extra's die het item heeft zoals THF.
    """
    def __init__(self, equipment_type, **kwargs):
        self.TYP = equipment_type                                       # Enum van EquipmentType
        self.qty = 1

        for eqp_value_key, eqp_value_value in kwargs.items():
            setattr(self, eqp_value_key.upper(), eqp_value_value)       # zet de dict van kwargs om in attributen

        try:
            # noinspection PyUnresolvedReferences
            self.RAW = self.NAM.strip().lower().replace(" ", "")        # als er een NAM is, geef hem een RAW
        except AttributeError:
            pass
        try:
            # noinspection PyUnresolvedReferences
            del self.SHP
        except AttributeError:
            pass

    def get_value_of(self, attr):
        """
        Vraagt een attribute op van een EquipmentItem. De RAW van bijv een skill is in lower zoals 'alc', maar de
        'alc' van een EquipmentItem is self.ALC, vandaar de upper().
        :param attr: sting, het opgevraagde attribute
        :return: de waarde van het attribute, en zo niet bestaand, nul.
        """
        return getattr(self, attr.upper(), 0)

    def is_not_empty(self):
        """
        Bekijkt of de EquipmentItem een 'empty' is, door te checken op attribute NAM.
        :return: True wanneer de NAM bestaat, want hij is niet empty. Anders False, want hij ís empty.
        """
        if hasattr(self, 'NAM'):
            return True
        return False
