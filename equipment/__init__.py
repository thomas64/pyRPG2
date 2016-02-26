
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
