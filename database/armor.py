
"""
class: ArmorDatabase
"""

# import collections

import enum

import aenum

from constants import EquipmentType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/armor1.png'


class ArmorDatabase(enum.Enum):
    """
    Een lege Enum.
    """


# Vul de Enum met de gecombineerde data.

# todo, upgradable, min_mech, metals zijn nog niet verwerkt.

#                     val, wht, prt, stl,  srt, row,      mtr[6]
armor_material = {
    "Leather Armor":   (0,   0,   0,   0, 1000,   0, ItemMaterial.ltr),
    "Bronze Armor":    (3,   3,   3,  -3, 2000,  32, ItemMaterial.brz),
    "Iron Armor":      (6,   6,   6,  -6, 3000,  64, ItemMaterial.irn),
    "Steel Armor":     (9,   9,   9,  -9, 4000,  96, ItemMaterial.stl),
    "Silver Armor":   (12,  12,  12, -12, 5000, 128, ItemMaterial.slv),
    "Titanium Armor": (15,   0,  12,   0, 6000, 160, ItemMaterial.tnm)
}
#                     val, wht, prt, stl,  srt, col
armor_type = {
    "Light":           (1,   1,   1,   0,  100,   0),
    "Medium":          (2,   2,   2,  -1,  200,  32),
    "Heavy":           (3,   3,   3,  -2,  300,  64)
}
#                     val, wht, prt, stl,  srt
armor_upgraded = {
    "":              (1.0,   0,   0,   0,   10),
    "+":             (1.1,   0,   0,   1,   20),
    "++":            (1.2,  -1,   0,   2,   30)
}
# hoogste protection mogelijk is 15: Heavy Silver/Titanium Armor /+/++

for material_key, material_value in armor_material.items():
    for type_key, type_value in armor_type.items():
        for upgraded_key, upgraded_value in armor_upgraded.items():

            raw_key_name = (type_key + material_key + upgraded_key).strip().lower().replace(" ", "")
            price = (material_value[0] + type_value[0])**2 + 10

            aenum.extend_enum(ArmorDatabase, raw_key_name, dict(

                nam=(type_key + " " + material_key + " " + upgraded_key).strip(),

                # puur voor sortering in de database, omdat geen enum is
                srt=material_value[4] + type_value[4] + upgraded_value[4],

                # berekening value: material * type * upgraded
                val=int(price * upgraded_value[0]),
                shp=True,

                mtr=material_value[6],

                # berekening weight: material + type + upgraded
                wht=material_value[1] + type_value[1] + upgraded_value[1],

                # berekening protection: material + type
                prt=material_value[2] + type_value[2],

                # berekening stealth: material + type + upgraded
                stl=material_value[3] + type_value[3] + upgraded_value[3],

                col=type_value[5],
                row=material_value[5]
            ))

# type en sprite toepassen.
# shop uitzetten voor sommige equipment items.
for eqp in ArmorDatabase:
    eqp.value['typ'] = EquipmentType.arm
    eqp.value['spr'] = SPRITEPATH
    if "+" in eqp.name or "titanium" in eqp.name:
        eqp.value['shp'] = False
# de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

# # Herschik de volgorde van de gecreerde dataset.
# temp_dict = collections.OrderedDict()
# # sorteer en zet in nieuwe database
# for eqp_key, eqp_value in sorted(arm.items(), key=lambda xx: xx[1]['srt']):
#     temp_dict[eqp_key] = eqp_value
# # maak eigen database leeg
# arm.clear()
# # zet de gesorteerde neer
# for eqp_key, eqp_value in temp_dict.items():
#     arm[eqp_key] = eqp_value
