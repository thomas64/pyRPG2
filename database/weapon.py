
"""
class: WeaponDatabase
"""

import enum
import aenum

from constants import EquipmentType
from constants import WeaponType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/weapon1.png'


class WeaponDatabase(enum.Enum):
    """
    Een lege Enum. (met customs)
    """
    customsword = dict(nam="Custom Sword", srt=1, val=2, shp=False, min_str='X', dam='X', hit='X', skl=WeaponType.swd, col=0,   row=672,
                       min_min_str=25, max_min_str=5, min_dam=10, max_dam=24, min_hit=35, max_hit=75,
                       cus=True, clt=2, ltr=3, wod=4,  mtl=20,
                       desc=("Creating a Custom Sword requires 2 Cloth, 3 Leather, 4 Wood and 20 metals.", " ",
                             "Min. Strength: 5 - 25", "Hit Chance: 35% - 75%", "Damage: 10 - 24"))
    customaxe = dict(nam="Custom Axe",     srt=2, val=2, shp=False, min_str='X', dam='X', hit='X', skl=WeaponType.haf, col=32,  row=672,
                     min_min_str=31, max_min_str=11, min_dam=16, max_dam=30, min_hit=25, max_hit=65,
                     cus=True, clt=2, ltr=3, wod=6,  mtl=18,
                     desc=("Creating a Custom Sword requires 2 Cloth, 3 Leather, 4 Wood and 20 metals.", " ",
                           "Min. Strength: 11 - 31", "Hit Chance: 25% - 65%", "Damage: 16 - 30"))
    customspear = dict(nam="Custom Spear", srt=3, val=2, shp=False, min_str='X', dam='X', hit='X', skl=WeaponType.pol, col=64,  row=672,
                       min_min_str=21, max_min_str=7, min_dam=4, max_dam=18, min_hit=45, max_hit=85,
                       cus=True, clt=3, ltr=4, wod=10, mtl=12,
                       desc=("Creating a Custom Spear requires 3 Cloth, 4 Leather, 10 Wood and 12 metals.", " ",
                             "Min. Strength: 7 - 21", "Hit Chance: 45% - 85%", "Damage: 4 - 18"))
    custombow = dict(nam="Custom Bow",     srt=4, val=2, shp=False, min_int='X', dam='X', hit='X', skl=WeaponType.mis, col=96,  row=672,
                     min_min_int=30, max_min_int=13, min_dam=10, max_dam=24, min_hit=35, max_hit=75,
                     cus=True, clt=5, ltr=2, wod=20, mtl=2,
                     desc=("Creating a Custom Bow requires 5 Cloth, 2 Leather, 20 Wood and 2 metals.", " ",
                           "Min. Intelligence: 13 - 30", "Hit Chance: 35% - 75%", "Damage: 10 - 24"))
    customknife = dict(nam="Custom Knife", srt=5, val=2, shp=False, min_str='X', dam='X', hit='X', skl=WeaponType.thr, col=128, row=672,
                       min_min_str=29, max_min_str=3, min_dam=4, max_dam=18, min_hit=25, max_hit=65,
                       cus=True, clt=1, ltr=2, wod=1,  mtl=15,
                       desc=("Creating a Custom Knife requires 1 Cloth, 2 Leather, 1 Wood and 15 metals.", " ",
                             "Min. Strength: 3 - 29", "Hit Chance: 25% - 65%", "Damage: 4 - 18"))


for equipment_item in WeaponDatabase:
    equipment_item.value['typ'] = EquipmentType.wpn
    equipment_item.value['spr'] = SPRITEPATH

# Vul de Enum met de gecombineerde data.

