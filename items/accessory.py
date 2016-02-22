
"""
class: AccessoriesData
"""

import items.gear

# todo, accessoires afmaken


class AccessoriesData(items.gear.GearData):
    """
    Hier staan alle accessoires uit het spel in als enum met een dict voor de waarden.
    """
    testaccessory = dict(nam="Test Accessory",   val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(accessory):
        """
        Maak een object van een enum database item.
        :param accessory: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if accessory is None:
            return items.gear.GearItem(items.gear.GearType.accessory)
        accessory['spr'] = ""
        return items.gear.GearItem(items.gear.GearType.accessory, **accessory.value)
