
"""
class: WeaponsDataClass
obj: WeaponsData
"""

import equipment.equipment

SPRITEPATH = 'resources/sprites/icons/gear/weapon1.png'


class WeaponsDataClass(equipment.equipment.GearDataClass):
    """
    Hier staan alle wapens uit het spel in een dict als enum met een dict voor de waarden.
    """

    @staticmethod
    def factory(weapon):
        """
        Maak een object van een enum database item.
        :param weapon: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if weapon is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.weapon, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.weapon, SPRITEPATH, **weapon)

    def __init__(self):
        super().__init__()

        # Vul de OrderedDict self.inside met de gecombineerde data.

        # todo, upgradable, min_mech, metals zijn nog niet verwerkt.

        #                     val, min int/str, dam, srt, col
        weapon_material = {
            "Bronze":        (100,           0,   3, 100,   0),
            "Iron":          (900,           1,   6, 200,  32),
            "Steel":        (1700,           2,   9, 300,  64),
            "Silver":       (2500,           3,  12, 400,  96),
            "Titanium":     (3300,           0,  12, 500, 128)
        }
        #                     val, min int, min str, hit, dam,     skl,  typ,   srt, row
        weapon_type = {
            "Dagger":        (100,       0,       6,  40,   8, "Sword",    2,  1000,   0),
            "Short Sword":   (200,       0,      10,  50,   9, "Sword",    2,  2000,  32),
            "Longsword":     (400,       0,      14,  60,  10, "Sword",    2,  3000,  64),
            "Broadsword":    (800,       0,      18,  70,  11, "Sword",    2,  4000,  96),

            "Mace":          (150,       0,      12,  30,  14, "Hafted",   3,  5000, 128),
            "Axe":           (300,       0,      15,  40,  15, "Hafted",   3,  6000, 160),
            "Poleaxe":       (600,       0,      18,  50,  16, "Hafted",   3,  7000, 192),
            "Maul":         (1200,       0,      21,  60,  17, "Hafted",   3,  8000, 224),

            "Staff":          (75,       0,       8,  50,   2, "Pole",     1,  9000, 256),
            "Spear":         (150,       0,      11,  60,   3, "Pole",     1, 10000, 288),
            "Pike":          (300,       0,      14,  70,   4, "Pole",     1, 11000, 320),
            "Lance":         (600,       0,      17,  80,   5, "Pole",     1, 12000, 352),

            "Shortbow":      (200,      10,       0,  40,   8, "Missile",  4, 13000, 384),
            "Longbow":       (400,      12,       0,  50,   9, "Missile",  4, 14000, 416),
            "Great Bow":     (800,      14,       0,  60,  10, "Missile",  4, 15000, 448),
            "War Bow":      (1600,      16,       0,  70,  11, "Missile",  4, 16000, 480),

            "Dart":           (50,       4,       0,  30,   2, "Thrown",   2, 17000, 512),
            "Knife":         (100,      10,       0,  40,   3, "Thrown",   2, 18000, 544),
            "Hatchet":       (200,      16,       0,  50,   4, "Thrown",   2, 19000, 576),
            "Javelin":       (400,      22,       0,  60,   5, "Thrown",   2, 20000, 608)
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

                    self.inside[raw_key_name] = dict(
                        nam=(material_key + " " + type_key + " " + upgraded_key).strip(),

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

                        # puur voor sortering in de winkels
                        srt=material_value[3] + type_value[7] + upgraded_value[3],

                        col=material_value[4],
                        row=type_value[8]
                    )

        # min_int op None zetten voor close weapons
        # min_str op None zetten voor range weapons
        for weapon_key, weapon_value in self.inside.items():
            if weapon_value['skl'] in ("Sword", "Hafted", "Pole"):
                weapon_value['min_int'] = None
            elif weapon_value['skl'] in ("Missile", "Thrown"):
                weapon_value['min_str'] = None

        self.set_shop()
        self.rearrage()


WeaponsData = WeaponsDataClass()
