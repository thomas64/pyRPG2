
"""
class: EquipmentType
class: WeaponType
"""

import enum

from equipment.item import EquipmentItem
import equipment.accessory
import equipment.amulet
import equipment.armor
import equipment.belt
import equipment.boots
import equipment.cloak
import equipment.gloves
import equipment.helmet
import equipment.ring
import equipment.shield
import equipment.weapon

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items


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

    @classmethod
    def get_empty_equipment_item_of_this_type(cls, equipment_type):
        """
        Geeft een 'empty' equipment item terug op verzoek van het type.
        :param equipment_type: Enum EquipmentType.value, dus bijv. "Shield".
        """
        if equipment_type == cls.wpn.value:
            return WeaponDatabase.factory(None)
        elif equipment_type == cls.sld.value:
            return ShieldDatabase.factory(None)
        elif equipment_type == cls.hlm.value:
            return HelmetDatabase.factory(None)
        elif equipment_type == cls.amu.value:
            return AmuletDatabase.factory(None)
        elif equipment_type == cls.arm.value:
            return ArmorDatabase.factory(None)
        elif equipment_type == cls.clk.value:
            return CloakDatabase.factory(None)
        elif equipment_type == cls.glv.value:
            return GlovesDatabase.factory(None)
        elif equipment_type == cls.rng.value:
            return RingDatabase.factory(None)
        elif equipment_type == cls.blt.value:
            return BeltDatabase.factory(None)
        elif equipment_type == cls.bts.value:
            return BootsDatabase.factory(None)
        elif equipment_type == cls.acy.value:
            return AccessoryDatabase.factory(None)


class WeaponType(enum.Enum):
    """
    Alle weapon types en shield op een rij.
    """
    swd = "Sword"
    haf = "Hafted"
    pol = "Pole"
    mis = "Missile"
    thr = "Thrown"
    shd = "Shield"


# Maak van alle equipment databases objecten, om die te kunnen laten gebruiken in het spel.
AccessoryDatabase = equipment.accessory.AccessoryDatabase()
AmuletDatabase = equipment.amulet.AmuletDatabase()
ArmorDatabase = equipment.armor.ArmorDatabase()
BeltDatabase = equipment.belt.BeltDatabase()
BootsDatabase = equipment.boots.BootsDatabase()
CloakDatabase = equipment.cloak.CloakDatabase()
GlovesDatabase = equipment.gloves.GlovesDatabase()
HelmetDatabase = equipment.helmet.HelmetDatabase()
RingDatabase = equipment.ring.RingDatabase()
ShieldDatabase = equipment.shield.ShieldDatabase()
WeaponDatabase = equipment.weapon.WeaponDatabase()
