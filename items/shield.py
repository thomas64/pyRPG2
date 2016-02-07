
"""
class: ShieldsData
def: fill_shield_data
"""

import collections

import items.gear


class ShieldsDataClass(object):
    """
    Hier staan alle schilden uit het spel in als enum met een dict voor de waarden.
    """
    def __init__(self):
        self.inside = collections.OrderedDict()

    def __iter__(self):                 # om gesorteerd op winkelvolgorde te laten zien
        return iter(sorted(self.inside.items(), key=lambda xx: xx[1]['sort']))      # [1] dan zijn het de .values()

    def __setitem__(self, key, value):  # om nieuwe attributen toe te kunnen voegen
        self.inside[key] = value

    def __getattr__(self, key):         # om een nieuwe aan te kunnen maken met factory
        return self.inside[key]

    @staticmethod
    def factory(shield):
        """
        Maak een object van een enum database item.
        :param shield: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.shield, **shield)


def fill_shield_data():
    """
    Vul de OrderedDict self.inside met de gecombineerde data.
    """

    # upgradable, min_mech, metals zijn nog niet verwerkt.

    #                   value, min str, prt, def, dex, stl, sortering, col
    shield_material = {
        "Wooden":        (200,       3,   2,   1,  -1,  -1,       100,   0),
        "Bronze":        (500,       6,   4,   2,  -2,  -2,       200,  32),
        "Iron":          (800,       9,   6,   3,  -3,  -3,       300,  64),
        "Steel":        (1100,      12,   8,   4,  -4,  -4,       400,  96),
        "Silver":       (1400,      15,  10,   5,  -5,  -5,       500, 128),
        "Titanium":     (1700,       3,  10,   5,  -1,  -1,       600, 160)
        # "Stealth":      (16,       1,   0,   0,  -1,  -1)
    }
    #                   value, min str, prt, def, dex, stl, sortering, row
    shield_type = {
        "Buckler":       (100,       3,   1,   5,  -1,  -3,      1000,   0),
        "Targe":         (700,       6,   2,  10,  -2,  -6,      2000,  32),
        "Heater":       (1300,       9,   3,  15,  -3,  -9,      3000,  64),
        "Kite":         (1900,      12,   4,  20,  -4, -12,      4000,  96),
        "Scutum":       (2500,      15,   5,  25,  -5, -15,      5000, 128)
    }
    #                   value, min str, prt, def, dex, stl, sortering
    shield_upgraded = {
        "":              (1.0,       0,   0,   0,   0,   0,        10),
        "+":             (1.1,       0,   0,   0,   1,   2,        20),
        "++":            (1.2,       0,   0,   0,   2,   4,        30)
    }
    # de hoogste protection/defense mogelijk is 15/30: Large Silver/Titanium Scutum /+/++

    for key_material, value_material in shield_material.items():
        for key_type, value_type in shield_type.items():
            for key_upgraded, value_upgraded in shield_upgraded.items():

                raw_key_name = (key_material + key_type + key_upgraded).strip().lower().replace(" ", "")
                price = (value_material[0] + value_type[0]) * (value_material[0] + value_type[0]) / 900

                ShieldsData[raw_key_name] = dict(
                    name=(key_material + " " + key_type + " " + key_upgraded).strip(),

                    # berekening value: material * type * upgraded
                    value=int(price * value_upgraded[0]),
                    shop=True,

                    # berekening min str: material + type
                    min_str=value_material[1] + value_type[1],

                    # berekening protection: material + type
                    prt=value_material[2] + value_type[2],

                    # berekening defense: material + type
                    defense=value_material[3] + value_type[3],

                    # berekening dexterity: material + type + upgraded
                    dex=value_material[4] + value_type[4] + value_upgraded[4],

                    # berekening stealth: material + type + upgraded
                    stl=value_material[5] + value_type[5] + value_upgraded[5],

                    # puur voor sortering in de winkels
                    sort=value_material[6] + value_type[6] + value_upgraded[6],

                    col=value_material[7],
                    row=value_type[7]
                )

    # shop uitzetten voor sommige armors
    for k, v in ShieldsData:
        if "+" in k or "titanium" in k:
            v['shop'] = False
    # de laatste van shop is misschien niet nodig. dit kan ook in de shop zelf gecheckt worden. scheelt een variable.


ShieldsData = ShieldsDataClass()
fill_shield_data()


# piet = ShieldsData.factory(ShieldsData.woodenbuckler)
# print(piet)
#
# for shield in ShieldsData:
#     print(shield[1]['name'])
#
# quit()
