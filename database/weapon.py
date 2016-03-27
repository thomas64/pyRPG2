
"""
Weapon
"""

import collections

from . import EquipmentType
from . import WeaponType


SPRITEPATH = 'resources/sprites/icons/equipment/weapon1.png'

w = collections.OrderedDict()

# Vul de OrderedDict self met de gecombineerde data.

# todo, upgradable, min_mech, metals zijn nog niet verwerkt.

#                     val, min int/str, dam, srt, col
weapon_material = {
    "Bronze":        (100,           0,   3, 100,   0),
    "Iron":          (900,           1,   6, 200,  32),
    "Steel":        (1700,           2,   9, 300,  64),
    "Silver":       (2500,           3,  12, 400,  96),
    "Titanium":     (3300,           0,  12, 500, 128)
}
#                     val, min int, min str, hit, dam,            skl, typ,   srt, row
weapon_type = {
    "Dagger":        (100,       0,       6,  40,   8, WeaponType.swd,   2,  1000,   0),
    "Short Sword":   (200,       0,      10,  50,   9, WeaponType.swd,   2,  2000,  32),
    "Longsword":     (400,       0,      14,  60,  10, WeaponType.swd,   2,  3000,  64),
    "Broadsword":    (800,       0,      18,  70,  11, WeaponType.swd,   2,  4000,  96),

    "Mace":          (150,       0,      12,  30,  14, WeaponType.haf,   3,  5000, 128),
    "Axe":           (300,       0,      15,  40,  15, WeaponType.haf,   3,  6000, 160),
    "Poleaxe":       (600,       0,      18,  50,  16, WeaponType.haf,   3,  7000, 192),
    "Maul":         (1200,       0,      21,  60,  17, WeaponType.haf,   3,  8000, 224),

    "Staff":          (75,       0,       8,  50,   2, WeaponType.pol,   1,  9000, 256),
    "Spear":         (150,       0,      11,  60,   3, WeaponType.pol,   1, 10000, 288),
    "Pike":          (300,       0,      14,  70,   4, WeaponType.pol,   1, 11000, 320),
    "Lance":         (600,       0,      17,  80,   5, WeaponType.pol,   1, 12000, 352),

    "Shortbow":      (200,      10,       0,  40,   8, WeaponType.mis,   4, 13000, 384),
    "Longbow":       (400,      12,       0,  50,   9, WeaponType.mis,   4, 14000, 416),
    "Great Bow":     (800,      14,       0,  60,  10, WeaponType.mis,   4, 15000, 448),
    "War Bow":      (1600,      16,       0,  70,  11, WeaponType.mis,   4, 16000, 480),

    "Dart":           (50,       4,       0,  30,   2, WeaponType.thr,   2, 17000, 512),
    "Knife":         (100,      10,       0,  40,   3, WeaponType.thr,   2, 18000, 544),
    "Hatchet":       (200,      16,       0,  50,   4, WeaponType.thr,   2, 19000, 576),
    "Javelin":       (400,      22,       0,  60,   5, WeaponType.thr,   2, 20000, 608)
}
#                     val, hit, dam, srt
weapon_upgraded = {
    "":              (1.0,   0,   0,  10),
    "+":             (1.1,   5,   0,  20),
    "++":            (1.2,   5,   1,  30)
}
# hoogste damage mogelijk is 30: Silver/Titanium Maul ++

for material_key, material_value in weapon_material.items():
    for type_key, type_value in weapon_type.items():
        for upgraded_key, upgraded_value in weapon_upgraded.items():

            raw_key_name = (material_key + type_key + upgraded_key).strip().lower().replace(" ", "")

            price = int((material_value[0] + type_value[0]) * (material_value[0] + type_value[0]) / 400)

            w[raw_key_name] = dict(
                nam=(material_key + " " + type_key + " " + upgraded_key).strip(),

                # puur voor sortering in de winkels
                srt=material_value[3] + type_value[7] + upgraded_value[3],

                # berekening value: material * type * upgraded
                val=int(price * upgraded_value[0]),
                shp=True,
                skl=type_value[5],

                # berekening min int/str: material * type_const + type
                min_int=material_value[1] * type_value[6] + type_value[1],
                min_str=material_value[1] * type_value[6] + type_value[2],

                # berekening base hit: type + upgraded
                hit=type_value[3] + upgraded_value[1],

                # berekening damage: material + type + upgraded
                dam=material_value[2] + type_value[4] + upgraded_value[2],

                col=material_value[4],
                row=type_value[8]
            )

# min_int op 0 zetten voor close weapons
# min_str op 0 zetten voor range weapons
for weapon_key, weapon_value in w.items():
    if weapon_value['skl'] in (WeaponType.swd,
                               WeaponType.haf,
                               WeaponType.pol):
        weapon_value['min_int'] = 0
    elif weapon_value['skl'] in (WeaponType.mis,
                                 WeaponType.thr):
        weapon_value['min_str'] = 0

# Shop uitzetten voor sommige equipment items.
for eqp_key, eqp_value in w.items():
    eqp_value['typ'] = EquipmentType.wpn
    eqp_value['spr'] = SPRITEPATH
    if "+" in eqp_key or "titanium" in eqp_key:
        eqp_value['shp'] = False
# de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

# Herschik de volgorde van de gecreerde dataset.
temp_dict = collections.OrderedDict()
# sorteer en zet in nieuwe database
for eqp_key, eqp_value in sorted(w.items(), key=lambda xx: xx[1]['srt']):
    temp_dict[eqp_key] = eqp_value
# maak eigen database leeg
w.clear()
# zet de gesorteerde neer
for eqp_key, eqp_value in temp_dict.items():
    w[eqp_key] = eqp_value