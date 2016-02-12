
"""
class: ShieldsDataClass
obj: ShieldsData
"""

import items.gear


class ShieldsDataClass(items.gear.GearDataClass):
    """
    Hier staan alle schilden uit het spel in een dict als enum met een dict voor de waarden.
    """

    @staticmethod
    def factory(shield):
        """
        Maak een object van een enum database item.
        :param shield: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if shield is None:
            return items.gear.GearItem(items.gear.GearType.shield)
        return items.gear.GearItem(items.gear.GearType.shield, **shield)

    def __init__(self):
        super().__init__()

        # Vul de OrderedDict self.inside met de gecombineerde data.

        # todo, upgradable, min_mech, metals zijn nog niet verwerkt.

        #                     val, min str, prt, des, dex, stl,  srt, col
        shield_material = {
            "Wooden":        (200,       3,   2,   1,  -1,  -1,  100,   0),
            "Bronze":        (500,       6,   4,   2,  -2,  -2,  200,  32),
            "Iron":          (800,       9,   6,   3,  -3,  -3,  300,  64),
            "Steel":        (1100,      12,   8,   4,  -4,  -4,  400,  96),
            "Silver":       (1400,      15,  10,   5,  -5,  -5,  500, 128),
            "Titanium":     (1700,       3,  10,   5,  -1,  -1,  600, 160)
            # "Stealth":      (16,       1,   0,   0,  -1,  -1)
        }
        #                     val, min str, prt, des, dex, stl,  srt, row
        shield_type = {
            "Buckler":       (100,       3,   1,   5,  -1,  -3, 1000,   0),
            "Targe":         (700,       6,   2,  10,  -2,  -6, 2000,  32),
            "Heater":       (1300,       9,   3,  15,  -3,  -9, 3000,  64),
            "Kite":         (1900,      12,   4,  20,  -4, -12, 4000,  96),
            "Scutum":       (2500,      15,   5,  25,  -5, -15, 5000, 128)
        }
        #                     val, min str, prt, des, dex, stl,  srt
        shield_upgraded = {
            "":              (1.0,       0,   0,   0,   0,   0,   10),
            "+":             (1.1,       0,   0,   0,   1,   2,   20),
            "++":            (1.2,       0,   0,   0,   2,   4,   30)
        }
        # de hoogste protection/defense mogelijk is 15/30: Large Silver/Titanium Scutum /+/++

        for material_key, material_value in shield_material.items():
            for type_key, type_value in shield_type.items():
                for upgraded_key, upgraded_value in shield_upgraded.items():

                    raw_key_name = (material_key + type_key + upgraded_key).strip().lower().replace(" ", "")
                    # todo, deze int was alleen bij weapon, moet de int hier weer weg?
                    price = int((material_value[0] + type_value[0]) * (material_value[0] + type_value[0]) / 900)

                    self.inside[raw_key_name] = dict(
                        nam=(material_key + " " + type_key + " " + upgraded_key).strip(),

                        # berekening value: material * type * upgraded
                        val=int(price * upgraded_value[0]),
                        shp=True,

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

                        # puur voor sortering in de database, omdat geen enum is
                        srt=material_value[6] + type_value[6] + upgraded_value[6],

                        col=material_value[7],
                        row=type_value[7]
                    )

        self.set_shop()
        self.rearrage()


ShieldsData = ShieldsDataClass()
