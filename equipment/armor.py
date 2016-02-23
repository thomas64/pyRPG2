
"""
class: ArmorDatabase
"""

import collections

import equipment.equipment as eqp

SPRITEPATH = ''


class ArmorDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # Vul de OrderedDict self met de gecombineerde data.

        # todo, col, row, upgradable, min_mech, metals zijn nog niet verwerkt.

        #                       val,    wht, prt, stl,  srt
        armor_material = {
            "Leather Armor":   (100,      0,   0,   0, 1000),
            "Bronze Armor":    (600,      3,   3,  -3, 2000),
            "Iron Armor":     (1100,      6,   6,  -6, 3000),
            "Steel Armor":    (1600,      9,   9,  -9, 4000),
            "Silver Armor":   (2100,     12,  12, -12, 5000),
            "Titanium Armor": (2600,      0,  12,   0, 6000)
            # "Stealth":        (16,     10,   1,   1)
        }
        #                       val,    wht, prt, stl,  srt
        armor_type = {
            "Light":           (100,      1,   1,   0,  100),
            "Medium":          (300,      2,   2,  -1,  200),
            "Heavy":           (500,      3,   3,  -2,  300)
        }
        #                       val,    wht, prt, stl,  srt
        armor_upgraded = {
            "":                (1.0,      0,   0,   0,   10),
            "+":               (1.1,      0,   0,   1,   20),
            "++":              (1.2,     -1,   0,   2,   30)
        }
        # hoogste protection mogelijk is 15: Heavy Silver/Titanium Armor /+/++

        for material_key, material_value in armor_material.items():
            for type_key, type_value in armor_type.items():
                for upgraded_key, upgraded_value in armor_upgraded.items():

                    raw_key_name = (type_key + material_key + upgraded_key).strip().lower().replace(" ", "")
                    # todo, deze int was alleen bij weapon, moet de int hier weer weg?
                    price = int((material_value[0] + type_value[0]) * (material_value[0] + type_value[0]) / 400)

                    self[raw_key_name] = dict(
                        nam=(type_key + " " + material_key + " " + upgraded_key).strip(),

                        # puur voor sortering in de database, omdat geen enum is
                        srt=material_value[4] + type_value[4] + upgraded_value[4],

                        # berekening value: material * type * upgraded
                        val=int(price * upgraded_value[0]),
                        shp=True,

                        # berekening weight: material + type + upgraded
                        wht=material_value[1] + type_value[1] + upgraded_value[1],

                        # berekening protection: material + type
                        prt=material_value[2] + type_value[2],

                        # berekening stealth: material + type + upgraded
                        stl=material_value[3] + type_value[3] + upgraded_value[3]
                    )

        # Shop uitzetten voor sommige equipment items.
        for eqp_key, eqp_value in self.items():
            if "+" in eqp_key or "titanium" in eqp_key:
                eqp_value['shp'] = False
        # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable

        # Herschik de volgorde van de gecreerde dataset.
        temp_dict = collections.OrderedDict()
        # sorteer en zet in nieuwe database
        for eqp_key, eqp_value in sorted(self.items(), key=lambda xx: xx[1]['srt']):
            temp_dict[eqp_key] = eqp_value
        # maak eigen database leeg
        self.clear()
        # zet de gesorteerde neer
        for eqp_key, eqp_value in temp_dict.items():
            self[eqp_key] = eqp_value

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return eqp.EquipmentItem(eqp.EquipmentType.arm)
        armor = self[key_name]
        armor['spr'] = SPRITEPATH
        return eqp.EquipmentItem(eqp.EquipmentType.arm, **armor)
