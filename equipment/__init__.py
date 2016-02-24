
"""
class: EquipmentType
class: EquipmentItem
"""

import enum

import equipment.accessory
import equipment.amulet
import equipment.armor
import equipment.belt
import equipment.boots
import equipment.cloak
import equipment.gloves
import equipment.helmet

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items

AccessoryDatabase = equipment.accessory.AccessoryDatabase()
AmuletDatabase = equipment.amulet.AmuletDatabase()
ArmorDatabase = equipment.armor.ArmorDatabase()
BeltDatabase = equipment.belt.BeltDatabase()
BootsDatabase = equipment.boots.BootsDatabase()
CloakDatabase = equipment.cloak.CloakDatabase()
GlovesDatabase = equipment.gloves.GlovesDatabase()
HelmetDatabase = equipment.helmet.HelmetDatabase()


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
            del self.SHP                                        # deze is niet nodig wanneer het een object geworden is.
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
