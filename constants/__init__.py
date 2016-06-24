
"""
class: Direction
class: PersonState
class: EquipmentType
class: WeaponType
class: ItemMaterial
class: SchoolType
"""

import enum


class Direction(enum.Enum):
    """
    De vier richtingen waarheen een unit kan lopen.
    """
    North = 1
    South = 2
    West = 3
    East = 4


class PersonState(enum.Enum):
    """
    Wat kan een NPC doen?
    """
    Resting = 1
    Moving = 2


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


class ItemMaterial(enum.Enum):
    """
    Alle materialen op een rij.
    """
    ltr = "Leather"
    wdn = "Wooden"
    brz = "Bronze"
    irn = "Iron"
    stl = "Steel"
    slv = "Silver"
    tnm = "Titanium"


class SchoolType(enum.Enum):
    """
    De 7 wizard schools.
    """
    non = ""
    spl = "Special"
    ntl = "Neutral"
    elm = "Elemental"
    nmg = "Naming"
    ncy = "Necromancy"
    str = "Star"