#                     val, min int, min str, dam, srt, col,     mtr[6]
weapon_material = {
    "Bronze":          (1,       0,       0,   3, 100,   0, ItemMaterial.brz),
    "Iron":            (2,       1,       1,   6, 200,  32, ItemMaterial.irn),
    "Steel":           (3,       2,       2,   9, 300,  64, ItemMaterial.stl),
    "Silver":          (4,       3,       3,  12, 400,  96, ItemMaterial.slv),
    "Titanium":        (5,       1,       1,  12, 500, 128, ItemMaterial.tnm)
}
#                     val, min int, min str, hit, dam,            skl, typ,   srt, row
weapon_type = {
    "Dagger":          (3,       0,       6,  40,   8, WeaponType.swd,   2,  1000,   0),
    "Short Sword":     (5,       0,      10,  50,   9, WeaponType.swd,   2,  2000,  32),
    "Longsword":       (7,       0,      14,  60,  10, WeaponType.swd,   2,  3000,  64),
    "Broadsword":      (9,       0,      18,  70,  11, WeaponType.swd,   2,  4000,  96),

    "Mace":            (4,       0,      12,  30,  14, WeaponType.haf,   3,  5000, 128),
    "Axe":             (6,       0,      15,  40,  15, WeaponType.haf,   3,  6000, 160),
    "Poleaxe":         (8,       0,      18,  50,  16, WeaponType.haf,   3,  7000, 192),
    "Maul":           (10,       0,      21,  60,  17, WeaponType.haf,   3,  8000, 224),

    "Staff":           (2,       0,       8,  50,   2, WeaponType.pol,   1,  9000, 256),
    "Spear":           (4,       0,      11,  60,   3, WeaponType.pol,   1, 10000, 288),
    "Pike":            (6,       0,      14,  70,   4, WeaponType.pol,   1, 11000, 320),
    "Lance":           (8,       0,      17,  80,   5, WeaponType.pol,   1, 12000, 352),

    "Shortbow":        (5,      14,       0,  40,   8, WeaponType.mis,   4, 13000, 384),
    "Longbow":         (7,      18,       0,  50,   9, WeaponType.mis,   4, 14000, 416),
    "Great Bow":       (9,      22,       0,  60,  10, WeaponType.mis,   4, 15000, 448),
    "Crossbow":       (11,      26,       0,  70,  11, WeaponType.mis,   4, 16000, 480),

    "Dart":            (1,       0,       4,  30,   2, WeaponType.thr,   2, 17000, 512),
    "Knife":           (3,       0,      10,  40,   3, WeaponType.thr,   2, 18000, 544),
    "Hatchet":         (5,       0,      16,  50,   4, WeaponType.thr,   2, 19000, 576),
    "Javelin":         (7,       0,      22,  60,   5, WeaponType.thr,   2, 20000, 608)
}
#                     val, hit, dam, srt
weapon_upgraded = {
    "":              (1.0,   0,   0,  10),
    "+":             (1.1,   5,   0,  20),
    "++":            (1.2,   5,   1,  30)
}
# hoogste damage mogelijk is 30: Silver/Titanium Maul ++

temp_weapon_dict = {}

for material_key, material_value in weapon_material.items():
    for type_key, type_value in weapon_type.items():
        for upgraded_key, upgraded_value in weapon_upgraded.items():

            raw_key_name = (material_key + type_key + upgraded_key).strip().lower().replace(" ", "")
            price = (material_value[0] + type_value[0])**2.3

            temp_weapon_dict[raw_key_name] = dict(
                nam=(material_key + " " + type_key + " " + upgraded_key).strip(),

                # voor sortering in de winkels
                srt=material_value[4] + type_value[7] + upgraded_value[3],

                # berekening value: material * type * upgraded
                val=int(price * upgraded_value[0]),
                shp=True,

                skl=type_value[5],
                mtr=material_value[6],

                # berekening min int/str: material * type_const + type
                min_int=material_value[1] + type_value[1],
                min_str=material_value[2] * type_value[6] + type_value[2],

                # berekening base hit: type + upgraded
                hit=type_value[3] + upgraded_value[1],

                # berekening damage: material + type + upgraded
                dam=material_value[3] + type_value[4] + upgraded_value[2],

                col=material_value[5],
                row=type_value[8]
            )

# min_int op 0 zetten voor close weapons
# min_str op 0 zetten voor range weapons
for weapon_key, weapon_value in temp_weapon_dict.items():
    if weapon_value['skl'] == WeaponType.mis:
        weapon_value['min_str'] = 0
    else:
        weapon_value['min_int'] = 0
# Shop uitzetten voor sommige equipment items.
for eqp_key, eqp_value in temp_weapon_dict.items():
    eqp_value['typ'] = EquipmentType.wpn
    eqp_value['spr'] = SPRITEPATH
    if "+" in eqp_key or "titanium" in eqp_key:
        eqp_value['shp'] = False
# de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

# Herschik de volgorde van de gecreerde dataset.
# sorteer en zet in nieuwe database
for eqp_key, eqp_value in sorted(temp_weapon_dict.items(), key=lambda xx: xx[1]['srt']):
    aenum.extend_enum(WeaponDatabase, eqp_key, eqp_value)
# maak eigen database leeg
temp_weapon_dict.clear()
