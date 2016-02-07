
"""
class: ArmorsDataClass
obj: ArmorsData
"""

import items.gear


class ArmorsDataClass(items.gear.GearDataClass):
    """
    Hier staan alle armors uit het spel in een dict als enum met een dict voor de waarden.
    """
    @staticmethod
    def factory(armor):
        """
        Maak een object van een enum database item.
        :param armor: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.armor, **armor)

    def __init__(self):
        super().__init__()
        """
        Vul de OrderedDict self.inside met de gecombineerde data.
        """

        # col, row, upgradable, min_mech, metals zijn nog niet verwerkt.

        #                     value, weight, prt, stl, sort
        armor_material = {
            "Leather Armor":   (100,      0,   0,   0, 1000),
            "Bronze Armor":    (600,      3,   3,  -3, 2000),
            "Iron Armor":     (1100,      6,   6,  -6, 3000),
            "Steel Armor":    (1600,      9,   9,  -9, 4000),
            "Silver Armor":   (2100,     12,  12, -12, 5000),
            "Titanium Armor": (2600,      0,  12,   0, 6000)
            # "Stealth":        (16,     10,   1,   1)
        }
        #                     value, weight, prt, stl, sort
        armor_type = {
            "Light":           (100,      1,   1,   0,  100),
            "Medium":          (300,      2,   2,  -1,  200),
            "Heavy":           (500,      3,   3,  -2,  300)
        }
        #                     value, weight, prt, stl, sort
        armor_upgraded = {
            "":                (1.0,      0,   0,   0,   10),
            "+":               (1.1,      0,   0,   1,   20),
            "++":              (1.2,     -1,   0,   2,   30)
        }
        # hoogste protection mogelijk is 15: Heavy Silver/Titanium Armor /+/++

        for key_material, value_material in armor_material.items():
            for key_type, value_type in armor_type.items():
                for key_upgraded, value_upgraded in armor_upgraded.items():

                    raw_key_name = (key_type + key_material + key_upgraded).strip().lower().replace(" ", "")
                    price = (value_material[0] + value_type[0]) * (value_material[0] + value_type[0]) / 400

                    self.inside[raw_key_name] = dict(
                        name=(key_type + " " + key_material + " " + key_upgraded).strip(),

                        # berekening value: material * type * upgraded
                        value=int(price * value_upgraded[0]),
                        shop=True,

                        # berekening weight: material + type + upgraded
                        weight=value_material[1] + value_type[1] + value_upgraded[1],

                        # berekening protection: material + type
                        prt=value_material[2] + value_type[2],

                        # berekening stealth: material + type + upgraded
                        stl=value_material[3] + value_type[3] + value_upgraded[3],

                        # puur voor sortering in de database, omdat geen enum is
                        sort=value_material[4] + value_type[4] + value_upgraded[4]
                    )

        # shop uitzetten voor sommige armors
        for k, v in self.inside.items():
            if "+" in k or "titanium" in k:
                v['shop'] = False
        # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable


ArmorsData = ArmorsDataClass()

