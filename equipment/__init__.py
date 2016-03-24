
"""
class: EquipmentType
class: WeaponType
"""

import enum

from equipment.item import EquipmentItem
import database.weapon
import database.shield
import database.helmet
import database.amulet
import database.armor
import database.cloak
import database.bracelet
import database.gloves
import database.ring
import database.belt
import database.boots
import database.accessory

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
    brc = "Bracelet"
    glv = "Gloves"
    rng = "Ring"
    blt = "Belt"
    bts = "Boots"
    acy = "Accessory"

    @classmethod
    def get_equipment_item_of_this_type(cls, equipment_type, equipment_item_key):
        """
        Geeft een equipment item terug op verzoek van het type en de key, geef een 'empty' terug bij key = None.
        :param equipment_type: Enum EquipmentType.value, dus bijv. "Shield".
        :param equipment_item_key: een sleutel uit de eqp items databases bijv "bronzeshortsword"
        """
        if equipment_type == cls.wpn.value:
            return WeaponDatabase.factory(equipment_item_key)
        elif equipment_type == cls.sld.value:
            return ShieldDatabase.factory(equipment_item_key)
        elif equipment_type == cls.hlm.value:
            return HelmetDatabase.factory(equipment_item_key)
        elif equipment_type == cls.amu.value:
            return AmuletDatabase.factory(equipment_item_key)
        elif equipment_type == cls.arm.value:
            return ArmorDatabase.factory(equipment_item_key)
        elif equipment_type == cls.clk.value:
            return CloakDatabase.factory(equipment_item_key)
        elif equipment_type == cls.brc.value:
            return BraceletDatabase.factory(equipment_item_key)
        elif equipment_type == cls.glv.value:
            return GlovesDatabase.factory(equipment_item_key)
        elif equipment_type == cls.rng.value:
            return RingDatabase.factory(equipment_item_key)
        elif equipment_type == cls.blt.value:
            return BeltDatabase.factory(equipment_item_key)
        elif equipment_type == cls.bts.value:
            return BootsDatabase.factory(equipment_item_key)
        elif equipment_type == cls.acy.value:
            return AccessoryDatabase.factory(equipment_item_key)


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
AccessoryDatabase = database.accessory.AccessoryDatabase()
AmuletDatabase = database.amulet.AmuletDatabase()
ArmorDatabase = database.armor.ArmorDatabase()
BeltDatabase = database.belt.BeltDatabase()
BootsDatabase = database.boots.BootsDatabase()
CloakDatabase = database.cloak.CloakDatabase()
BraceletDatabase = database.bracelet.BraceletDatabase()
GlovesDatabase = database.gloves.GlovesDatabase()
HelmetDatabase = database.helmet.HelmetDatabase()
RingDatabase = database.ring.RingDatabase()
ShieldDatabase = database.shield.ShieldDatabase()
WeaponDatabase = database.weapon.WeaponDatabase()
