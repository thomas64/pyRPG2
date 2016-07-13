
"""
class: Direction
class: PersonState
class: EquipmentType
class: WeaponType
class: ItemMaterial
class: SchoolType
class: Minimals
class: StatType
class: SkillType
class: SpellType
class: QuestType
class: QuestState
class: MapMusic
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
    ctn = "Cotton"
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


class Minimals(enum.Enum):
    """
    Substring wordt gebruikt om de eerste 4 chars van de .name te halen.
    Substring wordt gebruikt om de eerste 5 chars van de .value te halen.
    """
    min_int = "Min. Intelligence"
    min_wil = "Min. Willpower"
    min_dex = "Min. Dexterity"
    min_str = "Min. Strength"
    min_wiz = "Min. Wizard"


class StatType(enum.Enum):
    """..."""
    wht = "Weight"
    mvp = "Movepoints"
    prt = "Protection"
    des = "Defense"
    hit = "Hit Chance"
    dam = "Damage"

    int = "Intelligence"
    wil = "Willpower"
    dex = "Dexterity"
    agi = "Agility"
    edu = "Endurance"
    str = "Strength"
    sta = "Stamina"


class SkillType(enum.Enum):
    """..."""
    alc = "Alchemist"
    dip = "Diplomat"
    hlr = "Healer"
    lor = "Loremaster"
    mec = "Mechanic"
    mer = "Merchant"
    ran = "Ranger"
    stl = "Stealth"
    thf = "Thief"
    trb = "Troubadour"
    war = "Warrior"
    wiz = "Wizard"
    haf = "Hafted"
    mis = "Missile"
    pol = "Pole"
    shd = "Shield"
    swd = "Sword"
    thr = "Thrown"


class SpellType(enum.Enum):
    """..."""
    dis_nmg = "Dispel Naming"
    dis_ncy = "Dispel Necro"
    dis_str = "Dispel Star"
    mir = "Mirror"
    vs_elm = "vs. Elemental"
    vs_nmg = "vs. Naming"
    vs_ncy = "vs. Necromancy"
    vs_str = "vs. Star"

    air_sld = "Air Shield"
    deb = "Debilitation"
    drg_flm = "Dragon Flames"
    frb = "Fireball"
    imo = "Immolation"
    rem_psn = "Remove Poison"
    str = "Strength"
    wnd = "Wind"

    ban = "Banishing"
    edu = "Endurance"
    sen_aur = "Sense Aura"
    tlp = "Teleportation"
    wks = "Weakness"

    frz_dom = "Frozen Doom"
    sol_wrt = "Solar Wrath"
    stl_gty = "Stellar Gravity"
    wos = "Web of Starlight"
    wfi = "Whitefire"

    ctr_zom = "Control Zombies"
    hst = "Haste"
    wob = "Wall of Bones"
    spr_sld = "Spirit Shield"


class QuestType(enum.Enum):
    """..."""
    ItemQuest = 1
    PersonQuest = 2
    EnemyQuest = 3


class QuestState(enum.Enum):
    """
    De volgorde en de 1, 2, 3, 4 worden in het spel gebruikt. Kan dus niet zomaar aangepast worden.
    Dit heeft met de tekst in QuestDatabase te maken en get_text() in QuestItem.
    """
    Unknown = 1
    Running = 2
    Finished = 3
    Rewarded = 4


class MapMusic(enum.Enum):
    """
    Alle tmx kaarten op een rij, met de muziek erachter en ambient sound.
    De key's komen precies overeen met de .tmx namen. De values[0] en [1] komen overeen met de .ogg namen.
    """
    ersin_forest_start =        'ersin_forest',  'birds'
    ersin_forest_waterfall =    'ersin_forest',  'river'
    ersin_forest_center =       'ersin_forest',  'birds'
    ersin_forest_cave =         'ersin_forest',  'birds'
    ersin_cave_room1 =          'ersin_cave',    None
    ersin_cave_room2 =          'ersin_cave',    None
    ersin_cave_room3 =          'ersin_cave',    None
    invernia_town =             'invernia_town', 'town'
    invernia_armor_shop =       'invernia_town', None
    invernia_weapon_shop =      'invernia_town', None
    invernia_item_shop =        'invernia_town', None
    invernia_inn_1f =           'invernia_town', None
    invernia_inn_2f =           'invernia_town', None
    invernia_guild =            'invernia_town', 'fire'
    invernia_school =           'invernia_town', None
    invernia_house_big_1f =     'invernia_town', None
    invernia_house_big_2f =     'invernia_town', None
    invernia_house_left =       'invernia_town', None
    invernia_house_right =      'invernia_town', None
