
"""
class: ShieldDatabase
"""

import enum
import aenum

from constants import EquipmentType
from constants import WeaponType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/shield4.png'


class ShieldDatabase(enum.Enum):
    """
    Een lege Enum. (met custom)
    """
    customshield = dict(nam="Custom Shield", srt=1, val=2, shp=False,
                        min_str='X', prt='X', des='X', dex='X', stl='X', col=192, row=0,
                        min_min_str=31, max_min_str=5, min_prt=2, max_prt=16, min_des=5, max_des=31,
                        min_dex=-11, max_dex=-1, min_stl=-21, max_stl=-3,
                        cus=True, clt=0, ltr=2, wod=18, mtl=12,
                        desc=("Creating a Custom Shield requires 2 Leather, 18 Wood and 12 metals.", " ",
                              "Min. Strength: 5 - 31", "Protection: 2 - 16", "Defense: 5 - 31", "Dexterity -11 - -1",
                              "Stealth: -21 - -3"))


for equipment_item in ShieldDatabase:
    equipment_item.value['typ'] = EquipmentType.sld
    equipment_item.value['skl'] = WeaponType.shd
    equipment_item.value['spr'] = SPRITEPATH


# Vul de Enum met de gecombineerde data.

#                     val, min str, prt, des, dex, stl,  srt, col,      mtr[8]
shield_material = {
    "Wooden":          (3,       3,   2,   1,  -1,  -1,  100,   0, ItemMaterial.wdn),
    "Bronze":          (6,       6,   4,   2,  -2,  -2,  200,  32, ItemMaterial.brz),
    "Iron":            (9,       9,   6,   3,  -3,  -3,  300,  64, ItemMaterial.irn),
    "Steel":          (12,      12,   8,   4,  -4,  -4,  400,  96, ItemMaterial.stl),
    "Silver":         (15,      15,  10,   5,  -5,  -5,  500, 128, ItemMaterial.slv),
    "Titanium":       (18,       6,  10,   5,  -1,  -1,  600, 160, ItemMaterial.tnm)
}
#                     val, min str, prt, des, dex, stl,  srt, row
shield_type = {
    "Buckler":         (4,       3,   1,   5,  -1,  -3, 1000,   0),
    "Targe":           (8,       6,   2,  10,  -2,  -6, 2000,  32),
    "Heater":         (12,       9,   3,  15,  -3,  -9, 3000,  64),
    "Kite":           (16,      12,   4,  20,  -4, -12, 4000,  96),
    "Scutum":         (20,      15,   5,  25,  -5, -15, 5000, 128)
}
#                     val, min str, prt, des, dex, stl,  srt
shield_upgraded = {
    "":              (1.0,       0,   0,   0,   0,   0,   10),
    "+":             (1.1,       0,   0,   0,   1,   2,   20),
    "++":            (1.2,       0,   0,   0,   2,   4,   30)
}
# de hoogste protection/defense mogelijk is 15/30: Large Silver/Titanium Scutum /+/++

temp_shield_dict = {}

for material_key, material_value in shield_material.items():
    for type_key, type_value in shield_type.items():
        for upgraded_key, upgraded_value in shield_upgraded.items():

            raw_key_name = (material_key + type_key + upgraded_key).strip().lower().replace(" ", "")
            price = (material_value[0] + type_value[0])**1.6 - 10

            temp_shield_dict[raw_key_name] = dict(
                nam=(material_key + " " + type_key + " " + upgraded_key).strip(),

                # voor sortering in de database
                srt=material_value[6] + type_value[6] + upgraded_value[6],

                # berekening value: material * type * upgraded
                val=int(price * upgraded_value[0]),
                shp=True,

                mtr=material_value[8],

                # berekening min str: material + type
                min_str=material_value[1] + type_value[1],

                # berekening protection: material + type
                prt=material_value[2] + type_value[2],

                # berekening defense: material + type
                des=material_value[3] + type_value[3],  # 'def' kon niet, dus maar des gedaan.

                # berekening dexterity: material + type + upgraded
                dex=material_value[4] + type_value[4] + upgraded_value[4],

                # berekening stealth: material + type + upgraded
                stl=material_value[5] + type_value[5] + upgraded_value[5],

                col=material_value[7],
                row=type_value[7]
            )

# type, skill en sprite toepassen.
# Shop uitzetten voor sommige equipment items.
for eqp_key, eqp_value in temp_shield_dict.items():
    eqp_value['typ'] = EquipmentType.sld
    eqp_value['skl'] = WeaponType.shd
    eqp_value['spr'] = SPRITEPATH
    if "+" in eqp_key or "titanium" in eqp_key:
        eqp_value['shp'] = False
# de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

# Herschik de volgorde van de gecreerde dataset.
# sorteer en zet in nieuwe database
for eqp_key, eqp_value in sorted(temp_shield_dict.items(), key=lambda xx: xx[1]['srt']):
    aenum.extend_enum(ShieldDatabase, eqp_key, eqp_value)
# maak eigen database leeg
temp_shield_dict.clear()
